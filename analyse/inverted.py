from analyse.stemmer import Stemmer
from collections import defaultdict

class Inverted:
    @staticmethod
    def inverted_File(article):
        di = {}
        counter = 0
        wort_liste = []
        #for article in articles:
        for word in article.get_content().split():
            wort_liste.append(word)
        wort_liste = Stemmer.get_stems(wort_liste)
        #print(wort_liste)
        for word in wort_liste:
            li = []
            di[word] = li

        for word in wort_liste:
            counter +=1
            a = counter
            di[word].append(a)
            #print(di)
        return di


    @staticmethod
    def inverted_index(words):
        di = {}
        position = 0

        for word in words:
            li = []
            di[Stemmer.single_stem(word)] = li
        for word in words:
            position += 1
            di[Stemmer.single_stem(word)].append(position)
        return di



        # dic{wort: [position]}

    @staticmethod
    def inverted_index_all (articles):

        word_dict = {}
        for article in articles:
            for word in article.get_inverted_index().keys():
                word_dict[(word, article.get_article_id())] = (article.get_inverted_index()[word])




        # word_dict = {}
        # id_dict = {}
        # article_pos_list = []
        # for article in articles:
        #      #print(article.get_article_id())
        #      counter = 0
        #      #for word in article.get_inverted_index().keys():
        #       #   word_dict[word] = {}
        #      for word in article.get_inverted_index().keys():
        #          #print (article.get_inverted_index()[word])
        #          #id_dict = defaultdict(list)
        #          id_dict[article.get_article_id()].append(article.get_inverted_index()[word])
        #          #word_dict[word] = id_dict
        #          #print (article.get_article_id(), ", " + word +  ": ",  article.get_inverted_index()[word],  "/n")
        #          word_dict[word] = id_dict

        return word_dict

    @staticmethod
    def inverted_index_all_leon(articles):
        word_dict = {}

        list = []
        for article in articles:
            for word in article.get_inverted_index().keys():
                word_dict[word] = list
        for key in word_dict.keys():
            list = []
            tupel = ("articel_id", "list of positions")
            for article in articles:
                if key in article.get_inverted_index().keys():

                    tupel= (article.get_article_id(),article.get_inverted_index().get(key))

                    list.append(tupel)

                    #print(key,list)

            word_dict[key] = list

        return word_dict



