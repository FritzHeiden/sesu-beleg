import sys
import math
import time

from threading import Thread

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
from analyse.bool_and import AND

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

file = open("./stop_words", "r", errors='ignore')
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


def find_articles(query):
    print("Finding articles for query '{0}':".format(query))
    andEvaluator = AND(database)
    articles = andEvaluator.AND(query)


def persist_articles(url):
    # download xml documents
    try:
        article_xml = UrlHelper.retrieve_url(url)
    except UnicodeDecodeError as e:
        print(e)
        # print("Invalid URL '{0}'!".format(url))
        return

    # deserialize documents
    articles = Deserializer.deserialize_articles_xml(article_xml)

    total_articles = len(articles)
    count = 0
    threads = []
    for article in articles:
        count += 1
        added = False
        while not added:
            if len(threads) < 5:
                thread = Thread(target=persist_article, args=(article, count, total_articles))
                thread.start()
                threads.append(thread)
                added = True
            else:
                for thread in threads:
                    if not thread.isAlive():
                        threads.remove(thread)
                time.sleep(1)


def persist_article(article, count, total_articles):
    if database.get_article(article.get_article_id()) is None:
        article = ArticlesAnalyser.analyse_article(article, database)

        # persist article in database
        print(
            "{0}/{1} ({2}%): New article added: id: {3}, version: {4}, date: {5}, source: {6}, title: {7}, url: {8}".format(
                count, total_articles, math.floor(count / total_articles * 10000) / 100, article.get_article_id(),
                article.get_version(), article.get_date(), article.get_source(),
                article.get_title(), article.get_url()
            ))

        database.insert_article(article)
        persist_inv_index(article)
        articles_statistic = ArticlesAnalyser.get_article_statistic(article)
        database.add_articles_statistic(articles_statistic)
    else:
        print("{0}/{1} ({2}%): Article with id {3} already in database.".format(
            count, total_articles, math.floor(count / total_articles * 10000) / 100, article.get_article_id()))


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


def persist_inv_index(article):
    persisted_words = []
    total_words = len(article.get_stems())
    for word in article.get_stems():
        if word in persisted_words:
            continue

        count = 0
        for other_word in article.get_stems():
            if word == other_word:
                count += 1
        tf = count / total_words
        post = {'article_id': article.get_article_id(), 'tf': tf}
        database.add_post(word, post)
        persisted_words.append(word)



        # for article in database.get_articles():
        # start word um dopplung zu vermeiden
        # for article in database.get_articles_range(1,10):
        #     start_word = 0
        #     for word_a in article.get_stems():
        #         post = []
        #         start_word = start_word +1
        #         if word_a not in article_words:
        #             article_words.append(word_a)
        #             counter = 1
        #             for word_b in article.get_stems()[start_word:]:
        #                 if word_a == word_b:
        #                     counter = counter +1
        #
        #             term_frequency = counter / len(article.get_stems())
        #             post.append(article.get_article_id())
        #             post.append(term_frequency)
        #             database.add_inverted_index(word_a, post)


def model_train():
    # TRAINIERTES MODEL WIRD ERZEUGT
    articles = []
    for article in database.get_articles():
        articles.append(article)
    Similarity.train(articles)

<<<<<<< HEAD
def leon():
    #print(Similarity.similarity("füllen","felder"))
=======

def leon():
    # print(Similarity.similarity("füllen","felder"))
>>>>>>> 48f0364341e5d7a38b9a7d187397230424a675da

    wortliste = ["eins", "zwei", "drei"]
    print(AND.AND(wortliste))


def emil():
    print(database.get_inverted_index(Stemmer.single_stem("matthia")))


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
    elif command[0] == "f" or command[0] == "find":
        query = ""
        for i in range(1, len(command)):
            query += command[i] + " "
        find_articles(query)
    elif command[0] == "s" or command[0] == "stats":
        list_stats()
    elif command[0] == "model_train":
        model_train()
    elif command[0] == "leon":
        leon()
    elif command[0] == "inv":
        persist_inv_index()
    elif command[0] == "emil":
        emil()
    else:
        print("Unknown command '{0}'. Enter h or help for command list".format(command))
