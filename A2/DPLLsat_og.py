#!/usr/bin/python3
# CMPT310 A2
#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
"""
num_hours_i_spent_on_this_assignment = 
"""
#
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
"""
<Your feedback goes here>


"""
#####################################################
#####################################################
import sys, getopt
import copy
import random
import time
import numpy as np
sys.setrecursionlimit(10000)

class SatInstance:
    def __init__(self):
        pass

    def from_file(self, inputfile):
        self.clauses = list()
        self.VARS = set()
        self.p = 0
        self.cnf = 0
        with open(inputfile, "r") as input_file:
            self.clauses.append(list())
            maxvar = 0
            for line in input_file:
                tokens = line.split()
                if len(tokens) != 0 and tokens[0] not in ("p", "c"):
                    for tok in tokens:
                        lit = int(tok)
                        maxvar = max(maxvar, abs(lit))
                        if lit == 0:
                            self.clauses.append(list())
                        else:
                            self.clauses[-1].append(lit)
                if tokens[0] == "p":
                    self.p = int(tokens[2])
                    self.cnf = int(tokens[3])
            assert len(self.clauses[-1]) == 0
            self.clauses.pop()
            if (maxvar > self.p):
                print("Non-standard CNF encoding!")
                sys.exit(5)
        # Variables are numbered from 1 to p
        for i in range(1, self.p + 1):
            self.VARS.add(i)

    def __str__(self):
        s = ""
        for clause in self.clauses:
            s += str(clause)
            s += "\n"
        return s


def main(argv):
    inputfile = ''
    verbosity = False
    inputflag = False
    try:
        opts, args = getopt.getopt(argv, "hi:v", ["ifile="])
    except getopt.GetoptError:
        print('DPLLsat.py -i <inputCNFfile> [-v] ')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('DPLLsat.py -i <inputCNFfile> [-v]')
            sys.exit()
        ##-v sets the verbosity of informational output
        ## (set to true for output veriable assignments, defaults to false)
        elif opt == '-v':
            verbosity = True
        elif opt in ("-i", "--ifile"):
            inputfile = arg
            inputflag = True
    if inputflag:
        instance = SatInstance()
        instance.from_file(inputfile)
        #start_time = time.time()
        solve_dpll(instance, verbosity)
        #print("--- %s seconds ---" % (time.time() - start_time))

    else:
        print("You must have an input file!")
        print('DPLLsat.py -i <inputCNFfile> [-v]')


# Finds a satisfying assignment to a SAT instance,
# using the DPLL algorithm.
# Input: a SAT instance and verbosity flag
# Output: print "UNSAT" or
#    "SAT"
#    list of true literals (if verbosity == True)
#
#  You will need to define your own
#  DPLLsat(), DPLL(), pure-elim(), propagate-units(), and
#  any other auxiliary functions

def unit_propation(clauses, symbols):
    for i in symbols:
        for clause in clauses:
            if len(clause) == 1:
                if i in clause:
                    clauses.remove(clause)
    return clauses

def propagate_units(clauses):
    unitClauses = []
    symbols = []
    for clause in clauses:
        if len(clause) == 1:
            unitClauses.append([clause])
    while len(unitClauses) != 0:
        symbols.append(unitClauses[0])
        var = unitClauses[0]
        ret = check_var(clauses, var[0])
        symbols.append([var[0]])
        if ret == False:
            return False, []
        if not F:
            return F, symbols
        unitClauses = [clause for clause in clauses if len(clause) == 1]
    return clauses, symbols


def check_var(clauses, var):
    new_clauses = []
    #clauses = propagate_units(input_clauses, var)
    count = 0
    for clause in clauses:
        if var in clause:
            continue
        if -var in clause:
            newClause = []

            for i in clause:
                if (i != -var):
                    newClause.append(i)

            if len(newClause) == 0:
                return False
            new_clauses.append(newClause)

        else:
            count += 1
            new_clauses.append(clause)

    if count == len(clauses):
        return clauses
    return new_clauses

def check_symbols(clauses, symbols, visited):
    #print("start clauses: " + str(clauses))
    #print("checking... symbols: " + str(symbols))
    #new_clauses = unit_propation(clauses, symbols)
    #print("prop clauses: " + str(new_clauses))

    new_clauses = clauses
    for symbol in symbols:
        #print("new_clauses: " + str(new_clauses))
        #print("checking symbol: " + str(symbol))

        ret = check_var(new_clauses, symbol)
        if ret == False:
            #print("False")
            return False
        else:
            #print("return: " + str(ret))
            new_clauses = ret
    if(len(symbols) == len(visited)):
        if new_clauses != []:
            return False
    return new_clauses

def count(F): #count number of occurrances of each val
    counter = {}
    for c in F:
        for x in c:
            if x in counter:
                counter[x] += 1
            else:
                counter[x] = 1
    return counter

def DPLL(clauses, symbols, model, visited):
    #print("model: " + str(model) + " *~*~*~*~*~*~*~*~*~")

    sol = check_symbols(clauses, model, visited)
    # print("sol: " + str(sol))

    if sol == []:
        #print("SAT SOLUTION FOUND! model: " + str(model))
        return model

    elif sol == False:
        #print("UNSAT!")
        return False
    """
    if len(symbols) != 0:
        P = symbols.pop(0)
    else:
        #print("Check Symbol RESET!")
        check = []
        for i in model:
            check.append(abs(i))
        for j in visited:
            if j not in check:
                symbols.append(j)
        P = symbols.pop(0)
    

    for value in [1,-1]:
        ret = DPLL(clauses, symbols, model + [P*value], visited)

        if ret != False:
            return ret
    """
    counter = count(clauses):

    #print("end return: " + str(ret) )
    return ret

def format_answer(answer):
    ret_answer = []
    for i in answer:
        if i > 0:
            ret_answer.append(i)
    ret_answer.sort()
    return ret_answer


def solve_dpll(instance, verbosity):
    # print(instance)
    # instance.VARS goes 1 to N in a dict
    # print(instance.VARS)
    # print(verbosity)
    ###########################################
    # Start your code
    clauses = instance.clauses
    variables = instance.VARS

    symbols = list(variables)
    visited = variables
    #ret = propagate_units([ [1,2,3],[1],[2],[3,2],[3] ],1)
    #print(ret) 
    """
    print("START TESTING -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n\n")
    
    print("symbols: " + str(symbols))
    print("clauses: " + str(clauses))

    #checked_1 = check_var(clauses, 1)
    #print("check_var 1: " + str(checked_1))
    #checked_2 = check_var(clauses, 2)
    #print("check_var 2: " + str(checked_2))
    #checked_3 = check_var(clauses, 3)
    #print("check_var 3: " + str(checked_3))

    print("check_symbols: " + str(check_symbols(clauses, [1,2,3,-4], visited)))
    
    #ret = unit_propation([ [1,2,3],[1],[2],[3,2],[3] ],[1,3])
    #print(ret)

    print("\n\nEND TESTING -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n\n")
    """
    
    answer = DPLL(clauses,symbols,[], visited)
    if answer == False:
        print("UNSAT")

    else:
        print("SAT")
        if verbosity == True:
            print(format_answer(answer))
    



    ###########################################


if __name__ == "__main__":
    main(sys.argv[1:])
