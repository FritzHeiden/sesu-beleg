class Signature:
    def __init__(self, article_id, signatures=None):
        if signatures is None:
            signatures = {}
        self._article_id = article_id
        self._signature = signatures

    def add_hash_value(self, strap, hash_id, value):
        self._signature[strap][hash_id] = value

    def get_hash_value(self, hash_id):
        for strap in self._signature:
            if hash_id in self._signature[strap]:
                return self._signature[strap][hash_id]

    def get_strap(self, strap_id):
        return self._signature[strap_id]

    def get_signature(self):
        return self._signature

    def get_article_id(self):
        return self._article_id
