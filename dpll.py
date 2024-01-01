"""

Luke Marshall
DPLL solver object
"""
from typing import Any, Union, Iterator
from Literal import Literal
from Clause import Clause
import copy

class DPLL(object):
    """DPLL object contains a proposition in conjunctive normal form
    
    Properties:
        UNSAT: returned when the proposition is unsatisfiable
        SAT: returned when the propostion is satisfiable
        CHANGED: returned when the unit_clause_hueristic changes the proposition
        UNCHANGED: returned when the unit_clause_hueristic changes the proposition
        
    Attributes:
        variables: a dict of all the variables in every Literal in the proposition and their 
        corresponding boolean values; initialized to None, and finalized to their necessary 
        values for the proposition to be solved if it is satisfiable
        proposition: a list of Literal and/or Clause objects
        original: the original proposition before any dpll disregards or clause removals occur,
        used to replace the propostion after dpll algorithm takes place
        
    Important methods:
        ADD: adds a given Literal or Clause to the proposition
        solve: method used to implement dpll on proposition; returns 'sat' if proposition is 
        satisfiable, 'unsat' if otherwise
        solve_for_variables: uses the solve method to solve for the proposition, returns a dict of 
        the variables and their assigned boolean values to satisfy the proposition if it is satisfiable,'
        None if otherwise"""
    
    # Properties:
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
        self.__original = []
        for item in args: 
            if isinstance(item, set):
                # a negated clause produces a set of negated Literals that must individually 
                # be added to the proposition 
                for lit in item:
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
        self.__original = [copy.deepcopy(cl) for cl in self.__proposition]
            
    def __str__(self) -> str:
        """Returns: a string representation of the proposition"""
        return f"{[str(cl) for cl in self.__proposition]}"
    
    def __repr__(self) -> str:
        """Returns: a string representation of the proposition"""
        return f"{[repr(cl) for cl in self.__proposition]}"
    
    def get_proposition(self):
        """Returns: the proposition attribute"""
        return self.__proposition
    
    def get_variables(self) -> dict[str, Union[bool, None]]:
        """Returns: the variables attribute"""
        return self.__variables

    def ADD(self, item: Union[Literal, Clause, set[Literal]]):
        """Adds item to the proposition attribute

        Raises:
            TypeError if the object being added does not meet criteria"""
        # add the Clauses and Literals based on allowable types: 
        if isinstance(item, set):
            # a negated Clause produces a set of negated Literals; each must be added individually 
            for lit in item:
                if not isinstance(lit, Literal):
                    raise TypeError("""DPLL proposition can only be made up of 
                                    Literal and Clause objects.""")
                if (lit_var := lit.get_variable()) not in self.__variables:
                    self.__variables[lit_var] = None
                self.__proposition.append(lit)
                self.__original.append(copy.deepcopy(lit))
        elif isinstance(item, Literal):
            # Literals may be added directly, to proposition and variables
            if (item_var := item.get_variable()) not in self.__variables:
                self.__variables[item_var] = None
            self.__proposition.append(item)
            self.__original.append(copy.deepcopy(item))
        elif isinstance(item, Clause):
            # Clauses may be added directly, but the Literals they contains must be added to the 
            # variables individually
            if item.is_empty():
                return
            for lit in item:
                if (lit_var := lit.get_variable()) not in self.__variables:
                    self.__variables[lit_var] = None
            self.__proposition.append(item) # add the clause directly to the proposition
            self.__original.append(copy.deepcopy(item))
        else:
            raise TypeError("DPLL proposition can only be made up of Literal and Clause objects.")
        
    def __disregard(self, item: Union[Literal, Clause]):
        """Removes item from the proposition if it contains item
        Different than a pure removal because it does not attempt to remove the 
        variable(s) in the disregarded Literal(s) from the variable attribute.
        If given a Literal, the method will look for a unit clause, it will not find 
        it within a Clause. 
        
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
        """Returns: an iterator through the proposition attribute"""
        return iter(self.__proposition)
    
    def __getitem__(self, index: int) -> Union[Literal, Clause]:
        """Returns: the object in the proposition attribute at index"""
        return self.__proposition[index]
    
    def is_empty(self) -> bool:
        """Returns: a boolean representing if the proposition is empty or not"""
        return not len(self.__proposition)
    
    def __len__(self):
        """Returns: the length of the proposition list"""
        return len(self.__proposition)
    
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
    
    def solve_for_variables(self) -> Union[dict, None]:
        """Uses the solver process to set the variable values in the variables attribute.
        
        Returns: either None if the proposition is unsatisfiable, or the dict of variables
        and their boolean values used to satisfy the proposition"""
        
        res = self.solve()
        if res == 'sat':
            vars = self.__variables.copy()
            for var in vars:
                if vars[var] is None:
                    vars[var] = 'either'
            return vars
        else:
            return None
        
    def solve(self) -> str:
        """ replaces the resulting proposition with the original proposition after dpll method call
        
        Returns: a string representing if the proposition is satisfiable or not
                'sat' if satisfiable
                'unsat' if not satisfiable """
        
        res = self.dpll()
        self.__proposition = [copy.deepcopy(cl) for cl in self.__original]
        return res
    
    def dpll(self) -> str:
        """Implements the DPLL algorithm to find if the proposition is satisfiable or unsatisfiable
        
        Returns: a string representing if the proposition is satisfiable or not
                'sat' if satisfiable
                'unsat' if not satisfiable"""
        
        self.simplify()
        # Base case: the proposition is True so it contains only True clauses, therefore the 
        # proposition will eventually be empty if all True clauses are removed
        if self.is_empty():
            # an empty proposition is satisfiable
            return DPLL.SAT
        values = set()
        for clause in self.__proposition:
            if isinstance(clause, Literal):
                values.add(clause.get_calculated_val())
            elif isinstance(clause, Clause):
                values.add(clause.get_status())
        if (False in values):
            # if any clause has the external value of False, the proposition is unsatisfiable
            return DPLL.UNSAT
        elif (None in values):
            # if any clause has the external value of None, the proposition satisfiability is
            # still ambiguous
            pass
        elif (True in values):
            # None and False already not in values, so only things in the proposition are clauses
            # with the external value of True, ∴ the proposition is satisfiable
            return DPLL.SAT
        
        # apply unit clause heristic until the proposition is either unsat or did not change with
        # most recent call to UCH
        res = self.unit_clause_heuristic()
        if res == DPLL.UNSAT:
            return res
        elif res == DPLL.CHANGED:
            return self.solve()
        
        # apply pure clause hueristic until the proposition did not change with most recent call 
        # to PCH
        res2 = self.pure_clause_hueristic()
        if res2:
            return self.solve() 
        
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
        # assigns the guess value to the variable that makes the external value of the Literal True
        # so at least one Clause may be removed from the proposition
        self.__guess(guess_var, True if guess_sign == 'pos' else False)
        self.simplify()

        # check the guess:          
        res3 = self.solve()
        if res3 == 'sat':
            return res3
        else:
            self.__proposition = dpll_cp.get_proposition()
            self.__variables = dpll_cp.get_variables()

        # First guess was a failure, guess the opposite value:
        self.__guess(guess_var, False if guess_sign == 'pos' else True)
        self.simplify()

        # Second guess is either True XOR the resulting failure means the proposition is unsat
        return self.solve()
    
    def simplify(self):
        """Simplifies the proposition by disregarding the Literals with an external value of True;
        also the Clauses with an external value of True, or that are empty, and substitutes the 
        Literal contained within a Clause of length 1 in for the Clause"""
        to_disregard = []
        for i, item in enumerate(self):
            if isinstance(item, Literal):
                if item.get_calculated_val():
                    to_disregard.append(item)
            elif isinstance(item, Clause):
                if item.get_status() or item.is_empty():
                    to_disregard.append(item)
                    continue
                elif len(item) == 1:
                    to_disregard.append(item)
                    self.ADD(item[0])
                    continue
                for lit in item:
                    if lit.get_calculated_val() == False:
                        self.__proposition[i] = item.remove(lit)
            else:
                raise TypeError("Proposition may only contain Literals and Clauses")
        for item in to_disregard:
            self.__disregard(item)

    def unit_clause_heuristic(self) -> str:
            '''Sets the value of any unit clauses so their external calculated value is True.
            Checks the proposition for any sign contradictions on the unit clauses.
            Removes the unit clauses. Removes literals from clauses if they have a negated sign
            but the same variable as a unit clause; removes the clause from the proposition 
            if the sign is the same.
            
            Returns: string representing if the proposition was changed in the process or if a 
            contradiction was found, allowing the proposition to be labeled unsatisfiable'''

            uclauses = {} # Literal variable (str) : Literal sign (str)
            for item in self:
                # finds all unit clauses and adds their attributes to uclauses, sets the status 
                # of the Literal, checks there are no sign contradictions among the unit clauses
                if isinstance(item, Literal):
                    lit_var = item.get_variable()
                    lit_sign = item.get_sign()
                    if lit_var in uclauses:
                        # if the Literal variable is in uclauses, checks the sign is the same as in
                        # this Literal; if not, unsat by contradiction 
                        if lit_sign != uclauses[lit_var]:
                            return DPLL.UNSAT # by contradiction
                    else:
                        uclauses[lit_var] = lit_sign
                        self.__variables[lit_var] = True if lit_sign == 'pos' else False
                    item.set_status(self.__variables[lit_var])
            self.simplify()

            for clause in self:
                # If the Literal variable is in uclauses, sets the status of the Literal 
                # according to the variables attribute
                if isinstance(clause, Clause):
                    for lit in clause:
                        assert isinstance(lit, Literal), "Non-Literal found within Clause"
                        if (lit_var := lit.get_variable()) in uclauses:
                            lit.set_status(self.__variables[lit_var])
            self.simplify()
            return DPLL.CHANGED if len(uclauses) else DPLL.UNCHANGED

    def pure_clause_hueristic(self) -> bool:
        '''Sets the value of any pure clauses so that their external value is True. Removes all 
         caluses containig those clauses
         
         Returns: bool representing if the proposition was changed at all in the process
         
         Raises: AssertionError if any assertions found to be untrue'''
        
        changed = False
        # Literal variable (str) : Tuple(Literal sign (str), <---                            
        var_signs_uniformity = {} # ---> bool representing the uniformity of the signs throughout)
        for clause in self:
            # Checks that a given variable has sign uniformity throughout the proposition,
            # the status of this check is noted in var_signs_uniformity
            if isinstance(clause, Clause):
                for lit in clause:
                    assert isinstance(lit, Literal), "Non-Literal found within a Clause"
                    lit_var = lit.get_variable()
                    lit_sign = lit.get_sign()
                    if lit_var in var_signs_uniformity:
                        if var_signs_uniformity[lit_var][0] != lit_sign:
                            var_signs_uniformity[lit_var][1] = False
                    else:
                        var_signs_uniformity[lit_var] = [lit_sign, True]

        uniform_vars = set(var for var in var_signs_uniformity if var_signs_uniformity[var][1])
        for item in self:
            # Literals whose value in var_uniformity is True assigned a bool such that their 
            # external values are True and the clauses containing them may be disregarded from 
            # the proposition 
            if isinstance(item, Literal):
                if (lit_var := item.get_variable()) in uniform_vars:
                    lit_sign = lit.get_sign()
                    self.__variables[lit_var] = True if lit_sign == 'pos' else False
                    lit.set_status(self.__variables[lit_var])
                    changed = True
            elif isinstance(item, Clause):
                for lit in item:
                    assert isinstance(lit, Literal), "Non-Literal found within a Clause"
                    if (lit_var := lit.get_variable()) in uniform_vars:
                        lit_sign = lit.get_sign()
                        self.__variables[lit_var] = True if lit_sign == 'pos' else False
                        lit.set_status(self.__variables[lit_var])
                        changed = True
        self.simplify()
        return changed
    
    def __guess(self, var: str, val: bool):
        self.__variables[var] = val
        for clause in self:
            assert isinstance(clause, Clause)
            for lit in clause:
                assert isinstance(lit, Literal)
                if lit.get_variable() == var:
                    lit.set_status(val)



