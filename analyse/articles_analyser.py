from analyse.counter import Counter
from data.articles_statistic import ArticlesStatistic


class ArticlesAnalyser:
    @staticmethod
    def get_article_statistic(article):
        return ArticlesAnalyser.get_articles_statistic([article])

    @staticmethod
    def get_articles_statistic(articles):
        sources = Counter.count_article_sources(articles)
        words = {}
        for article in articles:
            article_words = article.get_words()
            for word in article_words:
                if word in words:
                    words[word] = words[word] + article_words[word]
                else:
                    words[word] = article_words[word]

        article_count = len(articles)
        return ArticlesStatistic(sources, words, article_count)
