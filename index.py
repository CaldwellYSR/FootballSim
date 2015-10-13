#!bin/bash

import StackFSM as FSM
import time

class Game(object):

  fsm = None
  cnt = 0

  def __init__(self):

    self.cnt = 0
    self.fsm = FSM.StackFSM()
    self.fsm.pushState(self.findLeaf)

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
