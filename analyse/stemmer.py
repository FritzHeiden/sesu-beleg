from nltk.stem.porter import *  # import des porter stemmers


class Stemmer:
    @staticmethod
    def get_stems(list):
        stemmer = PorterStemmer()  # erzeugen des Stemmers
        for i in range(0, len(list)):  # durchgehen der uebergebenen liste
            list[i] = stemmer.stem(list[i])  # stemmen der liste
        return list  # rueckgabe der liste

    @staticmethod
    def get_shingle_stems(shingles):
        for shingle in shingles:
            shingle = Stemmer.get_stems(shingle)
        return shingles

###### Ab Hier nur zum Testen
# b = ['caresses', 'flies', 'dies', 'mules', 'denied',
#    'died', 'agreed', 'owned', 'humbled', 'sized',
#   'meeting', 'stating', 'siezing', 'itemization',
#  'sensational', 'traditional', 'reference', 'colonizer',
# 'plotted']
# stem = Stemmer()
# stem.Stemming(b)
# print(b)
