class Node():

    def __init__(self, parent=None, position=None, g=0, h=0):
       self.position = position
       self.parent = parent
       self.g = g
       self.h = h
       self.f = g + h

    def __eq__ (self, other):
        return self.position == other.position