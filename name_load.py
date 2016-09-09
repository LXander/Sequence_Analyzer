


def get_gene_name():
    fr = open('./GeneName/GeneName.txt')
    fr.readline()
    geneName = []
    for name in fr.readlines():
        geneName.append(name.strip('\n'))
    return geneName

fr = open('./GeneName/gene_enhance.txt')
fr.readline()
name_list = []
name_dict = {}
for line in fr.readlines():
    syb,name = line.strip('\n').split('\t')[1:3]
    name_list.append(syb)
    name_list.append(name)
    name_dict[syb] = syb
    name_dict[name] = syb
