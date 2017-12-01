from collections import OrderedDict

import math

from data.signature import Signature


class MinHasher:
    @staticmethod
    def generate_min_hash(article_id, shingles, hash_functions):
        signature = Signature(article_id)
        ordered_shingles = OrderedDict(sorted(shingles.items()))

        for hash_function in hash_functions:
            min_value = hash_function.calculate(int(next(iter(ordered_shingles))))
            for shingle_id in ordered_shingles:
                min_value = min(hash_function.calculate(int(shingle_id)), min_value)
            signature.add_hash_value(math.floor((int(hash_function.get_id()) - 1) / 20), hash_function.get_id(), min_value)


        # ToDo min hash berechnen. jede hash funktion über die ids der übergebenen shingles aus der shingle map
        # kleinsten wert unter gleicher id im min hash speichern
        # (for hash { for shingle { hash(shingle ids) -> kleinster wert in min_hash[hash id] } }
        # hash_function.calculate(value)


        return signature
