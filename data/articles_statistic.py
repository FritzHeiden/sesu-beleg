class ArticlesStatistic:
    def __init__(self, source_counts):
        if source_counts is None:
            source_counts = {}
        self.__source_counts = source_counts

    def get_source_counts(self):
        return self.__source_counts

    def set_source_counts(self, source_counts):
        self.__source_counts = source_counts

    def update_source_count(self, source, count):
        self.__source_counts[source] = count

    def increase_source_count(self, source, count=1):
        self.__source_counts[source] = self.__source_counts[source] + count

    def get_source_count(self, source):
        return self.__source_counts[source]

    def __str__(self):
        return "ArticlesStatistic{{source_counts: {0}}}".format(self.get_source_counts())
