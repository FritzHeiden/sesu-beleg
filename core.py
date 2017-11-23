from analyse.articles_analyser import ArticlesAnalyser
from analyse.stemmer import Stemmer
from analyse.counter import Counter
from analyse.word_analyser import WordAnalyser
from database.search_engine_database import SearchEngineDatabase
from network.url_helper import UrlHelper
from serialization.deserializer import Deserializer

# data source
test_data_url = "http://daten.datenlabor-berlin.de/test.xml"
# test_data_url = "http://daten.datenlabor-berlin.de/newspart1.xml"

# mongodb connection information
mongodb_host = "spadi8.f4.htw-berlin.de"
# mongodb_host = "localhost"
mongodb_port = 28018
mongodb_db_name = "search_engine"

# initialize database
database = SearchEngineDatabase(mongodb_host, mongodb_port)

# download xml documents
article_xml = UrlHelper.retrieve_url(test_data_url)
# deserialize documents
articles = Deserializer.deserialize_articles_xml(article_xml)

for article in articles:
    # analyse words from content and add them to the article object
    article.add_words(WordAnalyser.analyse_words(article.get_content()))
    # create stems from words and add them to the article object
    article.add_stems(Stemmer.get_stems(article.get_words()))
    # persist article in database
    database.insert_article(article)

# get all article stored in database
articles = database.get_articles()

#anzahl der articel
print(Counter.countArticles(articles))
#anzahl der worte
print(Counter.countWords(articles))
#die x (= 5) häufigst auftretenden worte
print(Counter.topWords(Counter.countWords(articles),5))

print(Counter.countArticles(articles))
print(Counter.countWords(articles))

# print articles
for article in articles:
    print(article)

print(ArticlesAnalyser.get_articles_statistic(articles))
