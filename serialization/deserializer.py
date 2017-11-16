from data.article import Article
import xml.etree.ElementTree as ElementTree


class Deserializer:
    # creates an article array from a xml
    @staticmethod
    def deserialize_articles(articles_xml):
        articles = []

        # check if document root was provided, if not get it
        if type(articles_xml) is ElementTree.Element:
            root = articles_xml
        else:
            root = ElementTree.fromstring(articles_xml)

        # from every root child deserialize article and append to array
        for row in root:
            articles.append(Deserializer.deserialize_article(row))

        return articles

    # creates an article object from a xml
    @staticmethod
    def deserialize_article(article_xml):
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
