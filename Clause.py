"""Author: Luke Marshall

This module contains the definition of a Clause object to be used in a DPLL solver"""
from typing import Union, Iterator
import copy
from Literal import Literal


class Clause(object):
    """Clause object in a conjunctive normal form proposition. Secondary element of a proposition,
    contains a number of Literals. Represents a list of disjunct Literals.
    
    Attributes:
        clause: a list of Literal objects
        status: boolean representing the external status of the clause
        based on the external statuses of the individual Literals it contains"""
    
    def __init__(self, *args: list[Union['Clause', Literal]]):
        """Constructor method for the Clause object
        
        Examples:
        a = Literal('a')
        b = Literal('b')
        c = Literal('c')
        cl = Clause(a, b)
        cl2 = Clause(cl, c)
        """
        self.__clause = []
        self.__status = None # based on the statuses of the Literals it contains
        for arg in args:
            if isinstance(arg, Literal): # if it's a Literal, add it directly
                self.__clause.append(arg)
            elif isinstance(arg, Clause): 
                # if it's a Clause, add the literals inside it to the new Clause
                for lit in arg:
                    assert isinstance(lit, Literal)
                    self.__clause.append(lit)
            elif isinstance(arg, list):
                for item in arg:
                    self.ADD(item)
            else:
                raise TypeError("""Clause object only accepts Literal or non-negated 
                                Clause objects as input.""")
        # initialize status:
        self.set_status()
        # remove duplicates:
        self.__filter_duplicates()

    def __str__(self) -> str:
        """Returns: string representation of the Literals in clause attribute
        
        Example:
        >>> a = Literal('a')
        >>> b = Literal('b')
        >>> cl = Clause(a, b)
        >>> print(cl)
        "['+a', '+b']"
        >>> str(cl)
        "['+a', '+b']"
        """
        return f"{[str(lit) for lit in self.__clause]}"
    
    def __repr__(self):
        """Returns: string representation of the Literals in clause attribute
        
        Example:
        >>> a = Literal('a')
        >>> b = Literal('b')
        >>> cl = Clause(a, b)
        >>> repr(cl)
        "['+a', '+b']"
        """
        return f"{[repr(lit) for lit in self.__clause]}"

    def set_status(self):
        """checks the external truth value of Literals in the clause attribute to calculate and
        set the status attribute
        
        Example:
        >>> a = Literal('a')
        >>> a.set_internal_status(False)
        >>> b = Literal('b')
        >>> b.set_status()
        >>> cl = Clause(a)
        >>> cl.set_status()
        >>> cl.__status == False
        True
        >>> cl.ADD(b)
        >>> cl.set_status()
        >>> cl.__status == True
        True
        """
        if self.is_empty():
            self.__status = False
        elif self.__tautology_check():
            self.__status = True
        else:
            none_in = true_in = False
            for lit in self.__clause:
                assert isinstance(lit, Literal)
                lit_val = lit.get_external_status()
                if lit_val:
                    true_in = True
                elif lit_val == None:
                    none_in = True
            if true_in:
                self.__status = True
            elif none_in:
                self.__status = None
            else:
                self.__status = False
            

    def __tautology_check(self) -> bool:
        """Returns: a boolean representing if the clause attribute contains any
        Literals with the same variables and opposite signs
        
        >>> a = Literal('a')
        >>> a2 = a.NOT()
        >>> cl = Clause(a, a2)
        >>> cl.__tautology_check()
        True
        """
        var_dict = {} # Literal variable : Literal sign
        for lit in self.__clause:
            assert isinstance(lit, Literal)
            lit_var = lit.get_variable()
            lit_sign = lit.get_sign()
            if lit_var in var_dict:
                if not lit_sign == var_dict[lit_var]:
                    return True
            else:
                var_dict[lit_var] = lit_sign
        return False
    
    def __filter_duplicates(self):
        """Removes any duplicates from clause attribute"""
        seen = set()
        self.__clause = [obj for obj in self.__clause if 
                         not (obj in seen or seen.add(obj))]

    def get_status(self) -> bool:
        """Returns: a boolean representing the status of the clause after setting it
        
        Example:
        >>> a = Literal('a')
        >>> a.set_internal_status(False)
        >>> b = Literal('b')
        >>> b.set_status()
        >>> cl = Clause(a)
        >>> cl.set_status()
        >>> cl.get_status() 
        False
        >>> cl.ADD(b)
        >>> cl.get_status()
        True
        """
        self.set_status()
        return self.__status

    def ADD(self, item: Union['Clause', Literal]) -> 'Clause':
        """Adds item to the clause attribute if it is not a duplicate.
        Sets the status attribute to True if the variable in any of the added Literals is already
        in the clause in an opposite signed Literal.
        
        Raises: TypeError if wrong type given as item
        
        Example:
        >>> a = Literal('a')
        >>> b = Literal('b')
        >>> c = Literal('c')
        >>> cl = Clause(a, b)
        >>> cl2 = Clause()
        >>> cl2.ADD(c)
        >>> cl2.ADD(cl)
        >>> print(cl2)
        "['+a', '+b', '+c']"
        """
        new_clause = copy.copy(self)
        if isinstance(item, Literal):
            matched = False
            for lit in new_clause:
                if lit == item:
                    if lit.get_sign() != item.get_sign():
                        self.__status = True
                    else:
                        matched = True
            if not matched:
                self.__clause.append(item)
        elif isinstance(item, Clause):
            if item.is_empty():
                return
            for i in item:
                matched = False
                for lit in new_clause:
                    if lit == i:
                        if lit.get_sign() != i.get_sign():
                            self.__status = True
                        else:
                            matched = True
                if not matched:
                    self.__clause.append(i)
        else:
            raise TypeError("""Clause object only accepts Literal or non-negated 
                            Clause objects as input.""")
        new_clause.set_status()
        return new_clause

    def remove(self, item: Literal) -> 'Clause':
        """Removes item from clause attribute
        Does not remove the variables of the Literals contained in the clause from any DPLL 
        variables attributes if the clause is already contained within a DPLL

        Returns: new clause same as original but with item removed
        
        Example:
        >>> a = Literal('a')
        >>> b = Literal('b')
        >>> cl = Clause(a, b)
        >>> cl2 = cl.remove(b)
        >>> print(cl)
        "['+a', '+b']"
        >>> print(cl2)
        "['+a']"
        """
        if not isinstance(item, Literal):
            raise TypeError("Only Literal object types may be removed from a Clause")
        if item not in self:
            raise ValueError("Literal not in Clause")
        reduced_clause = copy.deepcopy(self)
        reduced_clause._Clause__clause.remove(item) 
        reduced_clause.set_status()
        return reduced_clause

    def NOT(self) -> set[Literal]:
        """Negates the clause and returns the negation as a set of negated Literals
        Does not change self

        Moves negations inside clause e.g. :
            ~(~a) = a
            ~(a v b) = ~a ∧ ~b
            
        Example:
        >>> a = Literal('a')
        >>> b = Literal('b')
        >>> cl = Clause(a, b)
        >>> cl2 = cl.NOT()
        >>> print(cl)
        "['+a', '+b']"
        >>> print(cl2)
        {'-a', '-b'}
        """
        negated = copy.deepcopy(self)
        negated_set = set()
        for lit in negated:
            negated_set.add(lit.NOT())
        return negated_set
    
    def get_clause(self):
        """Returns: the clause attribute
        
        Example:
        >>> a = Literal('a')
        >>> b = Literal('b')
        >>> cl = Clause(a, b)
        >>> cl.get_clause:
        ['+a', '+b']
        """
        return self.__clause
    
    def is_empty(self) -> bool:
        """Returns: boolean representing if clause attibute length is 0
        
        Example:
        >>> cl = Clause()
        >>> cl.is_empty()
        True

        >>> a = Literal('a')
        >>> cl.ADD(a)
        >>> cl.is_empty()
        False
        """
        return not len(self.__clause)
    
    def __len__(self) -> int:
        """Returns: int number of items in clause attribute
        
        Example:
        >>> a = Literal('a')
        >>> b = Literal('b')
        >>> c = Literal('c')
        >>> cl = Clause(a, b)
        >>> cl2 = Clause(c, cl)
        >>> len(cl2)
        3
        """
        return len(self.__clause)
    
    def __iter__(self) -> Iterator[Literal]:
        """Returns: an iterator for the clause list attribute"""
        return iter(self.__clause)
    
    def __getitem__(self, index: int) -> Literal:
        """Returns: the Literal in the clause list attribute at index"""
        return self.__clause[index]
    
    def __copy__(self) -> 'Clause':
        """Implements a shallow copy of the Clause
        Returns: a shallow copy of the Clause"""
        cp = Clause()
        cp.__clause = self.__clause.copy()
        cp.set_status
        return cp
    
    def __deepcopy__(self, memo: dict) -> 'Clause':
        """Implements a deep copy of self
        Returns: a deep copy of self"""
        cp = Clause()
        memo[id(self)] = cp
        cp.__clause = [copy.deepcopy(lit, memo) for lit in self.__clause]
        cp.set_status()
        return cp
    
    def __eq__(self, other: 'Clause') -> bool:
        """Returns: a boolean representing if a List or another Clause contains the same 
        literals as are in clause"""
        same = False
        if not isinstance(other, (Clause, list)):
            return False
        elif isinstance(other, Clause):
            same = True if self.__clause == other.__clause else same
        else:
            same = True if self.__clause == other else same
        return same
    
    def __contains__(self, item: Literal) -> bool:
        """Returns: a boolean representing if item (Literal) is in the clause attribute"""
        if not isinstance(item, Literal):
            raise TypeError("A Clause cannot contain any non-Literal objects")
        return item in self.__clause