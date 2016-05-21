'''
Quyen Mac
ECE 4524
Project 2
03/29/16
This is the SAT Solver using
WalkSat algorithm
'''

import random

def satsolve(filename, max_flips):
    '''
    SAT solver, the function to be called
    Takes in the filename and the max number
    of flips
    '''

    #initialize variables
    max_var = 0
    clauses = ""
    one_zero = ""
    one_zero2 = ""

    # if it is a valid file
    if (valid_file(filename)):
        # get the clauses and max variable from parser
        clauses, max_var = parser(filename)

        # walksat and the results
        walk_sat = Problems(clauses, max_flips, max_var)
        result, boolean = walk_sat.walksat()

        # dpll and the results
        dpll_problem = Problems(clauses, max_flips, max_var)
        dpll_problem.find_unit_clause(([1,2],[-1,3]), {1: True, 2: False})
        results = dpll_problem.dpll_sat()



        # convert to 1s and 0s
        for key in result:
            # if value is true, assign 1
            if (result[key] == True):
                one_zero += "1"
            # if false, assign 0
            else:
                one_zero += "0"

        

        # print out solution
        print "\n"
        # if optimal solution is not found
        if boolean == False:
            print "Optimal solution for walk_sat is not found, closest solution: "
        # it is found
        else:
            print "Solution Found for walk_sat: "
        print one_zero

        # dpll outputs
        if not results:
            print "\tNo solution for dpll"
        else:
            for key in results:
                # if value is true, assign 1
                if (results[key] == True):
                    one_zero2 += "1"
                # if false, assign 0
                else:
                    one_zero2 += "0"
            print "\tdpll: "
            print one_zero2

        print "\n"


def valid_file(in_data):
    '''
    checks if the file could be opened
    '''
    try:
        # open the file
        myfile = open(in_data, 'r')
    except IOError:
        # file cannot be opened
        print "File " + in_data + " could not open!"
        # close file, return false
        myfile.close()
        return False

    # close file, return True, is valid
    myfile.close()
    return True

def parser(in_data):
    '''
    parses the text file
    returns clauses and max variable
    '''

    # open file in read mode
    myfile = open(in_data, 'r')

    # initialize variable
    line_list = list()
    cnf = list()
    cnf.append(list())
    maxvar = 0

    # append each line to a list
    for line in myfile:
        line_list.append(line)

    # close file
    myfile.close()

    # for each line in the list
    for line in line_list:
        # combine the lines
        tokens = line.split()

        # if the line is not p or c and the file is not empty
        if len(tokens) != 0 and tokens[0] not in ("p", "c"):
            # iterate through the combined lines
            for tok in tokens:
                # convert each byte to int
                lit = int(tok)
                # get the max variable
                maxvar = max(maxvar, abs(lit))

                # if we reach delimiter 0
                if lit == 0:
                    # append to list, ignore the 0
                    cnf.append(list())
                else:
                    # append to the list
                    cnf[-1].append(lit)

    # debug
    assert len(cnf[-1]) == 0
    # remove the last 0
    cnf.pop()

    # return clauses and max variable
    return cnf, maxvar

def is_true(exp, model):
    '''
    if the clause is true or false
    given the model
    '''

    # list for the T/F value of the clause
    temp = list()

    # iterate through each proposition
    for x in exp:
        # if number is a NOT
        if x < 0:
            # iterate through model to get the flipped value
            for key in model:
                # if key is equal to the number
                if key == abs(x):
                    # flip the T/F value and append to temp
                    if model[key] == True:
                        temp.append(False)
                    else:
                        temp.append(True)
        # no NOT
        else:
            # iterate through the model
            for key in model:
                # if the key is equal to the number
                if key == x:
                    # append to temp
                    temp.append(model[key])

    # return true if there is at least one true proposition in the clause
    for x in temp:
        if x == True:
            return True
    # else return False
    return False

def removeall(P, symbols):
    '''
    removes all occurance of the symbol
    return the list without the removed symbol
    '''

    # initialize variables
    new_symbols = list()

    # iterate through the list of symbols
    for x in symbols:
        # only append to list if x is not equal to P
        if x != P:
            new_symbols.append(x)

    return new_symbols


def extend(s, var, val):
    '''
    Copy the substitution s and extend it
    set variable to val
    val would be True or False
    return copy
    '''

    temp = s.copy()
    temp[var] = val

    return temp

class Problems:
    '''
    contains walksat and dpll
    '''

    def __init__(self, clauses, max_flips, max_var):
        '''
        constructor
        takes in clauses, max flips and max variable
        '''
        self.clauses = clauses
        self.max_flips = max_flips
        self.max_var = max_var

    def dpll_sat(self):
        '''
        main function for dpll
        checks the satisfiability of a propositional sentence
        '''

        # set the partial module so that each symbol
        # is assigned true
        model = dict([(s, True)
                 for s in range(1, self.max_var + 1)])

        # return the dpll function with parameters of
        # the clauses, symbols, and partial model
        return self.dpll(self.clauses, range(1, self.max_var + 1), model)

    def dpll(self, clauses, symbols, model):
        '''
        recursion function for dpll_sat
        sees if the clauses
        are true in a partial model
        '''
        # empty clauses list
        unknown_clauses = []

        # iterate through each clause
        for clause in clauses:
            # if any clause is false, it is false
            if not is_true(clause, model):
                return False
            # else, append to unknown clauses list
            unknown_clauses.append(clause)

        # if all clauses are true
        # checks the size of both, if equals
        if (len(unknown_clauses) == len(clauses)):
            return model

        # find pure symbol
        P, value = self.find_pure_symbol(symbols, unknown_clauses)
        # if not None
        if P:
            return self.dpll(clauses, removeall(P, symbols), extend(model, P, value))
        # find unit clause
        P, value = find_unit_clause(clauses, model)
        if P:
            return self.dpll(clauses, removeall(P, symbols), extend(model, P, value))
        # get P
        P = symbols.pop()

        # recursion
        return (self.dpll(clauses, symbols, extend(model, P, True)) or
            self.dpll(clauses, symbols, extend(model, P, False)))



    def find_pure_symbol(self, symbols, unknown_clauses):
        '''
        in the clauses, if a symbol is found all positive
        or all negative, then return that symbol
        '''
        # assume each variable is pure, initially
        pure = symbols

        # iterate through the list of symbols
        for s in symbols:
            # initialize found negative and positive booleans
            found_neg, found_pos = False, False
            # iterate through each clause
            for x in unknown_clauses:
                # iterate through each symbol in the clause
                for c in x:
                    # if neg is found
                    if (x < 0 and abs(x) == s):
                        found_neg = True
                    # if pos is found
                    elif (x == s):
                        found_pos = True
                if found_pos != found_neg:
                    return s, found_pos
        return None, None

    def find_unit_clause(self, clauses, model):
        '''
        a unit clause with only 1 variable that
        is not bounded in the model
        '''

        # initialize variables
        list_keys = list()
        true_false = list()
        count = 0
        count2 = 0

        # append keys to list
        for key in model:
            list_keys.append(key)


            # initialize default bool when found
            found = True
            
            for each in clauses:
                # check if all symbols in the clause,
                # are also in the module
                for val in each:
                    if abs(val) not in list_keys:
                        found = False
                        count += 1
                
            # if there is only one variable not in clause
            if not found and count == 1:
                # initially, the unknown variable will be True
                positive = True
                sym = 0
                # iterate through the clause
                for each in clauses:
                    for val in each:
                        # if the symbol match the model, append
                        if val in list_keys:
                            true_false.append(model[each])
                        # if the symbol matches but it's NOT, append the flipped val
                        elif val < 0 and val in list_keys:
                            if model[val] == True:
                                true_false.append(False)
                            else:
                                true_false.append(True)
                        # the final unknown value
                        else:
                            if val < 0:
                                positive = False
                                sym = abs(each)

                # return the unknown value, and the T/F value
                # for the clause to be true
                if all(item[i] == False for item in true_false):
                    if positive:
                        return sym, True
                    else:
                        return sym, False
                else:
                    return sym, True

            





    def walksat(self):
        '''
        model is random assignment of T/F
        iterate through max flips and
        flip a random symbol until solution is
        found, if found
        '''
        # assign random T/F value for each variable into a dictionary
        model = dict([(s, random.choice([True, False]))
                 for s in range(1, self.max_var + 1)])

        # list for when no solution is found
        no_solution = dict()

        # initialize variable
        maxi = 100000

        # iterate through max flips
        for i in range(self.max_flips):
            # create empty list
            unsatisfied = []

            # for each clause
            for clause in self.clauses:
                # if clause returns false
                if not is_true(clause, model):
                    unsatisfied.append(clause)

            # when all clauses are satisfied
            if not unsatisfied:
                # returns model, True for when the optimal solution is found
                return model, True

            # randomly select an unsatisfied clause
            clause_temp = random.choice(unsatisfied)

            # select a random symbol
            symbol = random.choice(clause_temp)

            # iterate through each key in dictionary
            for key in model:
                # if the key is equal to the symbol, flip
                if key == abs(symbol):
                    if model[key] == True:
                        model[key] = False
                    else:
                        model[key] = True
                    break

            # if no solution is found
            # then grab the solution where only 1 clause is unsatisfied
            if len(unsatisfied) < maxi:
                # get smallest length
                maxi = len(unsatisfied)
                no_solution = model.copy()

        # return non-optimal solution, False for no optimal solution found
        return no_solution, False



if __name__ == '__main__':
    '''
    testing through terminal
    '''

    filename = "testcase1.txt"
    satsolve(filename, 10000)


    filename = "c17.txt"
    satsolve(filename,10000)

    filename = "par8-1-c.txt"
    satsolve(filename, 1000)
