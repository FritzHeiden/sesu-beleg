class ArticlesStatistic:
    def __init__(self, sources=None, words=None, article_count=0):
        if sources is None:
            sources = {}
        if words is None:
            words = {}
        self.__sources = sources
        self.__words = words
        self.__article_count = article_count

    def get_sources(self):
        return self.__sources

    def set_sources(self, sources):
        self.__sources = sources

    def __str__(self):
        return "ArticlesStatistic{{sources: {0}, words: {1}}}".format(self.get_sources(), self.get_words())

    def get_words(self):
        return self.__words

    def set_words(self, words):
        self.__words = words

    def get_article_count(self):
        return self.__article_count

    def set_article_count(self, article_count):
        self.__article_count = article_count
