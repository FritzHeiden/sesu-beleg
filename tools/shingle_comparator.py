class ShingleComparator:
    @staticmethod
    def compare_shingles(shingle1, shingle2):
        equal = True
        if len(shingle1) != len(shingle2):
            equal = False
        else:
            for i in range(0, len(shingle1)):
                element1 = shingle1[i]
                element2 = shingle2[i]
                if element1 != element2:
                    equal = False
                    break

        return equal
