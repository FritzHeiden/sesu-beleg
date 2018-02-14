from gensim.models import Word2Vec


class Similarity:

    @staticmethod
    def train(articles):
        sentences = []
        for article in articles:
            sentences.append(article.get_words().keys())

        model = Word2Vec(sentences,size=100, window=5, min_count=5)
        #model = Word2Vec(sentences,min_count = 1)
        model.save("trained.model")
        print (sentences)


    @staticmethod
    def similarity(Wort1, Wort2):
        model = Word2Vec.load("trained.model")
        return model.wv.similarity(Wort1,Wort2)
