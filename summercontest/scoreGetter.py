import requests
from bs4 import BeautifulSoup
from joblib import Parallel, delayed

def acmpComplexityDict():
    pagesSrc = requests.get('http://acmp.ru/index.asp?main=tasks')
    soup = BeautifulSoup(pagesSrc.text, 'html.parser')
    result = {}
    pageLinks = ['http://acmp.ru/' + pageLink['href'] for pageLink in soup.select('.small')]
    pageLinks.append('http://acmp.ru/index.asp?main=tasks&str=%20&page=0&id_type=0')
    for pageLink in pageLinks:
        print('Procssing acmp page', pageLink)
        prof = requests.get(pageLink)
        soup = BeautifulSoup(prof.text, 'html.parser')
        rows = soup.select('.white')
        for row in rows:
            tds = row.select('td')
            result[str(int(tds[0].getText()))] = int(tds[4].getText().strip()[:-1])
    return result

def timusComplexityDict():
    print('Processing timus page')
    prof = requests.get('http://acm.timus.ru/problemset.aspx?space=1&page=all&skipac=False&sort=difficulty')
    soup = BeautifulSoup(prof.text, 'html.parser')
    rows = soup.select('.content')
    result = {}
    for row in rows:
        tds = row.select('td')
        if not tds:
            continue # header
        result[tds[1].getText()] = int(tds[5].getText())
    return result

def getAcmpSolved(idStr):
    prof = requests.get('http://acmp.ru/index.asp?main=user&id=' + idStr)
    soup = BeautifulSoup(prof.text, 'html.parser')
    acs = soup.select('.text')[0]
    links = acs.select('a')
    acs = len(links)
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
    participant['acmp'], acmp101sComplexity = getAcmpSolved(participant['acmp'])
    participant['timus'], timus31sComplexity = getTimusSolved(participant['timus'])
    participant['power'] = acmp101sComplexity * timus31sComplexity
    return participant

def getSolved(groups):
    groups = Parallel(n_jobs=4)(delayed(processSmallSites)(participant) for participant in groups)
    return groups

print(acmpComplexityDict())