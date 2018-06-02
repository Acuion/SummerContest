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

def procContestPages(contest, handle):
    offContestStandings = requests.get('http://codeforces.com/contest/{}/standings?showUnofficial=off'.format(contest))
    div1Round = 'rated-user user-red' in offContestStandings

    contestPagesGetter = BeautifulSoup(requests.get('http://codeforces.com/contest/{}/standings?showUnofficial=on'.format(contest)).text, 'html.parser')
    pagesCount = len(contestPagesGetter.select('.custom-links-pagination')[0].select('span'))

    div1, div23 = 0, 0

    for page in range(1, pagesCount + 1):
        print('page', page, 'from', pagesCount)
        contestPage = BeautifulSoup(requests.get('http://codeforces.com/contest/{}/standings/page/{}?showUnofficial=on'.format(contest, page)).text, 'html.parser')
        contestTable = contestPage.select('.standings')[0]
        for tr in contestTable.select('tr'):
            if 'participantid' not in tr.attrs:
                continue
            tds = tr.select('td')
            userInfo = tds[1]
            if 'Virtual participant' in userInfo.text:
                continue
            userName = userInfo.select('a')[0].text
            solved = 0
            for td in tds:
                if 'acceptedsubmissionid' in td.attrs:
                    solved += 1
            if handle == userName:
                if div1Round:
                    div1 += solved
                else:
                    div23 += solved
                return div1, div23
    return 0, 0

def getCodeforcesSolved(handle):
    # yep, it is inefficient to load the pages every time
    recentContestsList = BeautifulSoup(requests.get('http://codeforces.com/contests').text, 'html.parser').select('.datatable')[1].select('table')[0]
    matchingContests = []
    for tr in recentContestsList.select('tr'):
        cid = tr.get('data-contestid')
        if not cid:
            continue
        cdate = datetime.strptime(tr.select('.format-date')[0].text, '%b/%d/%Y %M:%S')
        if BEGIN_JUNE <= cdate <= END_AUGUST:
            matchingContests.append(cid)

    div1, div23 = 0, 0

    for contest in matchingContests:
        print('contest', contest)
        cdiv1, cdiv23 = procContestPages(contest, handle)
        div1 += cdiv1
        div23 += cdiv23

    return div1, div23

def getSolved(acmpId, timusId, cfHandle):
    div1, div23 = getCodeforcesSolved(cfHandle)
    return {'acmp': getAcmpSolved(acmpId), 'timus': getTimusSolved(timusId), 'cfdiv1': div1, 'cfdiv23': div23}

if __name__ == '__main__':
    print(getSolved("222131", "249543", "pholen"))
