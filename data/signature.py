class Signature:
    def __init__(self, article_id, signature=None):
        if signature is None:
            signature = {}
        self._article_id = article_id
        self._signature = signature

    def add_hash_value(self, strap, hash_id, value):
        if strap not in self._signature:
            self._signature[strap] = {}

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

    def get_hash_ids(self):
        hash_ids = []
        for strap_id in self._signature:
            for hash_id in self._signature[strap_id]:
                hash_ids.append(hash_id)
        return hash_ids

    def compare_straps(self, signature):
        for strap_id in signature.get_signature():
            if strap_id not in self._signature:
                continue
            found = True
            for hash_id in self._signature[strap_id]:
                if hash_id not in signature.get_signature()[strap_id]:
                    found = False
                    break
                if self._signature[strap_id][hash_id] != signature.get_signature()[strap_id][hash_id]:
                    found = False
                    break
            if found:
                return strap_id

        return None
