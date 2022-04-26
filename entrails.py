import numpy as np
import math
from sympy.logic.boolalg import to_cnf, And, Or, Equivalent


def entails(KB,phi):

    phi = to_cnf(phi)
    clauses = []

    for i in KB:
        clauses += split_base(KB)

    clauses += split_base(to_cnf(~phi))


    result = {}                 # Check with thomas what type the function resolve gives
    n = len(clauses)
    for i in range(n):
        for j in range(i+1,n):
            L = resolve(clauses[i],clauses[j])
            if False in L :
                return True     # The goal of the entailment is to find a contradiction since we are reasoning by absurd.
            
            result.union(L)     # Check with thomas what type the function resolve gives