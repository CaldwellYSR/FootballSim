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

# m = StateMachine()
# m.add_state("Start", start_transitions)
# m.add_state("Python_state", python_state_transitions)
# m.add_state("is_state", is_state_transitions)
# m.add_state("not_state", not_state_transitions)
# m.add_state("neg_state", None, end_state=1)
# m.add_state("pos_state", None, end_state=1)
# m.add_state("error_state", None, end_state=1)
# m.set_start("Start")
# m.run("Python is great")
# m.run("Python is difficult")
# m.run("Perl is ugly")

class StateMachine:
    def __init__(self):
        self.handlers = {}
        self.startState = None
        self.endStates = []

    def add_state(self, name, handler, end_state=0):
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)

    def set_start(self, name):
        self.startState = name.upper()

    def run(self, cargo):
        try:
            handler = self.handlers[self.startState]
        except:
            raise InitializationError("must call .set_start() before .run()")
        if not self.endStates:
            raise  InitializationError("at least one state must be an end_state")
    
        while True:
            (newState, cargo) = handler(cargo)
            if newState.upper() in self.endStates:
                handler = self.handlers[newState.upper()]  
                handler(cargo)
                break 
            else:
                handler = self.handlers[newState.upper()]  
