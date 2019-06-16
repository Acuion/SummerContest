from summercontest import pgInstance

table = pgInstance().all("SELECT * FROM suco", back_as=dict)
highestScore = 0
bestParticipants = []
for participant in table:
    print('processing', participant['handle'])
    curr = pgInstance().one('SELECT * FROM daily WHERE handle=%(handle)s', {'handle': participant['handle']}, back_as=dict)
    if curr:
        scoreDiff = participant['acmp'] + participant['timus'] * 2 + participant['cfdiv1'] * 10 + participant['cfdiv23'] * 5 - curr['acmp'] - curr['timus'] * 2 - curr['cfdiv1'] * 10 - curr['cfdiv23'] * 5
        print(participant['acmp'], participant['timus'], participant['cfdiv1'], participant['cfdiv23'], curr['acmp'], curr['timus'], curr['cfdiv1'], curr['cfdiv23'])
        print(scoreDiff)
        if participant['handle'] != 'borisshapa' and scoreDiff > highestScore: # omg rewrite me
            highestScore = scoreDiff
            bestParticipants = []
            print('new top')
        if participant['handle'] != 'borisshapa' and scoreDiff == highestScore:
            bestParticipants.append({'handle': participant['handle'], 'rockets': curr['rockets']})
            print(bestParticipants)
        # exists
        pgInstance().run("UPDATE daily SET acmp=%(acmp)s, timus=%(timus)s, cfdiv1=%(cfdiv1)s, cfdiv23=%(cfdiv23)s WHERE handle=%(handle)s",
        {'handle': participant['handle'], 'acmp': participant['acmp'], 'cfdiv1': participant['cfdiv1'], 'cfdiv23': participant['cfdiv23'], 'timus': participant['timus']})
    else:
        # new
        pgInstance().run("INSERT INTO daily values(%(handle)s, %(acmp)s, %(timus)s, %(cfdiv1)s, %(cfdiv23)s, 0)",
        {'handle': participant['handle'], 'acmp': participant['acmp'], 'cfdiv1': participant['cfdiv1'], 'cfdiv23': participant['cfdiv23'], 'timus': participant['timus']})
if len(bestParticipants) == 1:
    print(bestParticipants)
    pgInstance().run("UPDATE daily SET rockets=%(rockets)s WHERE handle=%(handle)s",
    {'handle': bestParticipants[0]['handle'], 'rockets': bestParticipants[0]['rockets'] + 1})
