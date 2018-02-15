import math
from data.articles_statistic import ArticlesStatistic


class InvertedIndex:
    def __init__(self, searchEngineDatabase):
        self.searchEngineDatabase = searchEngineDatabase

    def get_term_frequency(self, word, article_id):
        posts = self.searchEngineDatabase.get_posts(word)
        for post in posts:
            if post["article_id"] == article_id:
                return post["tf"]
        return 0

    def get_inverted_document_frequency(self, word):
        total_article_count = len(self.searchEngineDatabase.get_posts(word))
        article_containing_word_count = self.searchEngineDatabase.get_articles_statistic().get_article_count()

        return math.log(total_article_count / article_containing_word_count)
