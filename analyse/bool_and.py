class AND:
    @staticmethod
    def AND(word_list):
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
        dic_list = [] #liste Aller Dicts die auch in Wortliste vorhanden sind
        for word in word_list:
            for dict in index:
                if word == list(dict.values())[0]:
                    dic_list.append(dict)
        #print(dic_list)

        start_liste = [] # liste aller Artikel in denen das erste Wort aus wortliste vorkommt
        for i in range(0, len(list(dic_list[0].values())[1])):
            start_liste.append(list(dic_list[0].values())[1][i]['article_id'])
        #print(start_liste)
        no_hit = [] # liste aller Artikel die zwar im ersten Wort vorkommen aber dannach nicht immer
        for i in range (0,len(dic_list)):
            vergleichs_liste = [] # liste aller weiteren wörter aus der Wortliste wird mit der startliste verglichen
            for x in range(0, len(list(dic_list[i].values())[1])):
                vergleichs_liste.append(list(dic_list[i].values())[1][x]['article_id'])
            #print (vergleichs_liste)
            for element in start_liste:
                if element not in vergleichs_liste:
                    no_hit.append(element)

        gemeinsame = list(set(start_liste) - set(no_hit)) # liste aller gemeinsamer artikeln
        return gemeinsame
        ### NEUER INDEX#####################################################################################