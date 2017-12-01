from data.article import Article
import xml.etree.ElementTree as ElementTree

from data.articles_statistic import ArticlesStatistic
from data.signature import Signature


class Deserializer:
    # creates an article array from a xml
    @staticmethod
    def deserialize_articles_xml(articles_xml):
        articles = []

        # check if document root was provided, if not get it
        if type(articles_xml) is ElementTree.Element:
            root = articles_xml
        else:
            root = ElementTree.fromstring(articles_xml)

        # from every root child deserialize article and append to array
        for row in root:
            articles.append(Deserializer.deserialize_article_xml(row))

        return articles

    # creates an article object from a xml
    @staticmethod
    def deserialize_article_xml(article_xml):
        article_id = 0
        version = 0
        content = ""
        date = ""
        source = ""
        title = ""
        url = ""

        # check if document root was provided, if not get it
        if type(article_xml) is ElementTree.Element:
            root = article_xml
        else:
            root = ElementTree.fromstring(article_xml)

        # evaluate all child elements and get its content
        for child in root:
            tag = child.tag
            text = child.text
            if tag == "id":
                article_id = text
            elif tag == "version":
                version = text
            elif tag == "content":
                content = text
            elif tag == "date":
                date = text
            elif tag == "source":
                source = text
            elif tag == "title":
                title = text
            elif tag == "url":
                url = text

        # create article from receive information
        article = Article(article_id, version, content, date, source, title, url)
        return article

    # create an article object from a json
    @staticmethod
    def deserialize_article_json(article_json):
        article_id = article_json["article_id"]
        version = article_json["version"]
        content = article_json["content"]
        date = article_json["date"]
        source = article_json["source"]
        title = article_json["title"]
        url = article_json["url"]
        words = article_json["words"]
        stop_words = article_json["stop_words"]
        stems = article_json["stems"]
        duplicates = article_json["duplicates"]
        return Article(article_id, version, content, date, source, title, url, words, stems, stop_words, duplicates)

    @staticmethod
    def deserialize_articles_json(articles_json):
        articles = []
        for article_json in articles_json:
            articles.append(Deserializer.deserialize_article_json(article_json))
        return articles

    @staticmethod
    def deserialize_articles_statistic(articles_statistic_json):
        sources = articles_statistic_json["sources"]
        words = articles_statistic_json["words"]
        article_count = articles_statistic_json["article_count"]
        return ArticlesStatistic(sources, words, article_count)

    @staticmethod
    def deserialize_signature(signature_json):
        article_id = signature_json["article_id"]
        signature = signature_json["signature"]
        return Signature(article_id, signature)

    @staticmethod
    def deserialize_signatures(signatures_json):
        signatures = []
        for signature in signatures_json:
            signatures.append(Deserializer.deserialize_signature(signature))

        return signatures

