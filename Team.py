#!/usr/bin/python

import nfldb as nfl

class Team:

    def __init__(self, name = "Team", short_name = "UNK", year = 2009):
        self.name = name
        self.short_name = short_name
        self.possession = False
        self.year = year
        self.db = nfl.connect()
        self.q = nfl.Query(self.db)
        self.q.player(team=short_name)
        self.roster = self.q.as_aggregate()
        print self.name

    # TODO use team statistics to determine these values
    def false_start_chance(self):
        return 2

    def field_goal_chance(self):
        attempts = 0
        made = 0
        for stats in self.roster:
            attempts += stats.kicking_fga
            made += stats.kicking_fgm
        return ( float(made) / float(attempts) ) * 1000

    def running_play_chance(self):
        return 550

    def fumble_chance(self):
        return 6

    def tackle_for_loss_chance(self):
        return 16

    def long_run_chance(self):
        return 30

    def sack_chance(self):
        return 5

    def interception_chance(self):
        return 20

    def catch_chance(self):
        return 65
