from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

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
        self._article_collection.update(query, document, upsert=True)

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


    # create query that specifies the given article
    @staticmethod
    def __article_update_query(article):
        return {"article_id": article.get_article_id()}


