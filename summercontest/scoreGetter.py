import requests
from datetime import datetime
from bs4 import BeautifulSoup

BEGIN_JUNE = datetime.strptime('Jun 1 2018', '%b %d %Y')
END_AUGUST = datetime.strptime('Aug 31 2018', '%b %d %Y')

def getAcmpSolved(idStr):
    prof = requests.get('http://acmp.ru/index.asp?main=user&id=' + idStr)
    soup = BeautifulSoup(prof.text, 'html.parser')
    acs = soup.select('.text')[0]
    acs = len(acs.select('a'))
    return acs

def getTimusSolved(idStr):
    prof = requests.get('http://acm.timus.ru/author.aspx?id=' + idStr)
    if 'No problems solved' in prof.text:
        return 0
    soup = BeautifulSoup(prof.text, 'html.parser')
    acs = soup.select('.author_stats_value')[1]
    acs = acs.text.split(' ')[0]
    return int(acs)

def procContestPages(contest, groups):
    offContestStandings = requests.get('http://codeforces.com/contest/{}/standings?showUnofficial=off'.format(contest))
    div1Round = 'rated-user user-red' in offContestStandings

    contestPagesGetter = BeautifulSoup(requests.get('http://codeforces.com/contest/{}/standings?showUnofficial=on'.format(contest)).text, 'html.parser')
    pagesCount = len(contestPagesGetter.select('.custom-links-pagination')[0].select('span'))

    for page in range(1, pagesCount + 1):
        print('page', page, 'from', pagesCount)
        contestPage = BeautifulSoup(requests.get('http://codeforces.com/contest/{}/standings/page/{}?showUnofficial=on'.format(contest, page)).text, 'html.parser')
        contestTable = contestPage.select('.standings')[0]
        for tr in contestTable.select('tr'):
            if 'participantid' not in tr.attrs:
                continue
            tds = tr.select('td')
            userInfo = tds[1]
            if 'Virtual participant' in userInfo.text or tds[0].text.isspace():
                continue
            userName = userInfo.select('a')[0].text
            solved = 0
            for td in tds:
                if 'acceptedsubmissionid' in td.attrs:
                    solved += 1
            for participant in groups:
                if participant['cf'] == userName:
                    print('found cf', participant['cf'])
                    if div1Round:
                        participant['cfdiv1'] += solved
                    else:
                        participant['cfdiv23'] += solved

def getCodeforcesSolved(groups):
    for participant in groups:
        participant['cfdiv1'] = 0
        participant['cfdiv23'] = 0

    recentContestsList = BeautifulSoup(requests.get('http://codeforces.com/contests').text, 'html.parser').select('.datatable')[1].select('table')[0]
    matchingContests = []
    for tr in recentContestsList.select('tr'):
        cid = tr.get('data-contestid')
        if not cid:
            continue
        cdate = datetime.strptime(tr.select('.format-date')[0].text, '%b/%d/%Y %M:%S')
        if BEGIN_JUNE <= cdate <= END_AUGUST:
            matchingContests.append(cid)

    for contest in matchingContests:
        print('contest', contest)
        procContestPages(contest, groups)

def getSolved(groups):
    getCodeforcesSolved(groups)
    for participant in groups:
        print('small sites for', participant['cf'])
        participant['acmp'] = getAcmpSolved(participant['acmp'])
        participant['timus'] = getTimusSolved(participant['timus'])
    return groups
