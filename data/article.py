class Article:

    def __init__(self, id, version, content, date, source, title, url):
        self._id = id
        self._version = version
        self._content = content
        self._date = date
        self._source = source
        self._title = title
        self._url = url
        self._words = []

    def __str__(self) -> str:
        return "Article{{id: '{0}', version: '{1}', content: '{2}', " \
               "date: '{3}', source: '{4}', title: '{5}', url: '{6}'}}"\
            .format(self._id, self._version, self._content, self._date, self._source, self._title, self._url)

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._id = id

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

    def add_word(self, word):
        if self._words.count(word.lower()) <= 0:
            self._words.append(word.lower())

    def get_words(self):
        return self._words

    def set_words(self, words):
        self._words = words

    def add_words(self, words):
        for word in words:
            if self._words.count(word.lower()) <= 0:
                self._words.append(word.lower())
