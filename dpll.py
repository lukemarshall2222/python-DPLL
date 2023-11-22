"""

Luke Marshall
DPLL solver

ANDs are implicit in the dpll array between each of the clauses, ORs are implicit in the clause arrays
"""

from typing import Union

class Literal(object):

    def __init__(self, variable) -> None:
        self.__variable = str(variable)
        self.__sign = "+"
        self.__status = None
        self.__calculated_val = None

    def __str__(self) -> str:
        return self.__sign + f"{self.__variable}"
    
    def NOT(self):
        # ~(~a) == a
        # ~(a) == ~a
        self.__sign = '-' if self.__sign == '+' else '+'
        if self.__status is not None:
            self.set_calculated_val()
    
    def get_variable(self):
        return self.__variable
    
    def get_sign(self):
        return 'pos' if self.__sign == '+' else 'neg'
    
    def set_status(self, val=True):
        try:
            if not isinstance(val, bool):
                raise TypeError
        except TypeError:
            print('set_status only takes a boolean value as an argument.')
            raise TypeError
        self.__status = val
        self.set_calculated_val()

    def get_status(self):
        return self.__status
    
    def get_calculated_val(self):
        return self.__calculated_val
    
    def set_calculated_val(self):
        if self.__status is None:
            pass
        elif self.__status == True:
            self.__calculated_val = self.__sign == '+'
        elif self.__status == False:
            self.__calculated_val = self.__sign == '-'

    def __eq__(self, other: 'Literal',) -> bool:
        return self.get_variable() == other.get_variable()


class DPLL(object):

    def __init__(self, *args) -> None:
        self.__variables = {}
        self.__proposition = [arg for arg in args]
        for clause in self.__proposition:
            if not isinstance(clause, Literal) and not isinstance(clause, Clause):
                print("The proposition only takes Literal and Clause objects.")
                raise TypeError
            elif isinstance(clause, Literal):
                if not clause.get_variable() in self.__variables:
                    self.__variables[clause.get_variable()] = None
            else:
                for lit in clause:
                    if not lit.get_variable() in self.__variables:
                        self.__variables[lit.get_variable()] = None


    def ADD(self, clause):
        if isinstance(clause, set): # negating a clause produces separted negated literals that must be added individually
            while len(clause != 0):
                x = clause.pop()
                if not isinstance(x, Clause) and not isinstance(x, Literal):
                    print("DPLL proposition can only be made up of Literal and Clause objects.")
                    raise TypeError
                x_var = x.get_variable()
                if not x_var in self.__variables:
                    self.__variables[x_var] = None
                self.__proposition.append(x)
        elif isinstance(clause, Literal):
            if not clause.get_variable() in self.__variables:
                self.__variables[clause.get_variable()] = None
            self.__proposition.append(clause) # add the literal directly to the proposition
        elif isinstance(clause, Clause):
            for lit in clause:
                if not lit.get_variable() in self.__variables:
                    self.__variables[lit.get_variable()] = None
            self.__proposition.append(clause) # add the clause directly to the proposition
        else:
            print("DPLL proposition can only be made up of Literal and Clause objects.")
            raise TypeError
        
    def remove(self, clause):
        if clause in self.__proposition:
            self.__proposition.remove(clause)
        else:
            return False
        return True
    
    def __iter__(self):
        return iter(self.__proposition)
    
    def __getitem__(self, index):
        return self.__proposition[index]
    
    def is_empty(self):
        return len(self.__proposition) == 0

    def sat(self):
        """Returns if the proposition is solvable or not"""
        # check if all the clauses in the proposition are true, if they are, the proposition is satisfied
        if self.is_empty():
            return "sat"
        sat = True
        unsat = True
        for clause in self.__proposition:
            if isinstance(clause, Literal):
                sat = False if not clause.get_calculated_val() else sat
                unsat = False if clause.get_calculated_val() else unsat
            elif isinstance(clause, Clause):
                sat = False if clause.get_status() == False else sat
                unsat = False if clause.get_status() == True else unsat
        if sat:
            return "sat"
        elif unsat:
            return "unsat"
        
        # apply unit clause heristic
        res = self.unit_clause_heuristic()
        if res == 'unsat':
            return res
        elif res == 'changed':
            return self.sat()
        
        # apply pure clause hueristic
        res2 = self.pure_clause_hueristic()
        if res2:
            return sat() 
        
        # apply guess and check
        prop_cp = self.__proposition.copy()
        vars_cp = self.__variables.copy()
        least = len(self.__proposition[0])
        guess = self.__proposition[0][0].get_variable()
        for clause in self.__proposition:
            if len(clause) < least:
                least = len(clause)
                guess = clause[0].get_variable()
        self.__variables[guess] = True
        for clause in self.__proposition:
            assert isinstance(clause, Clause)
            for lit in clause:
                assert isinstance(lit, Literal)
                if lit.get_variable() == guess:
                    lit.set_status()
                    if lit.get_sign() == 'pos':
                        self.__proposition.remove(clause)
                        break
                    else:
                        clause.remove(lit)
                        continue
        res3 = sat()
        if res3 == 'sat':
            return res3
        else:
            self.__proposition = prop_cp
            self.__variables = vars_cp
        self.__variables[guess] = False
        for clause in self.__proposition:
            assert isinstance(clause, Clause)
            for lit in clause:
                assert isinstance(lit, Literal)
                if lit.get_variable() == guess:
                    lit.set_status(False)
                    if lit.get_sign() == 'neg':
                        self.__proposition.remove(clause)
                        break
                    else:
                        clause.remove(lit)
                        continue

        return sat()


    def pure_clause_hueristic(self) -> bool:
        # check if a variable shows up only in its positive or negative form in the proposition
        changed = False
        var_signs = {}
        var_uniformity = {}
        for clause in self.__proposition:
            assert isinstance(clause, Clause), "non-Clause found during pure clause check"
            for lit in clause:
                assert isinstance(lit, Literal), "non-Literal found within a clause"
                lit_var = lit.get_variable()
                lit_sign = lit.get_sign()
                if lit_var in var_signs:
                    var_uniformity[lit_var] = False if var_signs[lit_var] == lit_sign else var_uniformity[lit_var]
                else:
                    var_signs[lit_var] = lit_sign
                    var_uniformity[lit_var] = True
        for clause in self.__proposition:
            for lit in clause:
                assert isinstance(lit, Literal)
                lit_var = lit.get_variable()
                lit_sign = lit.get_sign()
                if var_uniformity[lit_var]:
                    self.__variables[lit_var] = True if lit_sign == 'pos' else 'False'
                    self.__proposition.remove(clause)
                    break
        return changed

    def unit_clause_heuristic(self):
        changed = False
        uclauses = {} # variable : bool (True if lit sign is 'pos' else False)
        for clause in self.__proposition:
            # if the clause is empty: remove and continue in loop
            if not len(clause):
                self.remove(clause)
                continue
            # if the clause only has one literal in it, it is now a unit clause
            # add it to the back and continue in loop, hit it when get to it in added spot
            if len(clause) == 1:
                new_unit = clause[0]
                self.remove(clause)
                self.ADD(new_unit)
                continue
            # gather the unit caluses into a dict of their variables and sign
            # check for contradictions
            if isinstance(clause, Literal):
                lit_var = clause.get_variable()
                lit_sign = clause.get_sign()
                # gather variable and sign, check if the variable is already a key in the dict
                # if it is, check its sign against the one in the the dict at that key
                if lit_var in uclauses:
                    # if it's not the same sign, unsat by contradiction; can't have to literals,
                    # same variable 
                    if lit_sign != uclauses[lit_var]:
                        return 'unsat'
                else:
                    # if it's not in the dict, put it in the dict and set it's value to the literal's sign
                    uclauses[lit_var] = lit_sign
                    self.__variables[lit_var] = True if lit_sign == 'pos' else False
                # either way, remove it from the proposition as it can't affect its truthiness
                self.__proposition.remove(clause)
                changed = True
        for clause in self.__proposition:
            if isinstance(clause, Clause):
                for lit in clause:
                    assert isinstance(lit, Literal), f"{clause} contains {lit} which is not a Literal."
                    lit_var = lit.get_variable()
                    if lit_var in uclauses:
                        if lit.get_sign() == uclauses[lit_var]:
                            self.__proposition.remove(clause)
                            break
                        else:
                            clause.remove(lit)
                            continue
        return "changed" if changed else "unchanged"
    

class Clause(object):

    def __init__(self, *args) -> None:
        self.__clause = []
        self.__status = None
        for arg in args:
            if isinstance(arg, Literal):
                self.__clause.append(arg)
            elif isinstance(arg, Clause):
                for lit in arg:
                    assert isinstance(lit, Literal)
                    self.__clause.append(lit)
            elif isinstance(arg, set):
                self.ADD(arg)
            else:
                print("Clause object only accepts Literal or Clause objects as input.")
                raise TypeError
            # contradiction check:
        #TODO fix contradiction check
        len = len(self.__clause)
        for i in range(len):
            lit_sign = self.__clause[i].get_sign()
            for j in range(len):
                if self.__clause[i] == self.__clause[j] and i != j:
                    if self.__clause[j].get_sign() != lit_sign:
                        print(f"Contradition: The variable {lit.get_variable()} is contained within the clause more than once with opposite signs.")
                        raise AttributeError
                else:
                    self.remove(self.__clause[j])
                    len -= 1
                    continue
        self.set_status()

    
    def __str__(self) -> str:
        return f"{[str(lit) for lit in self.__clause]}"
    
    def __iter__(self):
        return iter(self.__clause)

    def set_status(self):
        none_in = False
        true_in = False
        for literal in self.__clause:
            assert isinstance(literal, Literal)
            if literal.get_calculated_val() is None:
                none_in = True
            elif literal.get_calculated_val():
                true_in = True
        if true_in:
            self.__status = True
        elif none_in and not true_in:
            self.__status = None
        elif not none_in and not true_in:
            self.__status = False

    def get_status(self):
        self.set_status()
        return self.__status
    
    def ADD(self, item):
        if isinstance(item, Literal):
            for lit in self.__clause:
                if lit == item:
                    if lit.get_sign() != item.get_sign():
                        print("The Clause contains a Literal with this variable of opposite sign: Contradiction")
                        raise AttributeError
                    else:
                        continue
            self.__clause.append(item)
        elif isinstance(item, Clause):
            if item.is_empty():
                print("An empty Clause object cannot be added to a Clause object")
                raise AttributeError
            for i in item:
                for lit in self.__clause:
                    if lit == i and lit.get_sign() != i.get_sign:
                        print("Contradiction: The Clause contains a Literal with this variable of opposite sign.")
                        raise AttributeError
                    else:
                        break
                self.__clause.append(i)
        else:
            print("Clause object only accepts Literal or non-negated Clause objects as input.")
            raise TypeError
        self.set_status()

    def remove(self, literal):
       #for i in range(num):
        self.__clause.remove(literal) 

    def NOT(self):
        """Move negations inside e.g. :
            a) ~(~a) = a
            c) ~(a v b) = ~a ∧ ~b"""
        negated = set()
        for instance in self.__clause:
            negated.add(instance.NOT())
        self.set_status()
        return negated
    
    def is_empty(self):
        return len(self.__clause) == 0
    
    def __len__(self):
        return len(self.__clause)
    
    def __iter__(self):
        return iter(self.__clause)
    
    def __getitem__(self, index):
        return self.__clause[index]
    
    # TODO fix implication function
def implies(clause1: Clause, clause2: Clause, proposition=None) -> Clause:
    res_clause = Clause()
    if isinstance(clause1, Clause):
        for lit in clause1:
            res_clause.ADD(lit)
    elif isinstance(clause1, Literal):
        res_clause.ADD(clause1)
    else:
        print("Implication can only be between Literals and Objects")
        raise TypeError
    res_clause.NOT()
    if isinstance(clause2, Clause):
        for lit in clause2:
            res_clause.ADD(lit)
    elif isinstance(clause2, Literal):
        res_clause.ADD(clause2)
    else:
        print("Implication can only be between Literals and Objects")
        raise TypeError
    return res_clause

# TODO implement a biconditional function
# def bicond(clause1: Clause, clause2: Clause, proposition=None) -> tuple(Clause):
#     ''''''
#     res_clause1 = implies(clause1, clause2)
#     res_clause2 = implies(clause1, clause2)
#     if proposition is not None:
#         assert isinstance(proposition, DPLL)
#         proposition.ADD(res_clause1)
#         proposition.ADD(res_clause2)
#     return (res_clause1, res_clause2)

def solve(*args: Literal)
