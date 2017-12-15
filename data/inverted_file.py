class InvertedFile:
    def __init__(self, word, inv_index=None):
        if inv_index is None:
            inv_index = {}
        self._word = word
        self._inv_index = inv_index

    def __str__(self) -> str:
        return "{0}:{{1}}".format(self._word, self._article_ids)

    def set_word(self, word):
        self.__word = word

    def get_word(self):
        return self.__word


    def set_inv_index(self, inv_index):
        self._inv_index = inv_index

    def get_inv_index(self):
        return self._inv_index