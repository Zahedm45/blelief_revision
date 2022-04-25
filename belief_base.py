import math
import numpy as np

from sympy.logic.boolalg import to_cnf, And, Or, Equivalent

class Belief:
    def __init__(self, formula, order=None):
        self.formula = formula
        self.order = order



class Belief_Base(self):

    def __init__(self):
        self.beliefs = {}
        sorted(self.beliefs.items(),key=lambda x: -x[1])
        self.new_beliefs = [] #==> not sure it's useful

    def create_new_belief(self,belief): # maybe we can mix this function with the next one, but it might be useful later to have them separate
        if belief.order<=1 and belief.order>=0 :
            self.new_beliefs.append((to_cnf(belief.formula),belief.order))

    def add_new_beliefs(self):
        
        for b,o in self.new_beliefs:
            self.beliefs[b] = o

        sorted(self.beliefs.items(),key=lambda x:-x[1])
        self.new_beliefs = []
    

    