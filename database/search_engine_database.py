import math
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from data.articles_statistic import ArticlesStatistic
from serialization.deserializer import Deserializer
from serialization.serializer import Serializer


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
        self._inverted_index_collection = self._db["inverted_index"]

    # inserts an article if its not present in the db
    def insert_article(self, article):
        # create document that is understood by mongodb
        document = Serializer.serialize_article_json(article)
        # create a query which determines if documents is already in db
        query = self.__article_update_query(article)
        # execute query; if document is present, it is being updated; upsert true causes mongodb to insert article if
        # its not present
        self._article_collection.insert(document)

    # find an article by its article id
    def get_article(self, article_id):
        # execute query with criteria article_id
        document = self._article_collection.find_one({"article_id": article_id})
        if document is not None:
            # deserialize and return if an article was returned
            return Deserializer.deserialize_article_json(document)
        else:
            return None

    def article_exists(self, article_id):
        # execute query with criteria article_id
        document = self._article_collection.find({"article_id": article_id}).limit(1)
        return len(document) > 0

    # gets all articles present in the database
    def get_articles(self, article_ids=None):
        # execute query
        if article_ids is None:
            documents = self._article_collection.find()
        else:
            documents = self._article_collection.find({"article_id": {"$in": article_ids}})

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

        # sources = articles_statistic.get_sources()
        # if len(sources) > 0:
        #     for source in sources:
        #         inc_dict["sources.{0}".format(source)] = sources[source]
        #
        # words = articles_statistic.get_words()
        # if len(words) > 0:
        #     for word in words:
        #         inc_dict["words.{0}".format(word)] = words[word]

        article_count = articles_statistic.get_article_count()
        inc_dict["article_count"] = article_count

        self._statistics_collection.update({"id": "articles_statistic"},
                                           {"$inc": inc_dict})

    def get_articles_statistic(self):
        articles_statistic_json = self._statistics_collection.find_one({"id": "articles_statistic"})
        if articles_statistic_json is None:
            return None

        return Deserializer.deserialize_articles_statistic(articles_statistic_json)

    def add_inverted_index(self, word, post):

        if self.get_inverted_index(word) is not None:
            # print("hallo")
            post_tmp = post
            post = self.get_inverted_index(word)
            post.append(post_tmp)

        inv_index = Serializer.serialize_inverted_index(word, post)

        # return self._inverted_index_collection.update(word, post, upsert=True)["updatedExisting"]
        return self._inverted_index_collection.update({"word": word}, {"word": word, "post": post}, upsert=True)[
            "updatedExisting"]

    def get_inverted_index(self, word):
        inv_index = self._inverted_index_collection.find_one({"word": word})
        if inv_index is not None:
            return Deserializer.deserialize_inverted_index(inv_index)
        else:
            return None

    def add_post(self, word, post):
        if len(self._inverted_index_collection.find({"word": word}).limit(1)) == 0:
            self._inverted_index_collection.insert({"word": word, "posts": [post]})
        else:
            self._inverted_index_collection.update({"word": word}, {"$push": {"posts": post}})

    def get_posts(self, word):
        result = self._inverted_index_collection.find({"word": word}).limit(1)
        if result == 0:
            return None
        return result[0]["posts"]

    def get_term_frequencies(self, words, article_id):
        results = self._inverted_index_collection.find({"word": {"$in": words}})
        tfs = []
        for result in results:
            for post in result["posts"]:
                if post["article_id"] == article_id:
                    tfs.append({"word": result["word"], "tf": post["tf"]})
        return tfs

    def get_inverted_document_frequencies(self, words):
        results = self._inverted_index_collection.find({"word": {"$in": words}})
        idfs = []
        total_article_count = self._statistics_collection.find_one({"id": "articles_statistic"})["article_count"]

        for result in results:
            article_containing_word_count = len(result["posts"])
            idfs.append({"word": result["word"], "idf": math.log(total_article_count / article_containing_word_count)})

        return idfs

    def add_shingles(self, shingles):
        # ToDo implement add_shingles
        pass

    def get_hash_functions(self, functions_count):
        # ToDo implement get_hash_functions
        pass

    def get_shingle_map(self):
        # ToDo implement get_shingle_map
        pass

    def get_signatures(self):
        # ToDo implement get_signatures
        pass

    def add_signature(self, signature):
        # ToDo implement add_signature
        pass
