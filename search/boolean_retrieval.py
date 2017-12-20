from analyse.text_analyser import TextAnalyser
from analyse.stemmer import Stemmer
import analyse
import re
class BooleanRetrieval:

    @staticmethod
    def bool_operator(text, articles, inverted_index, ):
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
    def AND (word_list, articles):




        find_article = []
        found_all_word_in_article = len(word_list)
        #for word in word_list:
        #   if TextAnalyser.is_stop_word(word.lower()):
        #        break;
        #Stemmer.get_stems(word_list)

        for article in articles:

            is_word_in_article_counter = 0
            for word in word_list:
                #print("lol")
                if word in article.get_stems():
                    is_word_in_article_counter += 1
                    if is_word_in_article_counter == found_all_word_in_article:
                        find_article.append(article.get_article_id())
        return find_article
    @staticmethod
    def OR (word_list, articles):
        find_article = []
        found_more_then_one_word = 1
        #for word in word_list:
        #    if TextAnalyser.is_stop_word(word.lower()):
        #        break;
        #Stemmer.get_stems(word_list)

        for article in articles:

            is_word_in_article_counter = 0
            counter= 0
            for word in word_list:
                counter += 1
                #print(len(word_list), ": ", counter)
                if word in article.get_stems():
                    is_word_in_article_counter += 1
                    #print (word, ": ", article.get_article_id(), "| ", is_word_in_article_counter)

                if counter == len(word_list) and is_word_in_article_counter == 1:
                    #print("lol")
                    find_article.append(article.get_article_id())
        return find_article

    def NEAR (word_list, articles, art_ids, near):#, inverted_index):
        find_article = []

        #for word in word_list:
         #   for art_id in art_ids:
          #      for pos in inverted_index[(word, art_id)]:



        for article in articles:
            #print(art_ids)
            for art_id in art_ids:
                #print(art_id, " : ", article.get_article_id())
                if art_id == article.get_article_id():
                    for word_a in word_list:
                        for word_b in word_list:
                            if word_a == word_b:
                                break
                            for pos_a in article.get_inverted_index()[word_a]:
                                for pos_b in article.get_inverted_index()[word_b]:
                                    if pos_a == pos_b:
                                        break
                                    current_near = abs(pos_a - pos_b)
                                    #print(word_a, "|", word_b, ": ", pos_a, ", ", pos_b, ";", current_near, ", ", near)

                                    if current_near <= near:
                                        find_article.append((article.get_article_id(), current_near))
                                        ## wahrscheinlich vieles überflüssig



        return find_article

    @staticmethod
    def AND_NOT(word_list, articles):
        find_article = []

      # for word in word_list:
      # if TextAnalyser.is_stop_word(word.lower()):
      # break;
      # Stemmer.get_stems(word_list)


        for article in articles:
            #print(article.get_stems())
            #print(word_list[0])
            #print(word_list[1])

            if word_list[0] in article.get_stems() and word_list[1] not in article.get_stems():
                find_article.append(article.get_article_id())


        return find_article