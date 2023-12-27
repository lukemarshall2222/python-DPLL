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
from typing import Union, Iterator
from Literal import Literal
from Clause import Clause

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
        variables attribute dict by adding each Literal variable and initializing its value 
        to None.
        
        Raises:
            TypeError if the object being added does not meet criteria"""
        
        self.__variables = {}
        self.__proposition = []
        for item in args: 
            if isinstance(item, set): 
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

    def sat(self) -> str:
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


