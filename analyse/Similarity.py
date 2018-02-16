from gensim.models import Word2Vec
import math


class Similarity:
    @staticmethod
    def train(articles):
        sentences = []
        for article in articles:
            for i in range(0, len(article.get_stems()) - 5):
                sentences.append(article.get_stems()[i:i+5])

        # model = Word2Vec(sentences,size=100, window=5, min_count=5)
        model = Word2Vec(sentences, min_count=1)
        model.save("trained.model")
        print(sentences)

    @staticmethod
    def similarity(Wort1, Wort2):
        model = Word2Vec.load("trained.model")
        return model.wv.similarity(Wort1, Wort2)

    @staticmethod
    def cosine_similarity(query, article, database):
        query = query.split()

        print("Getting tfs and idfs ...")
        article_tfs = database.get_term_frequencies(article.get_stems(), article.get_article_id())
        article_idfs = database.get_inverted_document_frequencies(article.get_stems())
        print("Done.")

        factor1 = 0
        factor2 = 0
        factor3 = 0
        for word in query:
            tf = 0
            for tf in article_tfs:
                if tf["word"] == word:
                    tf = tf["tf"]
                    break
            idf = 0
            for idf in article_idfs:
                if idf["word"] == word:
                    idf = idf["idf"]
                    break
            idf_sqr = math.pow(idf, 2)
            factor1 += tf * idf_sqr
            factor3 += idf_sqr
        factor3 = math.sqrt(factor3)

        for word in article.get_stems():
            tf = 0
            for tf in article_tfs:
                if tf["word"] == word:
                    tf = tf["tf"]
                    break
            idf = 0
            for idf in article_idfs:
                if idf["word"] == word:
                    idf = idf["idf"]
                    break
            factor2 += math.pow(tf * idf, 2)
        factor2 = math.sqrt(factor2)

        return factor1 / (factor2 * factor3)

    @staticmethod
    def soft_cosine_similarity(query, article, database):
        query = query.split()

        query_idfs = database.get_inverted_document_frequencies(query)
        article_tfs = database.get_term_frequencies(article.get_stems(), article.get_article_id())
        article_idfs = database.get_inverted_document_frequencies(article.get_stems())

        factor1 = 0
        factor2 = 0
        factor3 = 0

        total = 2 * len(query) + len(article.get_stems())
        count = 0
        for word_q in query:
            for word_a in article.get_stems():
                similarity = Similarity.similarity(word_a, word_q)
                tf = 0
                for tf in article_tfs:
                    if tf["word"] == word_a:
                        tf = tf["tf"]
                        break
                idf_q = 0
                for idf in article_idfs:
                    if idf["word"] == word_q:
                        idf_q = idf["idf"]
                        break
                idf_a = 0
                for idf in article_idfs:
                    if idf["word"] == word_a:
                        idf_a = idf["idf"]
                        break
                factor1 += similarity * tf * idf_a * idf_q
                count += 1
                print("Calculating soft cosine similarity: {0}% ({1}/{2})".format(math.floor(count / total * 10000)/100, count, total))

        for word_1 in article.get_stems():
            for word_2 in article.get_stems():
                similarity = Similarity.similarity(word_1, word_2)
                tf_1 = 0
                for tf in article_tfs:
                    if tf["word"] == word_1:
                        tf_1 = tf["tf"]
                        break
                tf_2 = 0
                for tf in article_tfs:
                    if tf["word"] == word_2:
                        tf_2 = tf["tf"]
                        break
                idf_1 = 0
                for idf in article_idfs:
                    if idf["word"] == word_1:
                        idf_1 = idf["idf"]
                        break
                idf_2 = 0
                for idf in article_idfs:
                    if idf["word"] == word_2:
                        idf_2 = idf["idf"]
                        break
                factor2 += similarity * tf_1 * idf_1 * tf_2 * idf_2
                count += 1
                print("Calculating soft cosine similarity: {0}% ({1}/{2})".format(math.floor(count / total * 10000)/100, count, total))
        factor2 = math.sqrt(factor2)

        for word_1 in query:
            for word_2 in query:
                similarity = Similarity.similarity(word_1, word_2)
                idf_1 = 0
                for idf in article_idfs:
                    if idf["word"] == word_1:
                        idf_1 = idf["idf"]
                        break
                idf_2 = 0
                for idf in article_idfs:
                    if idf["word"] == word_2:
                        idf_2 = idf["idf"]
                        break
                factor3 += similarity * idf_1 * idf_2
                count += 1
                print("Calculating soft cosine similarity: {0}% ({1}/{2})".format(math.floor(count / total * 10000)/100, count, total))
        factor3 = math.sqrt(factor3)

        return factor1 / (factor2 * factor3)
