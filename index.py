#!bin/bash

import StackFSM as FSM
import random as R
import Scoreboard as S
import Team as T
from math import ceil

class Game:
    def __init__(self):
        self.fsm = FSM.StateMachine()
        self.scoreboard = S.Scoreboard()
        print()
        print("<p>===== New Game =====</p>")
        print()
        self.home_team = T.Team("Miami Dolphins", "MIA")
        self.away_team = T.Team("New England Patriots", "NE")
        self.offense = self.home_team
        self.defense = self.away_team
        self.offense.possession = True
        self.scoreboard.home_possession = self.home_team.possession
        print("<p>The {:s} have the ball at their own 20 yard line.</p>".format(self.offense.name))
    
    def describe_down(self, args):
        yard = "<p>< </p>"+str(self.scoreboard.yardline) if self.scoreboard.yardline < 50 else str(100 - self.scoreboard.yardline)+"<p> ></p>"
        print("<p>Down: {:d} Distance: {:d} Yardline: {:s}</p>".format( self.scoreboard.down, self.scoreboard.distance, yard))
        return ("Formation", args)

    def _move_ball(self, yds):
        self.scoreboard.distance -= yds
        self.scoreboard.yardline += yds

    def _first_down(self):
        self.scoreboard.down = 1
        self.scoreboard.distance = 10

    def swap_possession(self, args):
        print("<p>The {:s} take over at the {:d} yard line</p>".format(self.defense.name, self.scoreboard.yardline))
        tmp = self.offense
        self.offense = self.defense
        self.defense = tmp
        self.offense.possession = False
        self.defense.possession = True
        return ("Check Time", args)

    def formation(self, args):
        value = R.randrange(0, 100)
        falseStart = self.offense.false_start_chance()
        if value < falseStart:
            print("<p>False Start on the Offense!</p>")
            if self.scoreboard.yardline - 10 > 0:
                self._move_ball(-10)
            else:
                tmp = self.scoreboard.yardline
                self.scoreboard.yardline -= ceil(self.scoreboard.yardline / 2.0)
                self.scoreboard.distance += tmp - self.scoreboard.yardline
            return ("Check Time", args)
        else:
            if self.scoreboard.down == 4:
                if (self.scoreboard.yardline >= 60):
                    return ("Field Goal", args)
                else:
                    return ("Punt", args)
            else:
                return ("Quaterback Has Ball", args)

    def punt(self, args):
        print("<p>Punt!</p>")
        self.scoreboard.yardline = 100 - (self.scoreboard.yardline + 40)
        if self.scoreboard.yardline <= 0:
            print("<p>Touchback!</p>")
            self.scoreboard.yardline = 20
            
        self._first_down()
        return ("Swap Possession", args)

    def field_goal(self, args):
        print("<p>{:d} Yard Field Goal!</p>".format((100 - self.scoreboard.yardline) + 7))
        value = R.randrange(0, 100)
        made = self.offense.field_goal_chance()
        if value < made:
            print("<p>It's good!</p>")
            if self.scoreboard.home_possession:
                self.scoreboard.h_score += 3
            else:
                self.scoreboard.a_score += 3
            self.scoreboard.yardline = 20
            self.scoreboard.scored = True
        else:
            print("<p>No good!</p>")
            self.scoreboard.yardline = 100 - self.scoreboard.yardline

        self._first_down()
        return ("Swap Possession", args)

    def qb_has_ball(self, args):
        value = R.randrange(0, 1000)
        running = self.offense.running_play_chance()
        if value < running:
            print("<p>The QB hands the ball off</p>")
            return ("Running Play", args)
        else:
            print("T<p>he quarterback drops back to pass</p>")
            return ("Passing Play", args)

    def running_play(self, args):
        value = R.randrange(0, 100)
        fumble = self.offense.fumble_chance()
        tackle_for_loss = self.offense.tackle_for_loss_chance()
        long = self.offense.long_run_chance()
        if value < fumble:
            print("<p>FUMBLE!</p>")
            lost = R.randrange(0, 2)
            if lost == 1:
                print("<p>The defense recovers</p>")
                self._first_down()
                self.scoreboard.yardline = 100 - self.scoreboard.yardline
                return ("Swap Possession", args)
            else:
                print("<p>The offense manages to get the ball back</p>")
                self.scoreboard.down += 1
        elif value < tackle_for_loss:
            print("<p>Bonecrushing hit in the backfield for a loss of 2</p>")
            self.scoreboard.distance += 2
            self.scoreboard.yardline -= 2
            self.scoreboard.down += 1
        elif value < long:
            print("<p>What a run! The running back gains 12</p>")
            self.scoreboard.distance -= 12
            self.scoreboard.yardline += 12
            self.scoreboard.down += 1
        else:
            print("<p>The running back crashes up the middle for a gain of 4 yards</p>")
            self.scoreboard.distance -= 4
            self.scoreboard.yardline += 4
            self.scoreboard.down += 1
        return ("Check Time", args)

    def passing_play(self, args):
        value = R.randrange(0,100)
        sack = self.defense.sack_chance()
        interception = self.defense.interception_chance()
        catch = self.offense.catch_chance()
        if value < sack:
            print("<p>The quarterback was sacked!</p>")
            self._move_ball(-6)
        elif value < interception:
            print("<p>It was picked off by the defender!</p>")
            self.scoreboard.home_possession = not self.scoreboard.home_possession
            self.scoreboard.yardline = 100 - self.scoreboard.yardline - 15
            return ("Swap Possession", args)
        elif value < catch:
            print("<p>What a catch by the wide receiver! That's a gain of 10 yards</p>")
            self._move_ball(10)
        else:
            print("<p>The pass sails just a bit long</p>")
        self.scoreboard.down += 1
        return ("Check Time", args)

    def game_over(self, args):
        print("<p>Game over!</p>")
        if self.scoreboard.h_score == self.scoreboard.a_score:
            print("<p>It was a draw!</p>")
        elif self.scoreboard.h_score > self.scoreboard.a_score:
            print("<p>The {:s} Win!</p>".format(self.home_team.name))
        else:
            print("<p>The {:s} Win!</p>".format(self.away_team.name))
        print("<p>{:s}: {:d} {:s}: {:d}</p>".format( self.home_team.short_name, self.scoreboard.h_score, self.away_team.short_name, self.scoreboard.a_score ))
        return 0

if __name__ == "__main__":
    game = Game()
    game.fsm.add_state("Check Time", game.scoreboard.check_time)
    game.fsm.add_state("Check Yardage", game.scoreboard.check_yardage)
    game.fsm.add_state("Swap Possession", game.swap_possession)
    game.fsm.add_state("Describe Down", game.describe_down)
    game.fsm.add_state("Formation", game.formation)
    game.fsm.add_state("Punt", game.punt)
    game.fsm.add_state("Field Goal", game.field_goal)
    game.fsm.add_state("Quaterback Has Ball", game.qb_has_ball)
    game.fsm.add_state("Running Play", game.running_play)
    game.fsm.add_state("Passing Play", game.passing_play)
    game.fsm.add_state("Game Over", game.game_over, end_state=1)
    game.fsm.set_start("Check Time")
    game.fsm.run("")
