from summercontest import pgInstance

table = pgInstance().all("SELECT * FROM suco", back_as=dict)
for participant in table:
    curr = pgInstance().one('SELECT * FROM increase WHERE handle=%(handle)s', {'handle': participant['handle']}, back_as=dict)
    score = participant['acmp'] + participant['timus'] * 2 + participant['cfdiv1'] * 10 + participant['cfdiv23'] * 5
    if curr:
        # exists
        pgInstance().run("UPDATE increase SET score=%(score)s WHERE handle=%(handle)s",
        {'handle': participant['handle'], 'score': score})
    else:
        # new
        pgInstance().run("INSERT INTO increase values(%(handle)s, %(score)s)",
        {'handle': participant['handle'], 'score': score})
