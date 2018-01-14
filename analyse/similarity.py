from gensim.models import Word2Vec


class Similarity:

    @staticmethod
    def train(articles):
        sentences = []
        for article in articles:
            sentences.append(article.get_words().keys())


        model = Word2Vec(sentences,min_count = 1)
        model.save("test.test")
        print (sentences)

    @staticmethod
    def similarity(Wort1, Wort2):
        model = Word2Vec.load("test.test")
        print( model.wv.similarity(Wort1,Wort2))
        #print("as")

