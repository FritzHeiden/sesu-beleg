class MinHasher:
    @staticmethod
    def generate_min_hash(shingles, shingle_map, hash_function_parameters):
        # min hash dict
        min_hash = {}
        # ToDo min hash berechnen. jede hash funktion über die ids der übergebenen shingles aus der shingle map
        # kleinsten wert unter gleicher id im min hash speichern
        # (for hash { for shingle { hash(shingle ids) -> kleinster wert in min_hash[hash id] } }
        # hash funktion: h(x) = (a*x + b) % c

        return min_hash
