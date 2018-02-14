import math


class InvertedIndex:
    def __init__(self, searchEngineDatabase):
        self.searchEngineDatabase = searchEngineDatabase

    def get_term_frequency(self, word, article_id):
        # ToDo get term frequency from database
        pass

    def get_inverted_document_frequency(self, word):
        total_article_count = 1  # ToDo get total amount of articles
        article_containing_word_count = 1  # ToDo get amount of articles containing the given word
        return math.log(total_article_count / article_containing_word_count)
