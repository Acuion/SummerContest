import json
import requests
from datetime import datetime
from flask import request
from bs4 import BeautifulSoup
from summercontest import app

BEGIN_JUNE = datetime.strptime('Jun 1 2018', '%b %d %Y')
END_AUGUST = datetime.strptime('Aug 31 2018', '%b %d %Y')

def getAcmpScore(idStr):
    prof = requests.get('http://acmp.ru/index.asp?main=user&id=' + idStr)
    soup = BeautifulSoup(prof.text, 'html.parser')
    acs = soup.select('.text')[0]
    acs = len(acs.select('a'))
    return acs

def getTimusScore(idStr):
    prof = requests.get('http://acm.timus.ru/author.aspx?id=' + idStr)
    soup = BeautifulSoup(prof.text, 'html.parser')
    acs = soup.select('.author_stats_value')[1]
    acs = acs.text.split(' ')[0]
    return int(acs) * 2

def getCodeforcesScore(handle):
    recentContests = requests.get('http://codeforces.com/contests') # yep, it is inefficient to load the page every time
    recentContestsList = BeautifulSoup(recentContests.text, 'html.parser').select('.datatable')[1].select('table')[0]
    matchingContests = []
    for tr in recentContestsList.select('tr'):
        cid = tr.get('data-contestid')
        if not cid:
            continue
        cdate = datetime.strptime(tr.select('.format-date')[0].text, '%b/%d/%Y %M:%S')
        if BEGIN_JUNE <= cdate <= END_AUGUST:
            matchingContests.append(cid)

    score = 0
    clist = requests.get('http://codeforces.com/contests/with/' + handle)
    userContestsList = BeautifulSoup(clist.text, 'html.parser').select('.user-contests-table')[0].select('tbody')[0]
    for tr in userContestsList.select('tr'):
        solved = int(tr.select('td')[3].text)
        linkId = tr.select('td')[1].select('a')[0]['href'].split('/')[2]

        if linkId not in matchingContests:
            continue

        globalContestStandings = requests.get('http://codeforces.com/contest/{}/standings'.format(linkId))
        div1Round = 'rated-user user-red' in globalContestStandings
        score += (10 if div1Round else 5) * solved
    return score

def getScores(acmpId, timusId, cfHandle):
    return {'acmp': getAcmpScore(acmpId), 'timus': getTimusScore(timusId), 'cf': getCodeforcesScore(cfHandle)}

@app.route("/scores")
def scoreApi():
    acmpId = request.args.get('acmp')
    timusId = request.args.get('timus')
    cfHandle = request.args.get('cf')
    if not acmpId or not timusId or not cfHandle:
        return 'Not enough arguments'
    return json.dumps(getScores(acmpId, timusId, cfHandle))

if __name__ == '__main__':
    print(getScores("186318", "214280", "Acuion"))
