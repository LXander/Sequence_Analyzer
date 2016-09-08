import requests
import xml.etree.cElementTree as ET

def retrive_id_by_name(name):
    db = 'gene'
    based = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
    url = based + 'esearch.fcgi?db=%s&term=%s'%(db,name)
    r = requests.get(url)
    tree = ET.fromstring(r.text)
    IDList = map(lambda x: x.text, tree.find('IdList'))
    return list(IDList)

def get_region(idlist):
    set_flag = False
    if len(idlist) == 1:
        set_flag = False
    else:
        set_flag = True

    id = ','.join(idlist)
    db = 'gene'
    based = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
    url = based + 'esummary.fcgi?db=%s&id=%s'%(db,id)
    r = requests.get(url)
    tree = ET.fromstring(r.text)
    LocSet = tree.find('DocumentSummarySet').find('DocumentSummary').find('LocationHist')
    RegionDict = []
    for Loc in LocSet:
        LocDict = {}
        for _ in Loc:
            LocDict[_.tag] = _.text
        RegionDict.append(LocDict)
        
    return RegionDict

def get_geneDicts(name):
    IDList = retrive_id_by_name(name)
    geneDicts = get_region(IDList)
    return geneDicts