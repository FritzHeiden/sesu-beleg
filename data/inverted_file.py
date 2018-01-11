class InvertedFile:
    def __init__(self, word, article_amount=None, inv_index=None):
        if inv_index is None:
            inv_index = {}
        if article_amount is None:
            article_amount = 0
        self._word = word
        self._article_amount = article_amount
        self._inv_index = inv_index

    def __str__(self) -> str:
        return "word:{0} | articels:{1} | index:{2}".format(self._word, self._article_amount, self._inv_index)

    def set_word(self, word):
        self._word = word

    def get_word(self):
        return self._word

    def set_article_amount(self, article_amount):
        self._article_amount = article_amount

    def get_article_amount(self):
        return self._article_amount

    def set_inv_index(self, inv_index):
        self._inv_index = inv_index

    def get_inv_index(self):
        return self._inv_index

    def add_article_index(self, article_id, index):
        if index is not None and article_id is not None:
            self._inv_index[article_id] = index
            self._article_amount = self._article_amount + 1

