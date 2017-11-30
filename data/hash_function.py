class HashFunction:
    def __init__(self, hash_id, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.id = hash_id

    def calculate(self, value):
        return (self.a * value + self.b) % self.c

    def get_id(self):
        return self.id

    def set_id(self, hash_id):
        self.id = hash_id
