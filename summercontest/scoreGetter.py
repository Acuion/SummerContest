import requests
from bs4 import BeautifulSoup
from joblib import Parallel, delayed

def getAcmpSolved(idStr):
    prof = requests.get('http://acmp.ru/index.asp?main=user&id=' + idStr)
    soup = BeautifulSoup(prof.text, 'html.parser')
    acs = soup.select('.text')[0]
    acs = len(acs.select('a'))
    return acs

def getTimusSolved(idStr):
    prof = requests.get('http://acm.timus.ru/author.aspx?id=' + idStr)
    soup = BeautifulSoup(prof.text, 'html.parser')
    statsTdsList = soup.select('.author_stats_value')
    if not statsTdsList:
        return 0
    acs = statsTdsList[1]
    acs = acs.text.split(' ')[0]
    return int(acs)

def processSmallSites(participant):
    print('small sites for', participant['id'])
    participant['acmp'] = getAcmpSolved(participant['acmp'])
    participant['timus'] = getTimusSolved(participant['timus'])
    participant['power'] = 0 # TODO
    return participant

def getSolved(groups):
    groups = Parallel(n_jobs=4)(delayed(processSmallSites)(participant) for participant in groups)
    return groups
