import re


class WordAnalyser:
    word_validation_regex = re.compile("[a-zA-Zä-üÄ-Ü]+")
    trim_regex = re.compile("[^a-zA-Zä-üÄ-Ü-]")
    stop_words = ["der", "die", "das", "ein", "eine", "aus", "dem", "mit", "bei", "von", "ist", "oder", "nun", "in",
                  "wie", "wir", "und", "ob", "to", "the", "zu", "ihr", "für", "nur", "vor", "im", "zur", "by", "um",
                  "als", "den", "einem"]

    @staticmethod
    def analyse_words(text):
        words = []
        text_split = text.split()
        for word in text_split:
            match = WordAnalyser.word_validation_regex.match(word)
            if match is not None:
                trimmed_word = re.sub(WordAnalyser.trim_regex, "", word)
                if not WordAnalyser.is_stop_word(trimmed_word):
                    words.append(trimmed_word)

        return words

    @staticmethod
    def is_stop_word(word):
        is_stop_word = False
        for stop_word in WordAnalyser.stop_words:
            if word.lower() == stop_word:
                is_stop_word = True
                break
        return is_stop_word