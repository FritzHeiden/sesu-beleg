from random import randint

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from data.articles_statistic import ArticlesStatistic
from data.hash_function import HashFunction
from data.signature import Signature
from serialization.deserializer import Deserializer
from serialization.serializer import Serializer
from tools.shingle_comparator import ShingleComparator


class SearchEngineDatabase:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        # initialize the mongo client
        self._client = MongoClient(self._host, self._port)

        # check if connection was successful
        try:
            self._client.admin.command("ismaster")
        except ConnectionFailure as e:
            raise e

        # get the db and collection to store our data in
        self._db = self._client["search_engine"]
        self._article_collection = self._db["articles"]
        self._statistics_collection = self._db["statistics"]
        self._meta_data_collection = self._db["meta"]
        self._shingles_collection = self._db["shingles"]
        self._counters_collection = self._db["counters"]

    # inserts an article if its not present in the db
    def insert_article(self, article):
        # create document that is understood by mongodb
        document = Serializer.serialize_article_json(article)
        # create a query which determines if documents is already in db
        query = self.__article_update_query(article)
        # execute query; if document is present, it is being updated; upsert true causes mongodb to insert article if
        # its not present
        return self._article_collection.update(query, document, upsert=True)["updatedExisting"]

    # find an article by its article id
    def get_article(self, article_id):
        # execute query with criteria article_id
        document = self._article_collection.find_one({"article_id": article_id})
        if document is not None:
            # deserialize and return if an article was returned
            return Deserializer.deserialize_article_json(document)
        else:
            return None

    # gets all articles present in the database
    def get_articles(self):
        # execute query
        documents = self._article_collection.find()
        articles = []
        for document in documents:
            # deserialize articles and add them to the array
            articles.append(Deserializer.deserialize_article_json(document))
        # return all found articles
        return articles

    def get_articles_range(self, start, end):
        documents = self._article_collection.find().sort([("article_id", 1)]).limit(end - start).skip(start)
        return Deserializer.deserialize_articles_json(documents)

    # create query that specifies the given article
    @staticmethod
    def __article_update_query(article):
        return {"article_id": article.get_article_id()}

    def add_articles_statistic(self, articles_statistic):
        if self._statistics_collection.find_one({"id": "articles_statistic"}) is None:
            self._statistics_collection.insert(Serializer.serialize_articles_statistic(ArticlesStatistic()))

        inc_dict = {}

        sources = articles_statistic.get_sources()
        if len(sources) > 0:
            for source in sources:
                inc_dict["sources.{0}".format(source)] = sources[source]

        words = articles_statistic.get_words()
        if len(words) > 0:
            for word in words:
                inc_dict["words.{0}".format(word)] = words[word]

        article_count = articles_statistic.get_article_count()
        inc_dict["article_count"] = article_count

        self._statistics_collection.update({"id": "articles_statistic"},
                                           {"$inc": inc_dict})

    def get_articles_statistic(self):
        articles_statistic_json = self._statistics_collection.find_one({"id": "articles_statistic"})
        if articles_statistic_json is None:
            return None

        return Deserializer.deserialize_articles_statistic(articles_statistic_json)

    def add_shingles(self, shingles):
        for shingle in shingles:
            if self._shingles_collection.find_one({"shingle": shingle}) is not None:
                continue
            self.increase_counter("shingle_id")
            shingle_id = self.get_counter("shingle_id")
            self._shingles_collection.update({"shingle": shingle},
                                             {"shingle": shingle, "id": shingle_id}, upsert=True)

    def increase_counter(self, counter_name):
        if self._counters_collection.find_one({"_id": counter_name}) is None:
            self._counters_collection.insert_one({"_id": counter_name, "seq": 1})
        else:
            self._counters_collection.update({"_id": counter_name}, {"$inc": {"seq": 1}})

    def get_counter(self, counter_name):
        counter = self._counters_collection.find_one({"_id": counter_name})
        if counter is None:
            return 0
        else:
            counter = counter["seq"]
            if counter is None:
                return 0
            else:
                return counter

    def get_shingle_ids(self, shingles):
        shingles_with_id = []

        for shingle in shingles:
            entry = self._shingles_collection.find_one({"shingle": shingle})
            if entry is None:
                continue
            shingles_with_id.append({"shingle": shingle, "id": entry["id"]})

        return shingles_with_id

    def get_hash_functions(self, functions_count):
        hash_parameters = self._meta_data_collection.find_one({"id": "hash_parameters"})
        if hash_parameters is None:
            hash_parameters = {"id": "hash_parameters", "parameters": {}}
            self._meta_data_collection.update({"id": "hash_parameters"}, hash_parameters, upsert=True)

        parameters = hash_parameters["parameters"]
        if len(parameters) < functions_count:
            next_id = 1
            while str(next_id) in parameters:
                next_id += 1

            while len(parameters) < functions_count:
                new_parameters = {}
                found = False
                while found is False:
                    new_parameters = {
                        "a": randint(0, 2 ** 32 - 1),
                        "b": randint(0, 2 ** 32 - 1),
                        "c": 4294967311
                    }
                    found = True
                    for parameters_id in parameters:
                        found = False
                        for i in parameters[parameters_id]:
                            parameter1 = parameters[parameters_id][i]
                            parameter2 = new_parameters[i]
                            if parameter1 != parameter2:
                                found = True
                        if found is False:
                            break
                parameters[next_id] = new_parameters
                self._meta_data_collection.update({"id": "hash_parameters"},
                                                  {"$set": {"parameters." + str(next_id): new_parameters}})
                next_id += 1

        hash_functions = []
        for parameter_id in parameters:
            hash_functions.append(
                HashFunction(parameter_id, parameters[parameter_id]["a"], parameters[parameter_id]["b"],
                             parameters[parameter_id]["c"]))

        return hash_functions

    def get_shingle_map(self):
        shingles_map = self._meta_data_collection.find_one({"id": "shingles_map"})
        if shingles_map is None:
            return {}
        return shingles_map["shingles"]

    def get_signatures(self):
        signatures_json = self._meta_data_collection.find_one({"id": "signatures"})
        if signatures_json is None:
            return []

        signatures = Deserializer.deserialize_signatures(signatures_json["signatures"])

        return signatures

    def add_signature(self, signature):
        signatures = self._meta_data_collection.find_one({"id": "signatures"})
        if signatures is None:
            signatures = {"id": "signatures", "signatures": []}
            self._meta_data_collection.update({"id": "signatures"}, signatures, upsert=True)

        signatures = Deserializer.deserialize_signatures(signatures["signatures"])

        found = False
        for compare_signature in signatures:
            if compare_signature.get_article_id() == signature.get_article_id():
                found = True
                break

        if found is False:
            self._meta_data_collection.update({"id": "signatures"},
                                              {"$push": {"signatures": Serializer.serialize_signature(signature)}})
