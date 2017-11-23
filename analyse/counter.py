from collections import OrderedDict


class Counter:
    @staticmethod
    def count_articles(articles):  # zählt die anzahl der articel
        return len(articles)

    @staticmethod
    def count_words(words):  # nimmt jedes wort und zählt es
        di = {}
        for word in words:  # durchlaufen der wörter im content der articel
            if di.get(word.lower()) == None:  # falls nicht vorhanden hinzufügen
                di[word.lower()] = 1
            else:  # falls schon da +1
                di[word.lower()] = di.get(str(word.lower())) + 1

        return di

    @staticmethod
    def top_words(di, number=100):  # gibt häufigsten wörter zurück, number = anzahl
        if len(di) < number:
            number = len(di)
        sortedDi = OrderedDict(sorted(di.items(), key=lambda t: t[1]))  # sortiert das angegebene dic
        dili = list(sortedDi.items())  # in liste umwandeln
        ausgabeDi = {}
        for i in range(1, number + 1):
            x, y = dili[i * -1]  # splitteen der liste in key=x and value=y
            ausgabeDi[x] = y  # fügt dem rückgabe dictionary mit dem key =x  gleich das value = y hinzu

        return ausgabeDi

    @staticmethod
    def count_article_sources(articles):
        sources = {}
        for article in articles:
            source = article.get_source()
            if source not in sources:
                sources[source] = 0
            sources[source] = sources[source] + 1

        return sources
