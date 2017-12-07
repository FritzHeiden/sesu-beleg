import math

from data.signature import Signature


class MinHasher:
    @staticmethod
    def generate_min_hash(article_id, shingles, hash_functions):
        signature = Signature(article_id)

        for hash_function in hash_functions:
            min_value = None
            for shingle in shingles:
                if min_value is None:
                    min_value = hash_function.calculate(shingle["id"])
                else:
                    min_value = min(hash_function.calculate(shingle["id"]), min_value)
            signature.add_hash_value(math.floor((int(hash_function.get_id()) - 1) / 20), hash_function.get_id(), min_value)


        # ToDo min hash berechnen. jede hash funktion über die ids der übergebenen shingles aus der shingle map
        # kleinsten wert unter gleicher id im min hash speichern
        # (for hash { for shingle { hash(shingle ids) -> kleinster wert in min_hash[hash id] } }
        # hash_function.calculate(value)


        return signature



