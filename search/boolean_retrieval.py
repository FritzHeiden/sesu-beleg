from analyse.text_analyser import TextAnalyser
from analyse.stemmer import Stemmer
import analyse
import re
class BooleanRetrieval:

    @staticmethod
    def bool_operator(text, articles):
        word_a = ""
        word_b = ""
        operator = ""
        near = 0
        number_of_operations = 0
        hit_articels = []
        counter = 0
        for word in text.upper().split(): #upper
            print(word)
            if counter == 0:
                if TextAnalyser.is_stop_word(word.lower()):
                    print("keine Stoppworte in die Suchanfrage")
                    break; # Anfrag/Methode beenden
                word_a = word


            elif counter == 1:
                if word == "NEAR":
                    operator = word
                    counter=0
                elif operator == "NEAR":
                    near = int(word)
                else:
                    operator = word


            elif counter == 2:
                if TextAnalyser.is_stop_word(word.lower()):
                    print("keine Stoppworte in die Suchanfrage")
                    break; # Anfrage/Methode beenden
                word_b = word
                search_words = [word_a, word_b]
                search_words = Stemmer.get_stems(search_words)
                print(word_a, word_b, search_words, operator)
                if operator == "AND":
                    hit_articels.append(BooleanRetrieval.AND(search_words, articles)) # wird nicht funktionieren
                elif operator == "XOR":
                    hit_articels.append(BooleanRetrieval.XOR(search_words, articles))
                elif operator == "OR":
                    hit_articels.append(BooleanRetrieval.OR(search_words, articles))
                elif operator == "NEAR":
                    art_ids = BooleanRetrieval.AND(search_words, articles)
                    hit_articels.append(BooleanRetrieval.NEAR(search_words, articles, art_ids, near))
                elif operator == "ANDNOT":
                    hit_articels.append(BooleanRetrieval.AND_NOT(search_words, articles))
                else:
                    print("falsches Format angegeben, bitte ’word_a OPERATOR word_b' angeben")

                    return  [[]]
                    break;

                number_of_operations +=1 #evtl auch berechnen?
                counter = 0

            else:
                print("COUNTER_FEHLER, da counter: ", counter)

            counter += 1



        return hit_articels

        #dict_for_merge_articles ={}
        #for article in hit_articels:
              #for id in article:


    @staticmethod
    def AND (word_list, search_indizes):
        ## absicherung falls gesuchtes wort = None einbauen!
        #hit_indizes = []
        hit_articles = {}
        final_hit = set()
        #for word in word_list:
        #    hit_indizes.append(database.get_inv_index(word))
        for hit_index in search_indizes: #ursprünglich hit_indizes
            for article_id in hit_index.get_inv_index().keys():
                if hit_articles.get(article_id) == None:
                    hit_articles[article_id] = 1
                else:
                    hit_articles[article_id] = hit_articles[article_id] + 1
        for hit_article in hit_articles:
            if hit_articles[hit_article] == len(word_list):
                final_hit.add(hit_article)
        return final_hit



        # find_article = []
        # found_all_word_in_article = len(word_list)
        # #for word in word_list:
        # #   if TextAnalyser.is_stop_word(word.lower()):
        # #        break;
        # #Stemmer.get_stems(word_list)
        #
        # for article in articles:
        #
        #     is_word_in_article_counter = 0
        #     for word in word_list:
        #         #print("lol")
        #         if word in article.get_stems():
        #             is_word_in_article_counter += 1
        #             if is_word_in_article_counter == found_all_word_in_article:
        #                 find_article.append(article.get_article_id())
        # return find_article
    @staticmethod
    def XOR (word_list, search_indizes):

        ## absicherung falls gesuchtes wort = None einbauen!
        #hit_indizes = []
        hit_articles = {}
        final_hit = set()
        #for word in word_list:
            #hit_indizes.append(database.get_inv_index(word))
        for hit_index in search_indizes:
            for article_id in hit_index.get_inv_index().keys():
                if hit_articles.get(article_id) == None:
                    hit_articles[article_id] = 1
                else:
                    hit_articles[article_id] = hit_articles[article_id] + 1
        for hit_article in hit_articles:
            if hit_articles[hit_article] == 1:
                final_hit.add(hit_article)
        return final_hit




        # find_article = []
        # found_more_then_one_word = 1
        # #for word in word_list:
        # #    if TextAnalyser.is_stop_word(word.lower()):
        # #        break;
        # #Stemmer.get_stems(word_list)
        #
        # for article in articles:
        #
        #     is_word_in_article_counter = 0
        #     counter= 0
        #     for word in word_list:
        #         counter += 1
        #         #print(len(word_list), ": ", counter)
        #         if word in article.get_stems():
        #             is_word_in_article_counter += 1
        #             #print (word, ": ", article.get_article_id(), "| ", is_word_in_article_counter)
        #
        #         if counter == len(word_list) and is_word_in_article_counter == 1:
        #             #print("lol")
        #             find_article.append(article.get_article_id())
        # return find_article

    def OR (word_list, search_indizes):
        ## absicherung falls gesuchtes wort = None einbauen!
        #hit_indizes = []
        hit_articles = set()
        #for word in word_list:
            #hit_indizes.append(database.get_inv_index(word))
        for hit_index in search_indizes:
            for article_id in hit_index.get_inv_index().keys():
                hit_articles.add(article_id)
        return hit_articles # ACHTUNG SET

    def NEAR (word_list, search_indizes, art_ids, near):#, inverted_index):

        ## absicherung falls gesuchtes wort = None einbauen!
        #hit_indizes = []
        hit_articles = {}
        start_word = 0
        #for word in word_list:
            #hit_indizes.append(database.get_inv_index(word))
        for hit_index_a in search_indizes:
            start_word = start_word + 1
            for art_id in art_ids:
                for pos_a in hit_index_a.get_inv_index()[art_id]:
                    for hit_index_b in search_indizes[start_word:]:
                        for pos_b in hit_index_b.get_inv_index()[art_id]:
                            current_near = abs(pos_a - pos_b)
                            if current_near <= near:
                                if hit_articles.get(art_id) == None:
                                    hit_articles[art_id] = []
                                hit_articles[art_id].append(current_near)
        return hit_articles #achtung dictionary wird zurückgegeben









        find_article = []

        #for word in word_list:
         #   for art_id in art_ids:
          #      for pos in inverted_index[(word, art_id)]:



        # for article in articles:
        #     #print(art_ids)
        #     for art_id in art_ids:
        #         #print(art_id, " : ", article.get_article_id())
        #         if art_id == article.get_article_id():
        #             for word_a in word_list:
        #                 for word_b in word_list:
        #                     if word_a == word_b:
        #                         break
        #                     for pos_a in article.get_inverted_index()[word_a]:
        #                         for pos_b in article.get_inverted_index()[word_b]:
        #                             if pos_a == pos_b:
        #                                 break
        #                             current_near = abs(pos_a - pos_b)
        #                             #print(word_a, "|", word_b, ": ", pos_a, ", ", pos_b, ";", current_near, ", ", near)
        #
        #                             if current_near <= near:
        #                                 find_article.append((article.get_article_id(), current_near))
        #                                 ## wahrscheinlich vieles überflüssig
        #
        #
        #
        # return find_article

    #@staticmethod
    #def AND_NOT(word_list, articles):
        # change_list = True
        # hit_indizes_and = []
        # hit_indizes_not = []
        # hit_articles = {}
        # for word in word_list:
        #     if word == "ANDNOT":
        #         change_list = False
        #     elif change_list == True:
        #         hit_indizes_and.append(database.get_inv_index(word))
        #     else:
        #         hit_indizes_not.append(database.get_inv_index(word))
        #
        # for hit_index_and in hit_indizes_and:
        #     for article_id in hit_index_and.get_inv_index().keys():
        #         for hit_index
        #         if hit_articles.get(article_id) == None:
        #             hit_articles[article_id] = 1
        #         else:
        #             hit_articles[article_id] = hit_articles[article_id] + 1
        # return hit_articles.keys()

      #   find_article = []
      #
      # # for word in word_list:
      # # if TextAnalyser.is_stop_word(word.lower()):
      # # break;
      # # Stemmer.get_stems(word_list)
      #
      #
      #   for article in articles:
      #       #print(article.get_stems())
      #       #print(word_list[0])
      #       #print(word_list[1])
      #
      #       if word_list[0] in article.get_stems() and word_list[1] not in article.get_stems():
      #           find_article.append(article.get_article_id())
      #
      #
      #   return find_article