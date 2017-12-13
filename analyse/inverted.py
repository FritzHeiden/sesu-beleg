from analyse.stemmer import Stemmer

class Inverted:
    @staticmethod
    def inverted_File(article):
        di = {}
        counter = 0
        wort_liste = []
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