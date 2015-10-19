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
        print("===== New Game =====")
        print()
        self.home_team = T.Team("Miami Dolphins", "MIA")
        self.away_team = T.Team("New England Patriots", "NE")
        self.offense = self.home_team
        self.defense = self.away_team
        self.offense.possession = True
        self.scoreboard.home_possession = self.home_team.possession
        print("The {:s} have the ball at their own 20 yard line.".format(self.offense.name))
    
    def describe_down(self, cargo):
        yard = "< "+str(self.scoreboard.yardline) if self.scoreboard.yardline < 50 else str(100 - self.scoreboard.yardline)+" >"
        print("Down: {:d} Distance: {:d} Yardline: {:s}".format( self.scoreboard.down, self.scoreboard.distance, yard))
        return ("Formation", cargo)

    def _move_ball(self, yds):
        self.scoreboard.distance -= yds
        self.scoreboard.yardline += yds

    def _first_down(self):
        self.scoreboard.down = 1
        self.scoreboard.distance = 10

    def swap_possession(self, cargo):
        print("The {:s} take over at the {:d} yard line".format(self.defense.name, self.scoreboard.yardline))
        tmp = self.offense
        self.offense = self.defense
        self.defense = tmp
        self.offense.possession = False
        self.defense.possession = True
        return ("Check Time", cargo)

    def formation(self, cargo):
        value = R.randrange(0, 100)
        falseStart = self.offense.false_start_chance()
        if value < falseStart:
            print("False Start on the Offense!")
            if self.scoreboard.yardline - 10 > 0:
                self._move_ball(-10)
            else:
                tmp = self.scoreboard.yardline
                self.scoreboard.yardline -= ceil(self.scoreboard.yardline / 2.0)
                self.scoreboard.distance += tmp - self.scoreboard.yardline
            return ("Check Time", cargo)
        else:
            if self.scoreboard.down == 4:
                if (self.scoreboard.yardline >= 60):
                    return ("Field Goal", cargo)
                else:
                    return ("Punt", cargo)
            else:
                return ("Quaterback Has Ball", cargo)

    def punt(self, cargo):
        print("Punt!")
        self.scoreboard.yardline = 100 - (self.scoreboard.yardline + 40)
        if self.scoreboard.yardline <= 0:
            print("Touchback!")
            self.scoreboard.yardline = 20
            
        self._first_down()
        return ("Swap Possession", cargo)

    def field_goal(self, cargo):
        print("{:d} Yard Field Goal!".format((100 - self.scoreboard.yardline) + 7))
        value = R.randrange(0, 100)
        made = self.offense.field_goal_chance()
        if value < made:
            print("It's good!")
            if self.scoreboard.home_possession:
                self.scoreboard.h_score += 3
            else:
                self.scoreboard.a_score += 3
            self.scoreboard.yardline = 20
            self.scoreboard.scored = True
        else:
            print("No good!")
            self.scoreboard.yardline = 100 - self.scoreboard.yardline

        self._first_down()
        return ("Swap Possession", cargo)

    def qb_has_ball(self, cargo):
        value = R.randrange(0, 1000)
        running = self.offense.running_play_chance()
        if value < running:
            print("The QB hands the ball off")
            return ("Running Play", cargo)
        else:
            print("The quarterback drops back to pass")
            return ("Passing Play", cargo)

    def running_play(self, cargo):
        value = R.randrange(0, 100)
        fumble = self.offense.fumble_chance()
        tackle_for_loss = self.offense.tackle_for_loss_chance()
        long = self.offense.long_run_chance()
        if value < fumble:
            print("FUMBLE!")
            lost = R.randrange(0, 2)
            if lost == 1:
                print("The defense recovers")
                self._first_down()
                self.scoreboard.yardline = 100 - self.scoreboard.yardline
                return ("Swap Possession", cargo)
            else:
                print("The offense manages to get the ball back")
                self.scoreboard.down += 1
        elif value < tackle_for_loss:
            print("Bonecrushing hit in the backfield for a loss of 2")
            self.scoreboard.distance += 2
            self.scoreboard.yardline -= 2
            self.scoreboard.down += 1
        elif value < long:
            print("What a run! The running back gains 12")
            self.scoreboard.distance -= 12
            self.scoreboard.yardline += 12
            self.scoreboard.down += 1
        else:
            print("The running back crashes up the middle for a gain of 4 yards")
            self.scoreboard.distance -= 4
            self.scoreboard.yardline += 4
            self.scoreboard.down += 1
        return ("Check Time", cargo)

    def passing_play(self, cargo):
        value = R.randrange(0,100)
        sack = self.defense.sack_chance()
        interception = self.defense.interception_chance()
        catch = self.offense.catch_chance()
        if value < sack:
            print("The quarterback was sacked!")
            self._move_ball(-6)
        elif value < interception:
            print("It was picked off by the defender!")
            self.scoreboard.home_possession = not self.scoreboard.home_possession
            self.scoreboard.yardline = 100 - self.scoreboard.yardline - 15
            return ("Swap Possession", cargo)
        elif value < catch:
            print("What a catch by the wide receiver! That's a gain of 10 yards")
            self._move_ball(10)
        else:
            print("The pass sails just a bit long")
        self.scoreboard.down += 1
        return ("Check Time", cargo)

    def game_over(self, cargo):
        print("Game over!")
        if self.scoreboard.h_score == self.scoreboard.a_score:
            print("It was a draw!")
        elif self.scoreboard.h_score > self.scoreboard.a_score:
            print("The {:s} Win!".format(self.home_team.name))
        else:
            print("The {:s} Win!".format(self.away_team.name))
        print("{:s}: {:d} {:s}: {:d}".format( self.home_team.short_name, self.scoreboard.h_score, self.away_team.short_name, self.scoreboard.a_score ))
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
