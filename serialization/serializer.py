class Serializer:
    @staticmethod
    def serialize_article_json(article):
        return {"article_id": article.get_article_id(),
                "version": article.get_version(),
                "content": article.get_content(),
                "date": article.get_date(),
                "source": article.get_source(),
                "title": article.get_title(),
                "url": article.get_url(),
                "words": article.get_words(),
                "stop_words": article.get_stop_words(),
                "stems": article.get_stems(),
                "duplicates": article.get_duplicates(),
                "inverted_index": article.get_inverted_index()}

    @staticmethod
    def serialize_articles_statistic(articles_statistic):
        return {"id": "articles_statistic",
                "sources": articles_statistic.get_sources(),
                "words": articles_statistic.get_words(),
                "article_count": articles_statistic.get_article_count()}

    @staticmethod
    def serialize_signature(signature):
        article_id = signature.get_article_id()
        signature = signature.get_signature()
        sig = {}
        for strap in signature:
            sig[str(strap)] = {}
            for hash in signature[strap]:
                sig[str(strap)][str(hash)] = signature[strap][hash]

        return {
            "article_id": article_id,
            "signature": sig
        }
