from data.signature import Signature
import numpy as np

class MinHasher:


    #nicht getestet - läuft wahrscheinlich nicht
    @staticmethod
    def generate_min_hash(shingles, hash_functions):

        #np.asarray(shingles)
        # min hash dict
        #min_hash = []

        strep_id = 1
        strep_size = 10
        biggest_value = 0
        signature_params = list
        current_signature = Signature
        article_id = 0 #??????????



        # ToDo min hash berechnen. jede hash funktion über die ids der übergebenen shingles aus der shingle map




        for hash in hash_functions:
            if hash%strep_size == 0:
                strep_id += 1
            tmp_value = 0
            for shingle in shingles:
                tmp_value = hash.calculate(shingles(shingle))
                if tmp_value > biggestValue:
                    biggestValue = tmp_value
                    signature_params[strep_id][hash.getid()] = biggestValue

        current_signature = (article_id, signature_params)






        # kleinsten wert unter gleicher id im min hash speichern
        # (for hash { for shingle { hash(shingle ids) -> kleinster wert in min_hash[hash id] } }
        # hash_function.calculate(value)

        return current_signature
