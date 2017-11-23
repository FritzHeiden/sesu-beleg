import re


class WordAnalyser:
    # specify which words we want to use using regex
    word_validation_regex = re.compile("[a-zA-Zä-üÄ-Ü]+")
    # specify what parts of words we want to cut off using regex
    trim_regex = re.compile("[^a-zA-Zä-üÄ-Ü-]")
    # define all words that are irrelevant
    stop_words = ["der", "die", "das", "ein", "eine", "aus", "dem", "mit", "bei", "von", "ist", "oder", "nun", "in",
                  "wie", "wir", "und", "ob", "to", "the", "zu", "ihr", "für", "nur", "vor", "im", "zur", "by", "um",
                  "als", "den", "einem"]

    # create an array of words from a text based on the specified criteria
    @staticmethod
    def analyse_words(text):
        words = []
        # split text on spaces to get words
        text_split = text.split()
        for word in text_split:
            match = WordAnalyser.word_validation_regex.match(word)
            # if word matches our regex
            if match is not None:
                # cut off unwanted parts
                trimmed_word = re.sub(WordAnalyser.trim_regex, "", word)
                # do not use irrelevant words
                if not WordAnalyser.is_stop_word(trimmed_word):
                    words.append(trimmed_word)
        return words

    # evaluates if a given word is a stop word
    @staticmethod
    def is_stop_word(word):
        is_stop_word = False
        # see if the word is in the list of irrelevant words
        for stop_word in WordAnalyser.stop_words:
            if word.lower() == stop_word:
                is_stop_word = True
                break
        return is_stop_word
