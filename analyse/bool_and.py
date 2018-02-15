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
                "posts": [{"article_id": 68769, "tf": 0.00659684}]
            }
        ]
        # index = {"eins": [15, 1, 2, 3, 4, 5, 8, 9, 12, 19], "zwei": [2, 3, 4, 5, 12, 19], "drei": {4, 5, 12, 3, 31, 42}}
        start_liste = index[word_list[0]]
        for word in word_list:
            not_hit = []
            for i in start_liste:
                if i not in index[word]:
                    not_hit.append(i)

        # print(not_hit)
        # print(ergebnis_liste)
        gemeinsame = list(set(start_liste) - set(not_hit))

        return gemeinsame
