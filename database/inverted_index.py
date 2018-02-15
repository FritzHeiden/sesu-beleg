import math
from data.articles_statistic import ArticlesStatistic


class InvertedIndex:
    def __init__(self, searchEngineDatabase):
        self.searchEngineDatabase = searchEngineDatabase

    def get_term_frequency(self, word, article_id):
        inv_index = self.searchEngineDatabase.get_inverted_index(word)
        for index in inv_index:
            if inv_index == article_id:
                return inv_index[1]
        return None
        # ToDo get term frequency from database
        # pass

    def get_inverted_document_frequency(self, word):
        total_article_count = len(self.searchEngineDatabase.get_posts(word))
        article_containing_word_count = self.searchEngineDatabase.get_articles_statistic().get_article_count()

        return math.log(total_article_count / article_containing_word_count)
