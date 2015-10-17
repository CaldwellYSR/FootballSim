#!/usr/bin/python

import cgitb
import StackFSM as FSM
import random as R

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
            print("<p>That's the end of the 3rd quarter</p>")
            print("<p>Home Score: {:d} Away Score: {:d}</p>".format( self.h_score, self.a_score ))
            self.quarter = 4
        elif self.time >= 1800:
            print("<p>That's the end of the 2nd quarter</p>")
            print("<p>Home Score: {:d} Away Score: {:d}</p>".format( self.h_score, self.a_score ))
            self.home_possession = False
            self.yardline = 20
            self.down = 1
            self.distance = 10
            self.quarter = 3
        elif self.time >= 900:
            print("<p>That's the end of the 1st quarter</p>")
            print("<p>Home Score: {:d} Away Score: {:d}</p>".format( self.h_score, self.a_score ))
            self.quarter = 2
        return ("Check Yardage", cargo)

    def check_yardage(self, cargo):
        if self.yardline >= 100:
            print("<h3>Touchdown!</h3>")
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
                print("<p>Touchback after the turnover</p>")
                self.yardline = 20
            else:
                print("<h3>Safety!</h3>")
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
            print("<h3>First Down!</h3>")
            self.distance = 10
            self.down = 1
        if self.scored:
            print("<p>Home Score: {:d} Away Score: {:d}</p>".format( self.h_score, self.a_score ))
            self.scored = False
        self.turnover = False
        return ("Describe Down", cargo)

    def describe_down(self, cargo):
        yard = "< "+str(self.yardline) if self.yardline < 50 else str(100 - self.yardline)+" >"
        print("<p>Down: {:d} Distance: {:d} Yardline: {:s}</p>".format( self.down, self.distance, yard))
        return ("Formation", cargo)

    def formation(self, cargo):
        value = R.randrange(0, 100)
        falseStart = 5
        if value < falseStart:
            print("<h3>False Start on the Offense!</h3>")
            self.distance += 10
            self.yardline -= 10
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
        print("<h3>Punt!</h3>")
        self.yardline = 100 - (self.yardline + 40)
        self.home_possession = not self.home_possession
        if self.yardline <= 0:
            if self.home_possession:
                print("<h3>Touchback! The home team takes over at the 20 yard line.</h3>")
            else:
                print("<h2>Touchback! The away team takes over at the 20 yard line.</h3>")
            self.yardline = 20
        else:
            if self.home_possession:
                print("<p>The home team takes over at the {:d} yard line.</p>".format(self.yardline))
            else:
                print("<p>The away team takes over at the {:d} yard line.</p>".format(self.yardline))
            
        self.down = 1
        self.distance = 10
        return ("Check Time", cargo)

    def field_goal(self, cargo):
        print("<h3>{:d} Yard Field Goal!</h3>".format((100 - self.yardline) + 17))
        value = R.randrange(0, 100)
        made = 85
        if value < made:
            print("<h4>It's good!</h4>")
            if self.home_possession:
                self.h_score += 3
            else:
                self.a_score += 3
            self.yardline = 20
            self.scored = True
        else:
            print("<h4>No good!</h4>")
            self.yardline = 100 - self.yardline

        self.down = 1
        self.distance = 10
        self.home_possession = not self.home_possession
        return ("Check Time", cargo)

    def qb_has_ball(self, cargo):
        value = R.randrange(0, 1000)
        running = 550
        if value < running:
            print("<p>The QB hands the ball off</p>")
            return ("Running Play", cargo)
        else:
            print("<p>The quarterback drops back to pass</p>")
            return ("Passing Play", cargo)

    def running_play(self, cargo):
        value = R.randrange(0, 100)
        fumble = 6
        tackle_for_loss = 16
        long = 30
        if value < fumble:
            print("<h3>Fumble!</h3>")
            lost = R.randrange(0, 2)
            if lost == 1:
                print("<p>The defense recovers</p>")
                self.home_possession = not self.home_possession
                self.down = 1
                self.distance = 10
                self.yardline = 100 - self.yardline
                self.turnover = True
            else:
                print("<p>The offense manages to get the ball back</p>")
                self.down += 1
        elif value < tackle_for_loss:
            print("<p>Bonecrushing hit in the backfield for a loss of 2</p>")
            self.distance += 2
            self.yardline -= 2
            self.down += 1
        elif value < long:
            print("<p>What a run! The running back gains 12</p>")
            self.distance -= 12
            self.yardline += 12
            self.down += 1
        else:
            print("<p>The running back crashes up the middle for a gain of 4 yards</p>")
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
            print("<p>The quarterback was sacked!</p>")
            self.distance += 6
            self.yardline -= 6
        elif value < interception:
            print("<h3>It was picked off by the defender!</h3>")
            self.home_possession = not self.home_possession
            self.down = 1
            self.distance = 10
            self.yardline = 100 - self.yardline - 15
            self.turnover = True
        elif value < catch:
            print("<p>What a catch by the wide receiver! That's a gain of 10 yards</p>")
            self.distance -= 10
            self.yardline += 10
        else:
            print("<p>The pass sails just a bit long</p>")
            self.down += 1
        return ("Check Time", cargo)

    def game_over(self, cargo):
        print("<p>Game over!</p>")
        if self.h_score == self.a_score:
            print("<p>It was a draw!</p>")
        elif self.h_score > self.a_score:
            print("<p>The Home Team Wins!</p>")
        else:
            print("<p>The Away Team Wins!</p>")
        print("<p>Home Score: {:d} Away Score: {:d}</p>".format( self.h_score, self.a_score ))

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
  
  cgitb.enable()
  print("Content-Type: text/html")
  print("""
    <html>
    <head>
      <title>Python Football Simulator</title>
      <link rel="stylesheet" href="http://sandbox.matthew-caldwell.com/style.css" />
    </head>
    <body>
  """)
  game.fsm.run("")
  print("""
    </body>
    </html>
  """)
