from analyse.counter import Counter
from analyse.min_hasher import MinHasher
from analyse.shingle_generator import ShingleGenerator
from analyse.stemmer import Stemmer
from analyse.inverted import Inverted
from analyse.text_analyser import TextAnalyser
from data.articles_statistic import ArticlesStatistic



class ArticlesAnalyser:
    @staticmethod
    def get_article_statistic(article):
        return ArticlesAnalyser.get_articles_statistic([article])

    @staticmethod
    def get_articles_statistic(articles):
        sources = Counter.count_article_sources(articles)
        words = {}
        for article in articles:
            article_words = article.get_words()
            for word in article_words:
                if word in words:
                    words[word] = words[word] + article_words[word]
                else:
                    words[word] = article_words[word]

        article_count = len(articles)
        return ArticlesStatistic(sources, words, article_count)

    @staticmethod
    def get_duplicates(signatures, reference_signature):
        similar_signatures = []
        for signature in signatures:
            if reference_signature.compare_straps(signature) is not None:
                similar_signatures.append(signature)

        duplicates = {"80": [], "85": [], "90": []}
        for signature in similar_signatures:
            similar_values = []
            all_values = []
            for hash_id1 in signature.get_hash_ids():
                value1 = signature.get_hash_value(hash_id1)
                for hash_id2 in reference_signature.get_hash_ids():
                    value2 = reference_signature.get_hash_value(hash_id2)
                    if value1 == value2 and value1 not in similar_values:
                        similar_values.append(value1)
                    if value1 not in all_values:
                        all_values.append(value1)
                    if value2 not in all_values:
                        all_values.append(value2)
            similarity = len(similar_values) / len(all_values)

            if similarity < 0.8:
                continue
            elif 0.8 <= similarity < 0.85:
                duplicates["80"].append(signature.get_article_id())
            elif 0.85 <= similarity < 0.9:
                duplicates["85"].append(signature.get_article_id())
            elif 0.9 <= similarity:
                duplicates["90"].append(signature.get_article_id())
        return duplicates

    # simularity = 0.8
    # count = 0
    # duplicates = {}
    # http://mccormickml.com/2015/06/12/minhash-tutorial-with-python-code/ so wie ich das verstanden habe, müsste es so in der Art aussehen
    # kp ich versteh das mit den signaturen immer noch nicht, auch mit Folie und anderen quellen ...
    # for i in (0, len(signatures)):
    #     for a in (0, len(reference_signature)):
    #         if (signatures[i] == signatures[a]):
    #             count += 1
    # if (count / len(signatures) > simularity):
    #     duplicates.add(signatures.get_article_id)

    # ToDo dubletten erkennen. min. ein band aus den signaturen muss mit einem band der referenz signatur
    # übereinstimmen. dann jaccard ähnlichkeit bestimmen. bei > 80% eintrag in duplicates[80], bei > 85% eintrag
    # in duplicates[85] und bei > 90% eintrag in duplicates[90] (article id des duplikats)
    # siehe data.signature klasse

    # return {}

    @staticmethod
    def analyse_article(article=None, database=None):
        # analyse words from content and add them to the article object
        words = TextAnalyser.analyse_words(article.get_content())
        article.set_words(Counter.count_words(words))

        stop_words = TextAnalyser.analyse_stop_words(article.get_content())
        article.set_stop_words(Counter.count_words(stop_words))

        # create stems from words and add them to the article object
        article.add_stems(Stemmer.get_stems(words))

        #create inverted file
        article.set_inverted_index(Inverted.inverted_File(article))

        # Generate Shingles from stop words
        #shingles = ShingleGenerator.generate_stop_word_shingles(TextAnalyser.trim_text(article.get_content()), 5)

        # add shingles to shingle map in database
        #database.add_shingles(shingles)
        # get shingle map from database
        #shingles = database.get_shingle_ids(shingles)
        # get hash functions from database
        #hash_functions = database.get_hash_functions(200)

        # generate min hash signature for current documents shingles
        #reference_signature = MinHasher.generate_min_hash(article.get_article_id(), shingles, hash_functions)

        # get all min hash signatures
        #signatures = database.get_signatures()

        # determine duplicates
        #duplicates = ArticlesAnalyser.get_duplicates(signatures, reference_signature)
        #article.set_duplicates(duplicates)

        # add min hash signature of current document to signature index
        #database.add_signature(reference_signature)

        return article
