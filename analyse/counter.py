from collections import OrderedDict


class Counter:
    @staticmethod
    def countArticles(articles):  # zählt die anzahl der articel
        return len(articles)

    @staticmethod
    def countWords(articles):  # nimmt jedes wort und zählt es
        di = {}
        for article in articles:  # durchlaufen der articel
            for word in article._content.split():  # durchlaufen der wörter im content der articel
                if di.get(word.lower()) == None:  # falls nicht vorhanden hinzufügen
                    di[word.lower()] = 1
                else:  # falls schon da +1
                    di[word.lower()] = di.get(str(word.lower())) + 1

        return di

    @staticmethod
    def topWords(di, number=100):  # gibt häufigsten wörter zurück, number = anzahl
        sortedDi = OrderedDict(sorted(di.items(), key=lambda t: t[1]))  # sortiert das angegebene dic
        dili = list(sortedDi.items())  # in liste umwandeln
        ausgabeDi = {}
        for i in range(1, number + 1):
            x, y = dili[i * -1]  # splitteen der liste in key=x and value=y
            ausgabeDi[x] = y  # fügt dem rückgabe dictionary mit dem key =x  gleich das value = y hinzu

        return ausgabeDi

    @staticmethod
    def count_article_sources(articles):
        source_counts = {}
        for article in articles:
            source_name = article.get_source()
            if source_name not in source_counts:
                source_counts[source_name] = 0
            source_counts[source_name] = source_counts[source_name] + 1

        return source_counts
