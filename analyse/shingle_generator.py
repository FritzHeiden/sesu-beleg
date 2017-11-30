
class ShingleGenerator:
    file = open("./stop_words", "r")
    text = file.read()
    file.close()
    text_split = text.split("\n")
    stop_words = []
    for line in text_split:
        if line.startswith(";") is False:
            stop_words.append(line.lower())

    @staticmethod
    def generate_stop_word_shingles(text, shingle_length):
        shingles = []
        word_zeiger = 0
        # ToDo ein array von shingles generieren, welche als erstes wort ein stoppwort haben
        # stoppwörter befinden sich als array in der variablen stop_words
        #print(ShingleGenerator.stop_words)
        #print(text.split(" "))
        for word in text.split(" "):
            for stop_word in ShingleGenerator.stop_words:
                if (word == stop_word):
                    #print(word)
                    ele = []
                    for i in range (0,shingle_length):
                        if(word_zeiger+shingle_length < len(text.split(" "))):
                            ele.append(text.split(" ")[word_zeiger+i])
                    shingles.append(ele)

            word_zeiger +=1
        #print (shingles)
        #print(len(shingles))
        return shingles