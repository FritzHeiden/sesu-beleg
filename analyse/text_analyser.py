import re


class TextAnalyser:
    # specify which words we want to use using regex
    word_validation_regex = re.compile("[a-zA-Zä-üÄ-Ü]+")
    # specify what parts of words we want to cut off using regex
    trim_regex = re.compile("[^a-zA-Zä-üÄ-Ü-]")
    trim_text_regex = re.compile("[^a-zA-Zä-üÄ-Ü- ]")
    # define all words that are irrelevant
    stop_words = ["der", "die", "das", "ein", "eine", "aus", "dem", "mit", "bei", "von", "ist", "oder", "nun", "in",
                  "wie", "wir", "und", "ob", "to", "the", "zu", "ihr", "für", "nur", "vor", "im", "zur", "by", "um",
                  "als", "den", "einem"]

    # create an array of words from a text based on the specified criteria
    @staticmethod
    def analyse_words(text):
        if isinstance(text, str) is False:
            return []

        words = []
        # split text on spaces to get words
        text_split = text.split()
        for word in text_split:
            match = TextAnalyser.word_validation_regex.match(word)
            # if word matches our regex
            if match is not None:
                # cut off unwanted parts
                trimmed_word = re.sub(TextAnalyser.trim_regex, "", word)
                # do not use irrelevant words
                if not TextAnalyser.is_stop_word(trimmed_word):
                    words.append(trimmed_word)
        return words

    @staticmethod
    def analyse_stop_words(text):
        if isinstance(text, str) is False:
            return []
        
        stop_words = []
        text_split = text.split()
        for word in text_split:
            if TextAnalyser.is_stop_word(word.lower()):
                stop_words.append(word)

        return stop_words

    # evaluates if a given word is a stop word
    @staticmethod
    def is_stop_word(word):
        is_stop_word = False
        # see if the word is in the list of irrelevant words
        for stop_word in TextAnalyser.stop_words:
            if word.lower() == stop_word:
                is_stop_word = True
                break
        return is_stop_word

    @staticmethod
    def trim_text(text):
        try:
            text = re.sub(TextAnalyser.trim_text_regex, "", str(text))
        except:
            print("Failed to trim article.")
        return text
