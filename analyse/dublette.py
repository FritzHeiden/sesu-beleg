class Dublette:

    @staticmethod
    def shingledublette(array1,array2):
        count = 0
        for shingle in array1:
            if shingle in array2:
                count += 1
        #if count/len(array1)>=0.2:
        print(count/len(array1))