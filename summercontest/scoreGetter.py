import requests
from bs4 import BeautifulSoup
from joblib import Parallel, delayed

def getAcmpComplexityDict():
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

def getTimusComplexityDict():
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

def getAcmpSolved(idStr, complexityDict):
    prof = requests.get('http://acmp.ru/index.asp?main=user&id=' + idStr)
    soup = BeautifulSoup(prof.text, 'html.parser')
    acs = soup.select('.text')[0]
    links = acs.select('a')
    acs = len(links)
    complexity101 = 0
    if acs > 100:
        ids = [link.getText() for link in links]
        sortedTasks = sorted(ids, key=lambda x: complexityDict[x], reverse=True)
        complexity101 = complexityDict[sortedTasks[100]]
    return acs, complexity101

def getTimusSolved(idStr, complexityDict):
    prof = requests.get('http://acm.timus.ru/author.aspx?id=' + idStr)
    soup = BeautifulSoup(prof.text, 'html.parser')
    statsTdsList = soup.select('.author_stats_value')
    if not statsTdsList:
        return 0
    acs = statsTdsList[1]
    acs = int(acs.text.split(' ')[0])
    complexity31 = 0
    if acs > 30:
        accsTds = soup.select('.accepted')
        ids = [td.getText() for td in accsTds]
        sortedTasks = sorted(ids, key=lambda x: complexityDict[x], reverse=True)
        complexity31 = complexityDict[sortedTasks[30]]
    return acs, complexity31

def processSmallSites(participant, acmpComplexityDict, timusComplexityDict):
    print('small sites for', participant['id'])
    participant['acmp'], acmp101sComplexity = getAcmpSolved(participant['acmp'], acmpComplexityDict)
    participant['timus'], timus31sComplexity = getTimusSolved(participant['timus'], timusComplexityDict)
    participant['power'] = acmp101sComplexity * timus31sComplexity
    return participant

def getSolved(groups):
    acmpComplexityDict = getAcmpComplexityDict()
    timusComplexityDict = getTimusComplexityDict()
    groups = Parallel(n_jobs=4)(delayed(processSmallSites)(participant, acmpComplexityDict, timusComplexityDict) for participant in groups)
    return groups
