from analyse.counter import Counter
from analyse.min_hasher import MinHasher
from analyse.shingle_generator import ShingleGenerator
from analyse.stemmer import Stemmer
from analyse.text_analyser import TextAnalyser
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

    @staticmethod
    def get_duplicates(signatures, reference_signature):
        duplicates = {}

        # ToDo dubletten erkennen. min. ein band aus den signaturen muss mit einem band der referenz signatur
        # übereinstimmen. dann jaccard ähnlichkeit bestimmen. bei > 80% eintrag in duplicates[80], bei > 85% eintrag
        # in duplicates[85] und bei > 90% eintrag in duplicates[90] (article id des duplikats)
        # siehe data.signature klasse

        return duplicates

    @staticmethod
    def analyse_article(article=None, database=None):
        # analyse words from content and add them to the article object
        words = TextAnalyser.analyse_words(article.get_content())
        article.set_words(Counter.count_words(words))

        stop_words = TextAnalyser.analyse_stop_words(article.get_content())
        article.set_stop_words(Counter.count_words(stop_words))

        # create stems from words and add them to the article object
        article.add_stems(Stemmer.get_stems(words))

        # Generate Shingles from stop words
        shingles = ShingleGenerator.generate_stop_word_shingles(article.get_content(), 5)

        # add shingles to shingle map in database
        database.add_shingles(shingles)
        # get shingle map from database
        shingles = database.get_shingle_ids(shingles)
        # get hash functions from database
        hash_functions = database.get_hash_functions(200)

        # generate min hash signature for current documents shingles
        reference_signature = MinHasher.generate_min_hash(shingles, hash_functions)

        # get all min hash signatures
        signatures = database.get_signatures()

        # determine duplicates
        duplicates = ArticlesAnalyser.get_duplicates(signatures, reference_signature)

        # add min hash signature of current document to signature index
        database.add_signature(reference_signature)

        # ToDo add duplicate references to article

        return article
