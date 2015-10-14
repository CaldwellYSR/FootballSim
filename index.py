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
  home_possession = True

  def __init__(self):

    self.cnt = 0
    self.quarter = 1
    self.down = 1
    self.distance = 10
    self.h_score = 0
    self.a_score = 0
    self.yardline = 20
    self.home_possession = True
    self.fsm = FSM.StackFSM()
    self.fsm.pushState(self.describe_down)

  def describe_down(self):
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
        print("Home Score: {:d} Away Score: {:d}".format( self.h_score, self.a_score ))
        exit()
    elif self.distance <= 0:
        print("First Down!")
        self.distance = 10
        self.down = 1
    print("Down: {:d} Distance: {:d} Yardline: {:d}".format( self.down, self.distance, self.yardline ))
    self.fsm.pushState(self.formation)

  def formation(self):
    value = R.randrange(0, 1000)
    falseStart = 150
    if value < falseStart:
        print("False Start on the Offense!")
        self.distance += 10
        self.fsm.popState()
    else:
        self.fsm.popState()
        if self.down == 4:
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

  def qb_has_ball(self):
    value = R.randrange(0, 1000)
    running = 550
    if value < running:
        # This is a running play. Do some running stuff
        print("The QB hands the ball off")
        self.fsm.popState()
        self.fsm.pushState(self.running_play)
    else:
        # This is a passing play
        print("The quarterback drops back to pass")
        self.fsm.popState()
        self.fsm.pushState(self.passing_play)

  def running_play(self):
      print("The running back crashes up the middle for a gain of 3 yards")
      self.distance -= 3
      self.yardline += 3
      self.down += 1
      self.fsm.popState()

  def passing_play(self):
      value = R.randrange(0,100)
      catch = 65
      if value < catch:
          print("What a catch by the wide receiver! That's a gain of 10 yards")
          self.distance -= 10
          self.yardline += 10
      else:
          print("The pass sails just a bit long")
      self.down += 1
      self.fsm.popState()

  def findLeaf(self):
    self.cnt += 1
    if(self.cnt == 5):
      self.cnt = 0
      print("Found Leaf... going home")
      self.fsm.popState()
      self.fsm.pushState(self.goHome)
    else:
      print("Looking for Leaf")

  def goHome(self):
    self.cnt += 1
    if(self.cnt == 5):
      self.cnt = 0
      print("Leaf is home... looking for more")
      self.fsm.popState()
      self.fsm.pushState(self.findLeaf)
    else:
      print("Going home...")

  def update(self, dt):
    self.fsm.update()

if __name__ == "__main__":
  game = Game()
  lastFrameTime = 0
  FPS = 60
  while True:
    currentTime = time.time()
    dt = currentTime - lastFrameTime
    lastFrameTime = currentTime

    sleepTime = 1./FPS - (currentTime - lastFrameTime)
    if sleepTime > 0:
      time.sleep(sleepTime)

    game.update(dt)
