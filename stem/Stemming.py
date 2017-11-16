from nltk.stem.porter import * # import des porter stemmers


class Stemmer:
    def Stemming(self,liste):
        stemmer = PorterStemmer() #erzeugen des Stemmers
        for i in range(0, len(liste)):  #durchgehen der uebergebenen liste
            liste[i] = stemmer.stem(liste[i])  #stemmen der liste
        return liste    #rueckgabe der liste


###### Ab Hier nur zum Testen
#b = ['caresses', 'flies', 'dies', 'mules', 'denied',
 #    'died', 'agreed', 'owned', 'humbled', 'sized',
  #   'meeting', 'stating', 'siezing', 'itemization',
   #  'sensational', 'traditional', 'reference', 'colonizer',
    # 'plotted']
#stem = Stemmer()
#stem.Stemming(b)
#print(b)
