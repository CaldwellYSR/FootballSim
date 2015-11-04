#!/usr/bin/python

import nfldb as nfl 
import psycopg2

class Team_DB_Manager:

    def __init__(self):
        self.db = nfl.connect()
        self.q = nfl.Query(self.db)
        self.conn = psycopg2.connect(database="nfldb", user="nfldb", password="11me23MJ", host="127.0.0.1", port="5432")
        c = self.conn.cursor()
        c.execute("""
            SELECT team_id
            FROM team
        """)
        teams = c.fetchall()
        for team in teams:
            #self.field_goal_chance(team[0], db, q)
        self.conn.close()

    def field_goal_chance(self, team_name): 
        self.q.player(team=team_name)
        roster = self.q.as_aggregate()
        attempts = 0
        made = 0
        for stats in roster:
            attempts += stats.kicking_fga
            made += stats.kicking_fgm
        chance = ( float(made) / float(attempts) ) * 1000
        c = self.conn.cursor()
        c.execute("""
            INSERT INTO team_stats (team_name, stat_key, stat_value)
            VALUES ( %s, %s, %d ) """ % ( team_name, 'field_goal_chance', chance )
        )

   
    def create_table(self):
        print "Open DB"
        c = conn.cursor()
        c.execute("""
            CREATE TABLE team_stats
            ( stat_id    INT     PRIMARY KEY     NOT NULL,
              team_name  VARCHAR(5)              NOT NULL, 
              stat_key   VARCHAR(255)            NOT NULL,
              stat_value INT                     NOT NULL
            );
        """)
        print "Table Created"

        conn.commit()
        conn.close()

if __name__ == "__main__":
    tmp = Team_DB_Manager()
