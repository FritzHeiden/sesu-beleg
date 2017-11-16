from network.url_helper import UrlHelper
from serialization.deserializer import Deserializer
from analyse.word_analyser import WordAnalyser
from database.search_engine_database import SearchEngineDatabase

# data source
test_data_url = "http://daten.datenlabor-berlin.de/test.xml"

# mongodb connection information
mongodb_host = "spadi8.f4.htw-berlin.de"
mongodb_port = 28018
mongodb_db_name = "search_engine"

# initialize database
database = SearchEngineDatabase(mongodb_host, mongodb_port)

# download xml documents
article_xml = UrlHelper.retrieve_url(test_data_url)
# deserialize documents
articles = Deserializer.deserialize_articles(article_xml)

for article in articles:
    # analyse words from content and add them to the article object
    article.add_words(WordAnalyser.analyse_words(article.get_content()))
    # persist article in database
    database.insert_article(article)

# get all article stored in database
articles = database.get_articles()

# print articles
for article in articles:
    print(article)
