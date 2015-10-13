#!bin/bash

import StackFSM as FSM
import time

class Ant(object):

  brain = None
  cnt = 0

  def __init__(self):

    self.cnt = 0
    self.brain = FSM.StackFSM()
    self.brain.pushState(self.findLeaf)

  def findLeaf(self):
    self.cnt += 1
    if(self.cnt == 5):
      self.cnt = 0
      print("Found Leaf... going home")
      self.brain.popState()
      self.brain.pushState(self.goHome)
    else:
      print("Looking for Leaf")

  def goHome(self):
    self.cnt += 1
    if(self.cnt == 5):
      self.cnt = 0
      print("Leaf is home... looking for more")
      self.brain.popState()
      self.brain.pushState(self.findLeaf)
    else:
      print("Going home...")

  def update(self, dt):
    self.brain.update()

if __name__ == "__main__":
  ant = Ant()
  lastFrameTime = 0
  FPS = 1
  while True:
    currentTime = time.time()
    dt = currentTime - lastFrameTime
    lastFrameTime = currentTime

    sleepTime = 1./FPS - (currentTime - lastFrameTime)
    if sleepTime > 0:
      time.sleep(sleepTime)

    ant.update(dt)
