import sys

from analyse.articles_analyser import ArticlesAnalyser
from analyse.counter import Counter
from analyse.min_hasher import MinHasher
from analyse.shingle_generator import ShingleGenerator
from analyse.stemmer import Stemmer
from analyse.text_analyser import TextAnalyser
from database.search_engine_database import SearchEngineDatabase
from network.url_helper import UrlHelper
from serialization.deserializer import Deserializer
from analyse.Similarity import Similarity

# data source
test_data_url = "http://daten.datenlabor-berlin.de/test.xml"
test_data_url = "http://daten.datenlabor-berlin.de/newspart1.xml"

# mongodb connection information
mongodb_host = "spadi8.f4.htw-berlin.de"
# mongodb_host = "localhost"
mongodb_port = 28018
mongodb_db_name = "search_engine"

# initialize database
database = SearchEngineDatabase(mongodb_host, mongodb_port)

file = open("./stop_words", "r")
text = file.read()
file.close()
text_split = text.split("\n")
stop_words = []
for line in text_split:
    if line.startswith(";") is False:
        stop_words.append(line.lower())

TextAnalyser.stop_words = stop_words
ShingleGenerator.stop_words = stop_words


def list_commands():
    column_width = 40
    print("= Command List =")
    print("{0}{1}".format("h/help".ljust(column_width), "List all available commands"))
    print("{0}{1}".format("l/list [<count> [<start_position>]]".ljust(column_width), "List a selection of articles"))
    print("{0}{1}".format("w/words <article_id>".ljust(column_width), "List occurrences of words of an article"))
    print("{0}{1}".format("sw/stopwords <article_id>".ljust(column_width),
                          "List occurrences of stop words of an article"))
    print("{0}{1}".format("t/top <top_count> <article_id>".ljust(column_width),
                          "List top n occurrences of stop words of an article"))
    print("{0}{1}".format("s/stats".ljust(column_width), "Show stats concerning all articles"))
    print("{0}{1}".format("p/persist <url>".ljust(column_width), "Persists articles from URL"))
    print("{0}{1}".format("q/quit".ljust(column_width), "Quit"))


def list_articles(count, start_position):
    try:
        count = int(count)
    except ValueError:
        count = 10

    try:
        start_position = int(start_position)
    except ValueError:
        start_position = 0

    if count is None or type(count) is not int:
        raise Exception("Invalid value for count")
    print("Showing articles {0} to {1}".format(start_position, start_position + count))
    for article in database.get_articles_range(start_position, start_position + count):
        print("id: {0}, version: {1}, date: {2}, source: {3}, title: {4}, url: {5}".format(
            article.get_article_id(), article.get_version(), article.get_date(), article.get_source(),
            article.get_title(), article.get_url()
        ))


def persist_articles(url):
    # download xml documents
    try:
        article_xml = UrlHelper.retrieve_url(url)
    except:
        print("Invalid URL '{0}'!".format(url))
        return

    # deserialize documents
    articles = Deserializer.deserialize_articles_xml(article_xml)

    for article in articles:
        if database.get_article(article.get_article_id()) is None:
            article = ArticlesAnalyser.analyse_article(article, database)

            # persist article in database
            print("New article added: id: {0}, version: {1}, date: {2}, source: {3}, title: {4}, url: {5}".format(
                article.get_article_id(), article.get_version(), article.get_date(), article.get_source(),
                article.get_title(), article.get_url()
            ))
            persist_inv_index(article)
            articles_statistic = ArticlesAnalyser.get_article_statistic(article)
            database.add_articles_statistic(articles_statistic)
        else:
            print("Article with id {0} already in database.".format(article.get_article_id()))


def list_words(article_id):
    article = database.get_article(article_id)
    words = article.get_words()
    for word in words:
        print("{0}: {1}".format(word, words[word]))


def list_stop_words(article_id):
    article = database.get_article(article_id)
    stop_words = article.get_stop_words()
    for stop_word in stop_words:
        print("{0}: {1}".format(stop_word, stop_words[stop_word]))


def list_top_words(top, article_id):
    try:
        top = int(top)
    except ValueError:
        print("Usage: top <top_count> <article_id>")

    article = database.get_article(article_id)
    words = article.get_words()
    top_words = Counter.top_words(words, top)
    for top_word in top_words:
        print("{0}: {1}".format(top_word, top_words[top_word]))


def list_stats():
    articles_statistic = database.get_articles_statistic()
    if articles_statistic is None:
        print("No statistics so far.")
        return

    print("= Articles Statistic =")
    article_count = articles_statistic.get_article_count()
    print("Article Count: {0}".format(article_count))
    print("Top 10 Sources:")
    sources = Counter.top_words(articles_statistic.get_sources(), 10)
    for source in sources:
        print("\t{0}: {1}".format(source, sources[source]))

    print("Top 100 Words:")
    words = Counter.top_words(articles_statistic.get_words(), 100)
    for word in words:
        print("\t{0}: {1}".format(word, words[word]))


def persist_inv_index():

    article_words = []
    #term_frequency = 0


    #for article in database.get_articles():
        #start word um dopplung zu vermeiden
    for article in database.get_articles_range(1,10):
        start_word = 0
        for word_a in article.get_stems():
            post = []
            start_word = start_word +1
            if word_a not in article_words:
                article_words.append(word_a)
                counter = 1
                for word_b in article.get_stems()[start_word:]:
                    if word_a == word_b:
                        counter = counter +1

                term_frequency = counter / len(article.get_stems())
                post.append(article.get_article_id())
                post.append(term_frequency)
                database.add_inverted_index(word_a, post)

def leon():
    #TRAINIERTES MODEL WIRD ERZEUGT
    articles = []
    for article in database.get_articles():
        articles.append(article)
    Similarity.train(articles)


    print(Similarity.similarity("füllen","felder"))

def emil():
    print(database.get_inverted_index(Stemmer.single_stem("Merkel")))

print("= Article Database =")
print("Enter h or help to list commands")

close_requested = False
while close_requested is not True:
    command = input("\n> ").lower().split()
    for i in range(len(command), 4):
        command.append("")

    if command[0] == "h" or command[0] == "help":
        list_commands()
    elif command[0] == "q" or command[0] == "quit":
        sys.exit(0)
    elif command[0] == "l" or command[0] == "list":
        list_articles(command[1], command[2])
    elif command[0] == "p" or command[0] == "persist":
        persist_articles(command[1])
    elif command[0] == "w" or command[0] == "words":
        list_words(command[1])
    elif command[0] == "sw" or command[0] == "stopwords":
        list_stop_words(command[1])
    elif command[0] == "t" or command[0] == "top":
        list_top_words(command[1], command[2])
    elif command[0] == "s" or command[0] == "stats":
        list_stats()
    elif command[0] == "leon":
        leon()
    elif command[0] == "inv":
        persist_inv_index()
    elif command[0] == "emil":
        emil()
    else:
        print("Unknown command '{0}'. Enter h or help for command list".format(command))
