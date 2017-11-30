class Signature:
    def __init__(self, article_id):
        self.article_id = article_id
        self.signature = {}

    def add_hash_value(self, strap, hash_id, value):
        self.signature[strap][hash_id] = value

    def get_hash_value(self, hash_id):
        for strap in self.signature:
            if hash_id in self.signature[strap]:
                return self.signature[strap][hash_id]

    def get_strap(self, strap_id):
        return self.signature[strap_id]
