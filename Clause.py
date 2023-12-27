from typing import Union, Iterator
import copy
from Literal import Literal


class Clause(object):
    """Clause object in a conjunctive normal form proposition 
    
    Instance Attributes:
        clause: a list of Literal objects
        status: boolean representing the calculated value of the clause
        based on the calculated values of the individual """
    
    def __init__(self, *args: list[Union['Clause', Literal]]):
        """Initializes the Clause object"""
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
        # status checks:
        self.set_status()
        # remove duplicates
        self.__filter_duplicates()

    def set_status(self):
        """checks the status of Literals in the clause attribute for their statuses
        to calculate and set the status attribute"""
        none_in = true_in = False
        for lit in self.__clause:
            lit_val = lit.get_calculated_val()
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
        
        self.__status = True if self.__tautology_check() else self.__status

        if self.is_empty():
            self.__status = None

    def __tautology_check(self) -> bool:
        """Returns: a boolean representing if the clause attribute contains
        Literals with the same variables and opposite signs"""
        var_dict = {} # variable name: sign
        for lit in self.__clause:
            lit_var = lit.get_variable()
            lit_sign = lit.get_sign()
            if lit_var in var_dict:
                if not lit_sign == var_dict[lit_var]:
                    return True
            else:
                var_dict[lit_var] = lit_sign
        return False

    def get_status(self) -> bool:
        """Returns: a boolean represening the status of the clause"""
        self.set_status()
        return self.__status
    
    def __filter_duplicates(self):
        """Removes any duplicates from clause attribute"""
        seen = set()
        self.__clause = [obj for obj in self.__clause if 
                         not (obj in seen or seen.add(obj))]

    def __str__(self) -> str:
        """Returns: string representation of the Literals in clause attribute"""
        return f"{[str(lit) for lit in self.__clause]}"
    
    def __repr__(self):
        """Returns: string representation of the Literals in clause attribute"""
        return f"{[repr(lit) for lit in self.__clause]}"

    def ADD(self, item: Union['Clause', Literal]) -> 'Clause':
        """Adds item to the clause attribute if it is not already in clause.
        sets the status attribute to True if the variable is already in the clause with the opposite sign
        
        Raises: 
            AttributeError if contradiction is found
            TypeError if wrong type given as item"""
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
        """removes item from clause attribute
        Returns: new clause same as original but with item removed"""
        if not isinstance(item, Literal):
            raise TypeError("Only Literal object types may be removed from a Clause")
        if item not in self:
            raise ValueError("Literal not in Clause")
        reduced_clause = copy.copy(self)
        reduced_clause._Clause__clause.remove(item) 
        reduced_clause.set_status()
        return reduced_clause

    def NOT(self) -> set:
        """Negates the clause and returns the negation as a set
        Does not change actual clause attribute

        Moves negations inside clause e.g. :
            ~(~a) = a
            ~(a v b) = ~a ∧ ~b"""
        negated = copy.copy(self)
        negated_set = set()
        for lit in negated:
            negated_set.add(lit.NOT())
        return negated_set
    
    def get_clause(self):
        """Returns: the clause list attribute"""
        return self.__clause
    
    def is_empty(self) -> bool:
        """Returns: boolean representing if clause attibute length is 0"""
        return not len(self.__clause)
    
    def __len__(self) -> int:
        """Returns: int number of items in clause attribute"""
        return len(self.__clause)
    
    def __iter__(self) -> Iterator[Literal]:
        """Returns: an iterator for the clause list attribute"""
        return iter(self.__clause)
    
    def __getitem__(self, index: int) -> Literal:
        """Returns: the Literal in the clause list attribute at index"""
        return self.__clause[index]
    
    def __copy__(self) -> 'Clause':
        """Returns: a Clause shallow copy"""
        cl_cp = []
        for lit in self.__clause:
            lit_cp = copy.copy(lit)
            cl_cp.append(lit_cp)
        return Clause(cl_cp)
    
    def __eq__(self, other: 'Clause') -> bool:
        "Returns: a boolean representing if a List or another Clause contains the same "
        same = False
        if not isinstance(other, (Clause, list)):
            raise TypeError("Equality not defined between these two objects.")
        elif isinstance(other, Clause):
            same = True if self.__clause == other.__clause else same
        else:
            same = True if self.__clause == other else same
        return same
    
    def __contains__(self, item) -> bool:
        """Returns: a boolean representing if item is in the clause attribute"""
        if not isinstance(item, Literal):
            raise TypeError("A Clause cannot contain any non-Literal objects")
        return item in self.__clause