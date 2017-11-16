from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from data.article import Article


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

    # inserts an article if its not present in the db
    def insert_article(self, article):
        # create document that is understood by mongodb
        document = self.__serialize_article(article)
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
            return self.__deserialize_article(document)
        else:
            return None

    # gets all articles present in the database
    def get_articles(self):
        # execute query
        documents = self._article_collection.find()
        articles = []
        for document in documents:
            # deserialize articles and add them to the array
            articles.append(self.__deserialize_article(document))
        # return all found articles
        return articles

    # creates an document that is understandable by mongodb
    @staticmethod
    def __serialize_article(article):
        return {"article_id": article.get_article_id(),
                "version": article.get_version(),
                "content": article.get_content(),
                "date": article.get_date(),
                "source": article.get_source(),
                "title": article.get_title(),
                "url": article.get_url(),
                "words": article.get_words()}

    # create an article object based on an mongodb document
    @staticmethod
    def __deserialize_article(document):
        article_id = document["article_id"]
        version = document["version"]
        content = document["content"]
        date = document["date"]
        source = document["source"]
        title = document["title"]
        url = document["url"]
        words = document["words"]
        return Article(article_id, version, content, date, source, title, url, words)

    # create query that specifies the given article
    @staticmethod
    def __article_update_query(article):
        return {"article_id": article.get_article_id()}
