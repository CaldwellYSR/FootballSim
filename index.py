#!bin/bash

import StackFSM as FSM
import time
import random as R

class Game(object):

  fsm = None
  cnt = 0
  quarter = 1
  down = 1
  distance = 10
  h_score = 0
  a_score = 0
  yardline = 20
  time = 0
  home_possession = True
  scored = True

  def __init__(self):
    self.cnt = 0
    self.quarter = 1
    self.down = 1
    self.distance = 10
    self.h_score = 0
    self.a_score = 0
    self.yardline = 20
    self.time = 0
    self.home_possession = True
    self.scored = True
    self.fsm = FSM.StackFSM()
    self.fsm.pushState(self.check_time)
    self.fsm.pushState(self.check_yardage)

  def check_time(self):
    self.time += 30
    if self.time >= 3600:
        self.fsm.pushState(self.game_over)
    elif self.time >= 2700:
        print("That's the end of the 3rd quarter")
        print("Home Score: {:d} Away Score: {:d}".format( self.h_score, self.a_score ))
        self.quarter = 4
    elif self.time >= 1800:
        print("That's the end of the 2nd quarter")
        print("Home Score: {:d} Away Score: {:d}".format( self.h_score, self.a_score ))
        self.quarter = 3
    elif self.time >= 900:
        print("That's the end of the 1st quarter")
        print("Home Score: {:d} Away Score: {:d}".format( self.h_score, self.a_score ))
        self.quarter = 2
    self.fsm.pushState(self.check_yardage)

  def check_yardage(self):
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
    self.fsm.popState()
    self.fsm.pushState(self.describe_down)


  def describe_down(self):
    yard = "< "+str(self.yardline) if self.yardline < 50 else str(100 - self.yardline)+" >"
    print("Down: {:d} Distance: {:d} Yardline: {:s}".format( self.down, self.distance, yard))
    self.fsm.popState()
    self.fsm.pushState(self.formation)

  def formation(self):
    value = R.randrange(0, 100)
    falseStart = 5
    if value < falseStart:
        print("False Start on the Offense!")
        self.distance += 10
        self.yardline -= 10
        self.fsm.popState()
    else:
        self.fsm.popState()
        if self.down == 4:
            if (self.yardline >= 60):
                self.fsm.pushState(self.field_goal)
            else:
                self.fsm.pushState(self.punt)
        else:
            self.fsm.pushState(self.qb_has_ball)

  def punt(self):
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
    self.fsm.popState()

  def field_goal(self):
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
      self.fsm.popState()

  def qb_has_ball(self):
    value = R.randrange(0, 1000)
    running = 550
    if value < running:
        print("The QB hands the ball off")
        self.fsm.popState()
        self.fsm.pushState(self.running_play)
    else:
        print("The quarterback drops back to pass")
        self.fsm.popState()
        self.fsm.pushState(self.passing_play)

  def running_play(self):
      print("The running back crashes up the middle for a gain of 4 yards")
      self.distance -= 4
      self.yardline += 4
      self.down += 1
      self.fsm.popState()

  def passing_play(self):
      value = R.randrange(0,100)
      sack = 5
      catch = 65
      if value < sack:
          print("The quarterback was sacked!")
          self.distance += 6
          self.yardline -= 6
      elif value < catch:
          print("What a catch by the wide receiver! That's a gain of 10 yards")
          self.distance -= 10
          self.yardline += 10
      else:
          print("The pass sails just a bit long")
      self.down += 1
      self.fsm.popState()

  def game_over(self):
      print("Game over!")
      if self.h_score == self.a_score:
          print("It was a draw!")
      elif self.h_score > self.a_score:
          print("The Home Team Wins!")
      else:
          print("The Away Team Wins!")
      print("Home Score: {:d} Away Score: {:d}".format( self.h_score, self.a_score ))
      exit()

  def update(self, dt):
    self.fsm.update()

if __name__ == "__main__":
  game = Game()
  lastFrameTime = 0
  FPS = 600
  while True:
    currentTime = time.time()
    dt = currentTime - lastFrameTime
    lastFrameTime = currentTime

    sleepTime = 1./FPS - (currentTime - lastFrameTime)
    if sleepTime > 0:
      time.sleep(sleepTime)

    game.update(dt)
