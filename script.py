#!/usr/bin/python

import nfldb as nfl

db = nfl.connect()
q = nfl.Query(db)
q.player(team="MIA")
roster = q.as_aggregate()
for stats in roster:
    print stats
