
def get_gene_name():
    fr = open('./GeneName/GeneName.txt')
    fr.readline()
    geneName = []
    for name in fr.readlines():
        geneName.append(name.strip('\n'))
    return geneName