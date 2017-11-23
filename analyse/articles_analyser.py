from analyse.counter import Counter
from data.articles_statistic import ArticlesStatistic


class ArticlesAnalyser:
    @staticmethod
    def get_articles_statistic(articles):
        source_counts = Counter.count_article_sources(articles)
        return ArticlesStatistic(source_counts)
