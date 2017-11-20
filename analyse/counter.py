

class Counter:

    @staticmethod
    def countArticles(articles):
            return len(articles)

    @staticmethod
    def countWords(articles):
        di = {}
        for article in articles:
            for word in article._content.split():
                if di.get(word) == None:
                    di[word] = 1
                else:
                    di[word] = di.get(str(word)) + 1

        return di



#di[word] = 1
 #               for word in article._content.split():
  #                  di[word] = di.get(str(word)) + 1