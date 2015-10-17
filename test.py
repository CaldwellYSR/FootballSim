#!bin/bash

import StackFSM as FSM
import random as R
from math import ceil

class Game:
    def __init__(self):
        self.fsm = FSM.StateMachine()
        self.quarter = 1
        self.down = 1
        self.distance = 10
        self.h_score = 0
        self.a_score = 0
        self.yardline = 20
        self.time = 0
        self.home_possession = True
        self.scored = True
        self.turnover = False

    def check_time(self, cargo):
        self.time += 30
        if self.time >= 3600:
            cargo = (self.h_score, self.a_score)
            return ("Game Over", cargo)
        elif self.time >= 2700:
            print("That's the end of the 3rd quarter")
            print("Home Score: {:d} Away Score: {:d}".format( self.h_score, self.a_score ))
            self.quarter = 4
        elif self.time >= 1800:
            print("That's the end of the 2nd quarter")
            print("Home Score: {:d} Away Score: {:d}".format( self.h_score, self.a_score ))
            self.home_possession = False
            self.yardline = 20
            self.down = 1
            self.distance = 10
            self.quarter = 3
        elif self.time >= 900:
            print("That's the end of the 1st quarter")
            print("Home Score: {:d} Away Score: {:d}".format( self.h_score, self.a_score ))
            self.quarter = 2
        return ("Check Yardage", cargo)

    def check_yardage(self, cargo):
        if self.yardline >= 100:
            print("Touchdown!")
            if self.home_possession:
                self.h_score += 7
            else:
                self.a_score += 7
            self.home_possession = not self.home_possession
            self.yardline = 20
            self.down = 1
            self.distance = 10
            self.scored = True
        elif self.yardline <= 0:
            if self.turnover:
                self.turnover = not self.turnover
                print("Touchback after the turnover")
                self.yardline = 20
            else:
                print("Safety!")
                if self.home_possession:
                        self.a_score += 2 
                else:
                    self.h_score += 2
                self.yardline = 35
                self.down = 1
                self.distance = 1
                self.scored = True
                self.home_possession = not self.home_possession
        elif self.distance <= 0:
            print("First Down!")
            self.distance = 10
            self.down = 1
        if self.scored:
            print("Home Score: {:d} Away Score: {:d}".format( self.h_score, self.a_score ))
            self.scored = False
        return ("Describe Down", cargo)

    def describe_down(self, cargo):
        yard = "< "+str(self.yardline) if self.yardline < 50 else str(100 - self.yardline)+" >"
        print("Down: {:d} Distance: {:d} Yardline: {:s}".format( self.down, self.distance, yard))
        return ("Formation", cargo)

    def formation(self, cargo):
        value = R.randrange(0, 100)
        falseStart = 2
        if value < falseStart:
            print("False Start on the Offense!")
            if self.yardline - 10 > 0:
                self.distance += 10
                self.yardline -= 10
            else:
                tmp = self.yardline
                self.yardline -= ceil(self.yardline / 2.0)
                self.distance += tmp - self.yardline
            return ("Check Time", cargo)
        else:
            if self.down == 4:
                if (self.yardline >= 60):
                    return ("Field Goal", cargo)
                else:
                    return ("Punt", cargo)
            else:
                return ("Quaterback Has Ball", cargo)

    def punt(self, cargo):
        print("Punt!")
        self.yardline = 100 - (self.yardline + 40)
        self.home_possession = not self.home_possession
        if self.yardline <= 0:
            if self.home_possession:
                print("Touchback! The home team takes over at the 20 yard line.")
            else:
                print("Touchback! The away team takes over at the 20 yard line.")
            self.yardline = 20
        else:
            if self.home_possession:
                print("The home team takes over at the {:d} yard line.".format(self.yardline))
            else:
                print("The away team takes over at the {:d} yard line.".format(self.yardline))
            
        self.down = 1
        self.distance = 10
        return ("Check Time", cargo)

    def field_goal(self, cargo):
        print("{:d} Yard Field Goal!".format((100 - self.yardline) + 7))
        value = R.randrange(0, 100)
        made = 85
        if value < made:
            print("It's good!")
            if self.home_possession:
                self.h_score += 3
            else:
                self.a_score += 3
            self.yardline = 20
            self.scored = True
        else:
            print("No good!")
            self.yardline = 100 - self.yardline

        self.down = 1
        self.distance = 10
        self.home_possession = not self.home_possession
        return ("Check Time", cargo)

    def qb_has_ball(self, cargo):
        value = R.randrange(0, 1000)
        running = 550
        if value < running:
            print("The QB hands the ball off")
            return ("Running Play", cargo)
        else:
            print("The quarterback drops back to pass")
            return ("Passing Play", cargo)

    def running_play(self, cargo):
        value = R.randrange(0, 100)
        fumble = 6
        tackle_for_loss = 16
        long = 30
        if value < fumble:
            print("FUMBLE!")
            lost = R.randrange(0, 2)
            if lost == 1:
                print("The defense recovers")
                self.home_possession = not self.home_possession
                self.down = 1
                self.distance = 10
                self.yardline = 100 - self.yardline
            else:
                print("The offense manages to get the ball back")
                self.down += 1
        elif value < tackle_for_loss:
            print("Bonecrushing hit in the backfield for a loss of 2")
            self.distance += 2
            self.yardline -= 2
            self.down += 1
        elif value < long:
            print("What a run! The running back gains 12")
            self.distance -= 12
            self.yardline += 12
            self.down += 1
        else:
            print("The running back crashes up the middle for a gain of 4 yards")
            self.distance -= 4
            self.yardline += 4
            self.down += 1
        return ("Check Time", cargo)

    def passing_play(self, cargo):
        value = R.randrange(0,100)
        sack = 5
        interception = 20
        catch = 65
        if value < sack:
            print("The quarterback was sacked!")
            self.distance += 6
            self.yardline -= 6
        elif value < interception:
            print("It was picked off by the defender!")
            self.home_possession = not self.home_possession
            self.down = 1
            self.distance = 10
            self.yardline = 100 - self.yardline - 15
        elif value < catch:
            print("What a catch by the wide receiver! That's a gain of 10 yards")
            self.distance -= 10
            self.yardline += 10
        else:
            print("The pass sails just a bit long")
            self.down += 1
        return ("Check Time", cargo)

    def game_over(self, cargo):
        print("Game over!")
        if self.h_score == self.a_score:
            print("It was a draw!")
        elif self.h_score > self.a_score:
            print("The Home Team Wins!")
        else:
            print("The Away Team Wins!")
        print("Home Score: {:d} Away Score: {:d}".format( self.h_score, self.a_score ))

if __name__ == "__main__":
    game = Game()
    game.fsm.add_state("Check Time", game.check_time)
    game.fsm.add_state("Check Yardage", game.check_yardage)
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
