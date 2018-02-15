class AND:
    def __init__(self, database):
        self.database = database

    def AND(self, word_list):
        index = [
            {
                "word": "eins",
                "posts": [{"article_id": 68485, "tf": 0.009464635}, {"article_id": 98674, "tf": 0.0084693}]
            },
            {
                "word": "zwei",
                "posts": [{"article_id": 68769, "tf": 0.00659684}, {"article_id": 68485, "tf": 0.009464635}]
            }
        ]

        ### ALTER INDEX#####################################################################################
        # index = {"eins": [15, 1, 2, 3, 4, 5, 8, 9, 12, 19], "zwei": [2, 3, 4, 5, 12, 19], "drei": {4, 5, 12, 3, 31, 42}}


        #start_liste = index[word_list[0]]
        #for word in word_list:
            #not_hit = []
            #for i in start_liste:
                #if i not in index[word]:
                    #not_hit.append(i)
        #gemeinsame = list(set(start_liste) - set(not_hit))
        #return gemeinsame

        #print(list(a.values())[1][0]['article_id'])
        #print(index[0].values())

        #word = list(a.values())[0]
        #articel_id  = list(a.values())[1][0]['article_id']
        ### ALTER INDEX#####################################################################################


        ### NEUER INDEX#####################################################################################
        start_list = []
        posts = self.database.get_posts(word_list.split()[0])
        for post in posts:
                start_list.append(post['article_id'])
        print(start_list)

        no_hit = []
        for word in word_list.split():
            compare_list = []
            posts = self.database.get_posts(word)
            for post in posts:
                compare_list.append(post['article_id'])
            print(compare_list)
            for element in start_list:
                if element not in compare_list:
                    no_hit.append(element)

        for element in start_list:
            if element not in no_hit:
                no_hit.append(element)

        print (no_hit)
        list = []
        return list
        ### NEUER INDEX#####################################################################################