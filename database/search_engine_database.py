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
