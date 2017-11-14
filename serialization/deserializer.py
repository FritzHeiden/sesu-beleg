from data.article import Article
import xml.etree.ElementTree as ElementTree


class Deserializer:
    @staticmethod
    def deserialize_articles(articles_xml):
        articles = []

        if type(articles_xml) is ElementTree.Element:
            root = articles_xml
        else:
            root = ElementTree.fromstring(articles_xml)

        for row in root:
            articles.append(Deserializer.deserialize_article(row))

        return articles

    @staticmethod
    def deserialize_article(article_xml):
        id = 0
        version = 0
        content = ""
        date = ""
        source = ""
        title = ""
        url = ""

        if type(article_xml) is ElementTree.Element:
            root = article_xml
        else:
            root = ElementTree.fromstring(article_xml)

        for child in root:
            tag = child.tag
            text = child.text
            if tag == "id":
                id = text
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

        article = Article(id, version, content, date, source, title, url)
        return article
