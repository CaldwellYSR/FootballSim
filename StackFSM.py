#!bin/bash

class StackFSM(object):

  stack = None

  def __init__(self):
    self.stack = []

  def update(self):
    currentState = self.getCurrentState()
    
    if(currentState is not None):
      currentState()

  def popState(self):
    return self.stack.pop()

  def pushState(self, state):
    if(self.getCurrentState() is not state):
      self.stack.append(state)

  def getCurrentState(self):
    return self.stack[len(self.stack) - 1] if len(self.stack) > 0 else None
