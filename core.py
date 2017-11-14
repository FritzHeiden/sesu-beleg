from network.url_helper import UrlHelper
from serialization.deserializer import Deserializer
from analyse.word_analyser import WordAnalyser

test_data_url = "http://daten.datenlabor-berlin.de/test.xml"

article_xml = UrlHelper.retrieve_url(test_data_url)

articles = Deserializer.deserialize_articles(article_xml)

for article in articles:
    article.add_words(WordAnalyser.analyse_words(article.get_content()))
    for word in article.get_words():
        print(word)

