"""

Luke Marshall
DPLL solver
"""
from typing import Union, Iterator
from Literal import Literal
from Clause import Clause
import copy

class DPLL(object):
    """DPLL object contains a proposition in conjunctive normal form
    
    Class Attributes:
        UNSAT: returned when the proposition is unsatisfiable
        SAT: returned when the propostion is satisfiable
        CHANGED: returned when the unit_clause_hueristic changes the proposition
        UNCHANGED: returned when the unit_clause_hueristic changes the proposition
        
    Instance Attributes:
        variables: a dict of all the variables in every Literal in the proposition and their 
        corresponding boolean values; initialized to None, and finalized to their necessary 
        values for the proposition to be solved if it is satisfiable
        proposition: a list of Literal and/or Clause objects"""
    
    # Class Attributes:
    UNSAT = 'unsat'
    SAT = 'sat'
    CHANGED = 'changed'
    UNCHANGED = 'unchanged'

    def __init__(self, *args: Union[Literal, Clause, set[Literal]]):
        """Constructor function produces the proposition for the DPLL by appropriately
        adding the Literals and Clauses to the proposition attribute. Also produces the 
        variables attribute dict by adding each Literal variable as a key and initializing its 
        value to None.
        
        Raises:
            TypeError if the object being added does not meet criteria"""
        
        self.__variables = {}
        self.__proposition = []
        for item in args: 
            if isinstance(item, set):
                # a negated clause produces a set of negated Literals that must individually 
                # be added to the proposition 
                while len(item):
                    lit = item.pop()
                    if not isinstance(lit, Literal):
                        raise TypeError("""DPLL proposition can only be made up of 
                                        Literal and Clause objects.""")
                    self.__variables[lit.get_variable()] = None
                    self.__proposition.append(lit)
            elif isinstance(item, Literal):
                    self.__proposition.append(item)
                    self.__variables[item.get_variable()] = None
            elif isinstance(item, Clause):
                self.__proposition.append(item)
                for lit in item:
                    self.__variables[lit.get_variable()] = None
            else:
                raise TypeError("A DPLL object only accepts Literal and Clause objects in the proposition.")


    def ADD(self, item: Union[Literal, Clause, set[Literal]]):
        """Adds item to the proposition attribute

        Raises:
            TypeError if the object being added does not meet criteria"""
        # add the Clauses and Literals based on allowable types: 
        if isinstance(item, set): 
            while len(item):
                lit = item.pop()
                if not isinstance(lit, Literal):
                    raise TypeError("""DPLL proposition can only be made up of 
                                    Literal and Clause objects.""")
                self.__variables[lit.get_variable()] = None
                self.__proposition.append(lit)
        elif isinstance(item, Literal):
            self.__variables[item.get_variable()] = None
            self.__proposition.append(item) # add the literal directly to the proposition
        elif isinstance(item, Clause):
            if item.is_empty():
                return
            for lit in item:
                self.__variables[lit.get_variable()] = None
            self.__proposition.append(item) # add the clause directly to the proposition
        else:
            raise TypeError("DPLL proposition can only be made up of Literal and Clause objects.")
        
    def remove(self, item: Union[Literal, Clause]):
        """Removes item from the proposition if it contains item
        
        Raises:
            TypeError if item is not a Literal or a Clause"""
        
        if not isinstance(item, (Literal, Clause)):
            raise TypeError("A DPLL may only contain Literals or Clauses")
        if item in self:
            self.__proposition.remove(item)
    
    def __contains__(self, item: Union[Literal, Clause]) -> bool:
        """Returns: a boolean representing if the proposition contains item
        
        Raises:
            TypeError if item is not a Literal or a Clause"""
        
        if not isinstance(item, (Literal, Clause)):
            raise TypeError("A DPLL may only contain Literals or Clauses")
        return item in self.__proposition
    
    def __iter__(self) -> Iterator:
        """Returns: an iterator """
        return iter(self.__proposition)
    
    def __getitem__(self, index: int) -> Union[Literal, Clause]:
        """Returns: the object in the proposition at index"""
        return self.__proposition[index]
    
    def is_empty(self) -> bool:
        """Returns: a boolean representing if the proposition is empty or not"""
        return not len(self.__proposition)
    
    def __copy__(self) -> 'DPLL':
        """Implements a shallow copy of the DPLL
        Returns: a shallow copy of the DPLL"""
        cp = DPLL()
        cp._DPLL__proposition = self.__proposition.copy()
        cp._DPLL__variables = self.__variables.copy()
        return cp
    
    def __deepcopy__(self, memo) -> 'DPLL':
        """Implements a deep copy of the DPLL
        Returns: a deep copy of the DPLL"""
        cp = DPLL()
        memo[id(self)] = cp
        cp._DPLL__proposition = [copy.deepcopy(item, memo) for item in self.__proposition]        
        cp._DPLL__variables = copy.deepcopy(self.__variables, memo)
        return cp

    def sat(self) -> str:
        """Returns: a string representing if the proposition is satisfiable or not
                'sat' if satisfiable
                'unsat' if not satisfiable"""
        # Base case: the proposition is True so it contains only True clauses, therefore the 
        # proposition will eventually be empty if all True clauses are removed
        if self.is_empty():
            return DPLL.SAT
        values = set()
        for clause in self.__proposition:
            if isinstance(clause, Literal):
                values.add(clause.get_calculated_val())
            elif isinstance(clause, Clause):
                values.add(clause.get_status())
        if (True in values) and (False in values):
            raise ValueError("contradiction: cannot be sat and unsat simultaneously")
        elif (None in values):
            pass
        elif (True in values):
            return DPLL.SAT
        elif (False in values):
            return DPLL.UNSAT
        
        # apply unit clause heristic until the proposition is either unsat or did not change with
        # most recent call to UCH
        res = self.unit_clause_heuristic()
        if res == DPLL.UNSAT:
            return res
        elif res == DPLL.CHANGED:
            return self.sat()
        
        # apply pure clause hueristic until the proposition did not change with most recent call 
        # to UHC
        res2 = self.pure_clause_hueristic()
        if res2:
            return self.sat() 
        
        # apply guess and check
        dpll_cp = copy.deepcopy(self)
        least = len(self.__proposition[0])
        guess = self.__proposition[0][0]
        for clause in self.__proposition:
            # finds the Clause containing the smallest number of Literals to make guess more likely
            # to be correct
            if len(clause) < least:
                least = len(clause)
                guess = clause[0]
        guess_var = guess.get_variable()
        guess_sign = guess.get_sign()
        # assigns the the value to the variable that makes the external value of the Literal True
        # so at least one Clause may be removed from the proposition
        self.__variables[guess_var] = True if guess_sign == 'pos' else False
        removals = []
        for i, clause in enumerate(self.__proposition):
            # removes approprite Literals and Clauses according to the guess
            assert isinstance(clause, Clause)
            for lit in clause:
                assert isinstance(lit, Literal)
                if lit.get_variable() == guess_var:
                    if lit.get_sign() == 'pos':
                        removals.append(i)
                        break
                    else:
                        self.__proposition[i] = clause.remove(lit)
        for num in removals:
            self.remove[self.__proposition[num]]  

        # check the guess:          
        res3 = self.sat()
        if res3 == 'sat':
            return res3
        else:
            self = dpll_cp

        # First guess was a failure, guess the opposite value:
        removals = []
        self.__variables[guess] = False
        for i, clause in enumerate(self.__proposition):
            assert isinstance(clause, Clause)
            for lit in clause:
                assert isinstance(lit, Literal)
                if lit.get_variable() == guess:
                    if lit.get_sign() == 'neg':
                        removals.append(i)
                        break
                    else:
                        self.__proposition[i] = clause.remove(lit)
        for num in removals:
            self.remove(self.__proposition[num])

        # Second guess is either True or the resulting failure means the proposition is unsat
        return self.sat()

    def unit_clause_heuristic(self) -> str:
            '''Sets the value of any unit clauses so their external calculated value is True.
            Checks the proposition for any sign contradictions on the unit clauses.
            Removes the unit clauses. Removes literals from clauses if they have a negated sign
            but the same variable as a unit clause; removes the clause from the proposition 
            if the sign is the same.
            
            Returns: string representing if the proposition was changed in the process or if a 
            contradiction was found, allowing the proposition to be labeled unsatisfiable'''
            uclauses = {} # Literal variable (str) : Literal sign (str)  
            for item in self.__proposition:
                # iterate through proposition, remove all empty clauses and tranform Clauses of
                # length 1 to unit clauses (Literals) 
                if isinstance(item, Clause):
                    if item.is_empty():
                        self.remove(item)
                    elif len(item) == 1:
                        new_unit = item[0]
                        self.remove(item)
                        self.ADD(new_unit)

            for item in self.__proposition:
                # finds all unit clauses and adds their attributes to uclauses if they are not 
                # already in it and remove the Literal from the proposition, otherwise check that 
                # the signs match between the two Literals; if they don't, return unsat by 
                # contradiction
                if isinstance(item, Literal):
                    lit_var = item.get_variable()
                    lit_sign = item.get_sign()
                    if lit_var in uclauses:
                        # if the Literal variable is in uclauses, checks the sign is the same as in
                        # this Literal; if not, unsat by contradiction 
                        if lit_sign != uclauses[lit_var]:
                            return 'unsat' # by contradiction
                    else:
                        uclauses[lit_var] = lit_sign
                        self.__variables[lit_var] = True if lit_sign == 'pos' else False
                    self.__proposition.remove(item)

            for i, clause in enumerate(self.__proposition):
                # If the Literal variable is in uclauses, marks clause for removal from the 
                # proposition if the signs match; removes the Literal from the Clause if the 
                # signs don't match
                removals = []
                assert isinstance(clause, Clause), "Unit clause found in proposition after unit clause removal"
                for lit in clause:
                    assert isinstance(lit, Literal), "Non-Literal found within Clause"
                    lit_var = lit.get_variable()
                    if lit_var in uclauses:
                        if lit.get_sign() == uclauses[lit_var]:
                            removals.append(i)
                            break
                        else:
                            self.__proposition[i] = clause.remove(lit)
                for num in removals:
                    # removes the clauses marked for removal earlier
                    self.__proposition.remove(self.__proposition[num])

            return DPLL.CHANGED if len(uclauses) else DPLL.UNCHANGED

    def pure_clause_hueristic(self) -> bool:
        '''Sets the value of any pure clauses so that their external value is True. Removes all 
         caluses containig those clauses
         
         Returns: bool representing if the proposition was changed at all in the process
         
         Raises: AssertionError if any assertions found to be untrue'''
        
        changed = False
        var_signs = {} # Literal variable (str) : Literal sign (str)
        var_uniformity = {} # Literal variable (str) : boolean representing literal sign uniformity
        for clause in self.__proposition:
            # Checks that a given variable has sign uniformity throughout the proposition,
            # the status of this check is noted in var_uniformity
            assert isinstance(clause, Clause), "Non-Clause found during pure clause check"
            for lit in clause:
                assert isinstance(lit, Literal), "Non-Literal found within a Clause"
                lit_var = lit.get_variable()
                lit_sign = lit.get_sign()
                if lit_var in var_signs:
                    if var_signs[lit_var] != lit_sign:
                        var_uniformity[lit_var] = False
                else:
                    var_signs[lit_var] = lit_sign
                    var_uniformity[lit_var] = True

        for clause in self.__proposition:
            # Literals whose value in var_uniformity is True assigned a bool such that their 
            # external values are True and the clauses containing them may be removed from 
            # the proposition 
            for lit in clause:
                assert isinstance(lit, Literal), "Non-Literal found within a Clause"
                lit_var = lit.get_variable()
                if var_uniformity[lit_var]:
                    lit_sign = lit.get_sign()
                    self.__variables[lit_var] = True if lit_sign == 'pos' else 'False'
                    self.__proposition.remove(clause)
                    changed = True
                    break
        return changed


