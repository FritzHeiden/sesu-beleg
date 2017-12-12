class Inverted:
    @staticmethod
    def inverted_File(articles):
        di = {}
        for article in articles:
            counter = 0
            for word in article.get_content().split():
                li = []
                di[word] = li
            for word in article.get_content().split():
                counter +=1
                a = (article.get_article_id(),counter)
                di[word].append(a)
        print(di)
        return di