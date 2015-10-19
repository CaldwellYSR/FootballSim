#!/usr/bin/python

class Scoreboard:

    def __init__(self):
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
        if self.time >= 3600 and self.quarter == 4:
            return ("Game Over", cargo)
        elif self.time >= 2700 and self.quarter == 3:
            print("<p>That's the end of the 3rd quarter</p>")
            print("<p>Home Score: {:d} Away Score: {:d}</p>".format( self.h_score, self.a_score ))
            self.quarter = 4
        elif self.time >= 1800 and self.quarter == 2:
            print("<p>That's the end of the 2nd quarter</p>")
            print("<p>Home Score: {:d} Away Score: {:d}</p>".format( self.h_score, self.a_score ))
            self.home_possession = False
            self.yardline = 20
            self.down = 1
            self.distance = 10
            self.quarter = 3
        elif self.time >= 900 and self.quarter == 1:
            print("<p>That's the end of the 1st quarter</p>")
            print("<p>Home Score: {:d} Away Score: {:d}</p>".format( self.h_score, self.a_score ))
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
        if self.turnover:
            self.turnover = False
            return ("Swap Possession", cargo)
        return ("Describe Down", cargo)

