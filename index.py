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

  def __init__(self):

    self.cnt = 0
    self.quarter = 1
    self.down = 1
    self.distance = 10
    self.h_score = 0
    self.a_score = 0
    self.fsm = FSM.StackFSM()
    self.fsm.pushState(self.describe_down)

  def describe_down(self):
    print("Down: {:d} Distance: {:d}".format( self.down, self.distance ))
    self.fsm.pushState(self.formation)

  def formation(self):
    value = R.randrange(0, 1000)
    falseStart = 500
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
    print("They punt the ball to the enemy")
    self.down = 1
    self.distance = 10
    self.fsm.popState()

  def qb_has_ball(self):
    print("The quarterback spikes the ball")
    self.distance += 2
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
  FPS = 1
  while True:
    currentTime = time.time()
    dt = currentTime - lastFrameTime
    lastFrameTime = currentTime

    sleepTime = 1./FPS - (currentTime - lastFrameTime)
    if sleepTime > 0:
      time.sleep(sleepTime)

    game.update(dt)
