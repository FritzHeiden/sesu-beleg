from gensim.models import Word2Vec
import math


class Similarity:
    @staticmethod
    def train(articles):
        sentences = []
        for article in articles:
            sentences.append(article.get_words().keys())

        # model = Word2Vec(sentences,size=100, window=5, min_count=5)
        print("1")
        model = Word2Vec(sentences, min_count=1)
        print("2")
        model.save("trained.model")
        print(sentences)

    @staticmethod
    def similarity(Wort1, Wort2):
        model = Word2Vec.load("trained.model")
        return model.wv.similarity(Wort1, Wort2)

    @staticmethod
    def cosine_similarity(query, article, inverted_index):
        query = query.split()

        factor1 = 0
        factor2 = 0
        factor3 = 0
        for word in query:
            tf = inverted_index.get_term_frequency(word, article.get_article_id())
            idf = inverted_index.get_inverted_document_frequency(word)
            idf_sqr = math.pow(idf, 2)
            factor1 += tf * idf_sqr
            factor3 += idf_sqr
        factor3 = math.sqrt(factor3)

        for word in article.get_words():
            tf = inverted_index.get_term_frequency(word, article.get_article_id())
            idf = inverted_index.get_inverted_document_frequency(word)
            factor2 += math.pow(tf * idf, 2)
        factor2 = math.sqrt(factor2)

        return factor1 / (factor2 * factor3)

    @staticmethod
    def soft_cosine_similarity(query, article, inverted_index):
        query = query.split()

        factor1 = 0
        factor2 = 0
        factor3 = 0

        for word_q in query:
            for word_a in article.get_words():
                similarity = Similarity.similarity(word_a, word_q)
                tf = inverted_index.get_term_frequency(word_a, article.get_article_id())
                idf_q = inverted_index.get_inverted_document_frequency(word_q)
                idf_a = inverted_index.get_inverted_document_frequency(word_a)
                factor1 += similarity * tf * idf_a * idf_q

        for word_1 in article.get_words():
            for word_2 in article.get_words():
                similarity = Similarity.similarity(word_1, word_2)
                tf_1 = inverted_index.get_term_frequency(word_1, article.get_article_id())
                tf_2 = inverted_index.get_term_frequency(word_2, article.get_article_id())
                idf_1 = inverted_index.get_inverted_document_frequency(word_1)
                idf_2 = inverted_index.get_inverted_document_frequency(word_2)
                factor2 += similarity * tf_1 * idf_1 * tf_2 * idf_2
        factor2 = math.sqrt(factor2)

        for word_1 in query:
            for word_2 in query:
                similarity = Similarity.similarity(word_1, word_2)
                idf_1 = inverted_index.get_inverted_document_frequency(word_1)
                idf_2 = inverted_index.get_inverted_document_frequency(word_2)
                factor3 += similarity * idf_1 * idf_2
        factor3 = math.sqrt(factor3)

        return factor1 / (factor2 * factor3)
