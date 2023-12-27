"""

Luke Marshall
DPLL solver

The solver uses a proposition in conjunctive normal form to designate whether 
or not it is satisfiable by assigning boolean values to each variable.
ANDs are implicit in the proposition between each of the clauses. 
ORs are implicit in between Literals in the Clauses.
All literals with the same variable name have the same underlying boolean
value, but may have different external values depending on their signs.
If the external value of a unit clause is True it may be removed from the proposition
because it can no longer cause it to be unsatisfiable. If the external value of a 
Literal contained within a Clause is True, the status of the Clause is therefore True 
and the Clause may be removed from the proposition because it can no longer cause the 
proposition to be unsatisfiable. If the external value of a Literal contained within a 
Clause is False, the Literal may be removed from the Clause because it can no longer 
contribute to the Clause being True. A Clause containing a single Literal becomes a 
unit clause.
The proposition is solved by recursion using the unit clause heuristic, 
the pure clause heuristic, and guess and check.
The unit clause heuristic is used to set all unit clauses so their external 
values are True, then they are removed from the proposition, and the clauses are 
seached for any Literals with the same variable name. If the found Literal has the 
same sign as the unit clause, the Clause containing it is removed; if it has the 
opposite sign, it is removed from the Clause. 
The pure clause heuristic is used to find Literals that have the same sign within 
all the Clauses that hold them. Their value is set such that their external values are True,
and the Clauses are removed from the proposition.
If the proposition only contains clauses with the external value of True, or is an empty 
proposition, it is deemed satisfiable; else it is deemed unsatisfiable.
If the proposition contains two unit clauses with the same variable name but opposite signs, 
it is unsatisfiable by contradiction.
The variable names and their values are tracked as the solver progresses so that if it is 
satisfiable they may be returned.
"""
from Literal import Literal
from Clause import Clause

# Constants:
UNSAT = 'unsat'
SAT = 'sat'
CHANGED = 'changed'
UNCHANGED = 'unchanged'


class DPLL(object):
    """DPLL object contains a proposition in conjunctive normal form"""

    def __init__(self, *args) -> None:
        self.__variables = {}
        self.__proposition = []
        for item in args:
            if isinstance(item, set):
                while len(item):
                    x = item.pop()
                    if not isinstance(x, (Clause, Literal)):
                        raise TypeError("""DPLL proposition can only be made up of 
                                        Literal and Clause objects.""")
                    self.__variables[x.get_variable()] = None
                    self.__proposition.append(x)
            elif isinstance(item, Literal):
                    self.__proposition.append(item)
                    self.__variables[item.get_variable()] = None
            elif isinstance(item, Clause):
                self.__proposition.append(item)
                for lit in item:
                    self.__variables[lit.get_variable()] = None
            else:
                raise TypeError("A DPLL object only accepts Literal and Clause objects in the proposition.")


    def ADD(self, item):
        if isinstance(item, set): 
            # negating a clause produces separated negated literals that must be 
            # added individually
            while len(item):
                x = item.pop()
                if not isinstance(x, (Clause, Literal)):
                    raise TypeError("""DPLL proposition can only be made up of 
                                    Literal and Clause objects.""")
                self.__variables[x.get_variable()] = None
                self.__proposition.append(x)
        elif isinstance(item, Literal):
            self.__variables[item.get_variable()] = None
            self.__proposition.append(item) # add the literal directly to the proposition
        elif isinstance(item, Clause):
            for lit in item:
                self.__variables[lit.get_variable()] = None
            self.__proposition.append(item) # add the clause directly to the proposition
        else:
            raise TypeError("DPLL proposition can only be made up of Literal and Clause objects.")
        
    def remove(self, clause):
        if clause in self.__proposition:
            self.__proposition.remove(clause)
    
    def __iter__(self):
        return iter(self.__proposition)
    
    def __getitem__(self, index):
        return self.__proposition[index]
    
    def is_empty(self):
        return not len(self.__proposition)

    def sat(self):
        """Returns if the proposition is satisfiable or not"""
        # check if all the clauses in the proposition are true, if they are, the proposition is satisfied
        if self.is_empty():
            return "sat"
        sat = unsat = True
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
        '''Sets tha value of any pure clauses so that their outward value is True. Removes all 
         caluses containig those clauses
         
         Returns: bool representing if the proposition was changed at all in the process'''
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

    """TODO: make it so if a clause is culled down to a single literal, change it to a unit clause"""
    def unit_clause_heuristic(self):
        '''Sets the value of any unit clauses so their outward calculated value is True.
        Checks the proposition for any sign contradictions on the unit clauses.
        Removes the unit clauses. Removes literals from clauses if they have a negated sign
        if they have the same variable as a unit clause; removes the clause from the proposition 
        if the sign is positive.
        
        Returns: string representing if the proposition was changed in the process or if a contradiction
        was found, allowing the proposition to be labeled unsatisfiable'''
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
    
