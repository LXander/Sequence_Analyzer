import random
import json



class var_gen:
    def __init__(self):
        self.Alleles = ['A','C','G','T']
        self.cursor = 1
        self.var_max_len = 10
        self.var_max_gap = 2000
        self.var_min_gap = 100
        self.var_max_num = 20


    def allele_gen(self,length):
        allele = ''
        for i in range(length):
            pos = random.randint(1,len(self.Alleles)-1)
            allele+=self.Alleles[pos]
        return allele

    def var_gen(self):
        var = {}
        var_len = random.randint(1,self.var_max_len)
        var['start'] = self.cursor
        self.cursor += var_len
        var['end'] = self.cursor
        var['observedAllele'] = self.allele_gen(var_len)

        ref = self.allele_gen(var_len)
        while ref==var['observedAllele']:
            ref = self.allele_gen(var_len)

        var['referenceAllele'] = ref
        var_gap = random.randint(self.var_min_gap,self.var_max_gap)
        self.cursor += var_gap
        return var

    def vars_gen(self):
        self.__init__()
        var_num = random.randint(1,self.var_max_num)
        vars = []
        for i in range(var_num):
            vars.append(self.var_gen())
        return vars



if __name__ == '__main__':
    gen = var_gen()
    print (json.dumps(gen.vars_gen(),indent=4))