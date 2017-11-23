class Article:
    def __init__(self, article_id, version, content, date, source, title, url, words=None, stems=None, stop_words=None):
        if words is None:
            words = {}
        if stems is None:
            stems = []
        if stop_words is None:
            stop_words = {}
        self._article_id = article_id
        self._version = version
        self._content = content
        self._date = date
        self._source = source
        self._title = title
        self._url = url
        self._words = words
        self._stems = stems
        self._stop_words = stop_words


    def __str__(self) -> str:
        return "Article{{id: '{0}', version: '{1}', content: '{2}', " \
               "date: '{3}', source: '{4}', title: '{5}', url: '{6}', words: '{7}', stems: '{8}', stop_words: '{9}'}}" \
            .format(self._article_id, self._version, self._content, self._date, self._source, self._title, self._url,
                    self._words, self._stems, self._stop_words)

    def get_article_id(self):
        return self._article_id

    def set_article_id(self, article_id):
        self._article_id = article_id

    def get_version(self):
        return self._version

    def set_version(self, version):
        self._version = version

    def get_content(self):
        return self._content

    def set_content(self, content):
        self._content = content

    def get_date(self):
        return self._date

    def set_date(self, date):
        self._date = date

    def get_source(self):
        return self._source

    def set_source(self, source):
        self._source = source

    def get_title(self):
        return self._title

    def set_title(self, title):
        self._title = title

    def get_url(self):
        return self._url

    def set_url(self, url):
        self._url = url

    # adds a word to the list if its not already there
    # def add_word(self, word):
    #     if self._words.count(word.lower()) <= 0:
    #         self._words.append(word.lower())

    def get_words(self):
        return self._words

    def set_words(self, words):
        self._words = words

    # def add_words(self, words):
    #     for word in words:
    #         self.add_word(word)

    def get_stems(self):
        return self._stems

    def set_stems(self, stems):
        self._stems = stems

    def add_stem(self, stem):
        if self._stems.count(stem) <= 0:
            self._stems.append(stem)

    def add_stems(self, stems):
        for stem in stems:
            self.add_stem(stem)

    def set_stop_words(self, stop_words):
        self._stop_words = stop_words

    def get_stop_words(self):
        return self._stop_words
