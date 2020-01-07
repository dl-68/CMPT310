#!/usr/bin/python3
# CMPT310 A2
#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
"""
num_hours_i_spent_on_this_assignment = 30
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
Material in class have been interesting so far. Topics are relatively easy
to understand but hard to implement. No suggestions for changes at the moment.


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

# Elminates set a symbol to True/False (var/-var) elminiates it from
# clauses. Returns new clauses.
def elim_symbol(clauses, var):
    new_clauses = []
    for clause in clauses:
    # var is True in clause, clause is True
        if var in clause:
            continue
        if -(var) in clause:
        # var is False, need to remove
            newClause = []
            for i in clause:
                if i != -(var):
                    newClause.append(i)
            if len(newClause) == 0:
                return False
            new_clauses.append(newClause)
        else:
            new_clauses.append(clause)
    return new_clauses

# Find all symbols which has a unit clause in clauses add to symbol_list
# if it does not exist in symbol_list,
def find_unitclauses(clauses, symbol_list):
    for clause in clauses:
        if len(clause) == 1:
            if clause[0] not in symbol_list:
                symbol_list.append(clause[0])
    return symbol_list

# Find all occurences unit clauses, elminate a each symbol that occurs
# in those unit clauses with elim_symbol. Returns eliminated symbols
# list and returns new clauses.
def propagate_units(clauses):
    #print("to_prop clauses: " + str(clauses))
    if clauses == False:
        return [], False
    symbols = []
    unitSymbols = []
    find_unitclauses(clauses, unitSymbols)
    #print("unitSymbols: " + str(unitSymbols))

    while len(unitSymbols) != 0:
        elimVar = unitSymbols.pop()
        #print("elimVar: " + str(elimVar))
        symbols.append(elimVar)
        clauses = elim_symbol(clauses, elimVar)
        #print("elimClauses: " + str(clauses))

        if clauses == False:
            #print("return: [], False")
            return [], False
        elif clauses == []:
            #print("claues == [] return: ")
            #print("symbols: " + str(symbols))
            #print("claues: " + str(clauses) + "\n")
            return symbols, clauses

        find_unitclauses(clauses, unitSymbols)

    #print("return: ")
    #print("symbols: " + str(symbols))
    #print("clauses: " + str(clauses) + "\n")
    return symbols, clauses

# Finds the number of remaining occurences left in clauses.
# Creates a dictionary where the key is symbols(True/False)
# and value is number of occurences. Represents the remaining
# branches of recursive calls.
def check_clauses(clauses):
    check_list = []
    for clause in clauses:
        for symbol in clause:
            check_list.append(symbol)

    return check_list

# Function to find most frequent occurence in a list
def most_freq(a_list):
    top_freq = 0
    symbol = a_list[0]

    for i in a_list:
        i_freq = a_list.count(i)
        if(i_freq > top_freq):
            top_freq = i_freq
            symbol = i
    return symbol

# Finds all occurences of pure literals, returns pure lits and new clauses
# with pure-literals eliminated
def pure_elim(clauses):
    if clauses == False:
        return [], False

    true_list = []
    false_list = []
    pure_literals = []

    for clause in clauses:
        for symbol in clause:
            if symbol > 0:
                if symbol not in true_list:
                    true_list.append(symbol)
            elif symbol < 0:
                if symbol not in false_list:
                    false_list.append(symbol)

    abs_false_list = [abs(x) for x in false_list]

    for lit in abs_false_list:
        if lit not in true_list:
            pure_literals.append(-lit)
    for lit in true_list:
        if lit not in abs_false_list:
            pure_literals.append(lit)

    for symbol in pure_literals:
        #print("elim clauses: " + str(clauses) + "\n")
        #print("elim symbol: " + str(symbol))
        clauses = elim_symbol(clauses, symbol)
        #print("elimed clauses: " + str(clauses) + "\n")

    #print("true_list: " + str(true_list))
    #print("false_list: " + str(false_list))
    #print("pure_literals: " + str(pure_literals) + "\n")
    return pure_literals, clauses


# Main recursive DPLL function
def DPLL(symbols, clauses):
    prop_symbols, clauses = propagate_units(clauses)
    pure_symbols, clauses = pure_elim(clauses)
    #print("symbols = " + str(symbols) + " + " + str(prop_symbols))
    symbols = symbols + prop_symbols + pure_symbols

    # Base cases
    #print("Clauses: ")
    #print(clauses)
    if clauses == False:
        return False
    if not clauses:
        return symbols

    # Check possible choices and choose one
    check = check_clauses(clauses)
    #print("Remaining values to check:")
    #print(check)
    #print("\n")

    #P = most_freq(check) # choose most freqent occurence symbol left
    P = random.choice(check) # choose random
    #print("checking.... P = " + str(P))

    # First recurse with True then False
    ret = DPLL(symbols + [P], elim_symbol(clauses, P))
    if not ret:
        ret = DPLL(symbols + [-P], elim_symbol(clauses, -P))
    return ret


def solve_dpll(instance, verbosity):
    # print(instance)
    # instance.VARS goes 1 to N in a dict
    # print(instance.VARS)
    # print(verbosity)
    ###########################################
    # Start your code
    clauses = instance.clauses
    variables = instance.VARS

    """
    print("~+~+~+~+~+~+~+~+~+ DEBUG ~+~+~+~+~+~+~+~+~+~+")
    test_clause = [[1,2,3],[1],[2],[-2,3],[1,-3]]
    print(test_clause)
    print(pure_elim(test_clause))
    print("~+~+~+~+~+~+~+~+~+  END  ~+~+~+~+~+~+~+~+~+~+")
    """

    answer = DPLL([], clauses)

    if answer == False:
        print("UNSAT")

    else:
        print("SAT")
        if verbosity == True:
            ret_answer = []
            for i in answer:
                if i > 0:
                    ret_answer.append(i)
            ret_answer.sort()
            print(ret_answer)

    ###########################################
    
if __name__ == "__main__":
    main(sys.argv[1:])
