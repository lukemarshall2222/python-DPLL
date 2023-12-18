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
        self.__clause = []
        #self.__status = None # based on the statuses of the Literals it contains
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
        # contradiction check:
        self.__contradiction_check()
        # remove duplicates
        self.__filter_duplicates()

    def __contradiction_check(self):
        """Checks clause for duplicates
        Raises:
            AttributeError if contradiction is found"""
        length = len(self.__clause)
        for i in range(length):
            lit_sign = self.__clause[i].get_sign()
            for j in range(length):
                if self.__clause[i] == self.__clause[j] and i != j:
                    if self.__clause[j].get_sign() != lit_sign:
                        raise AttributeError(f"""Contradition: The variable 
                                             {self.clause[i].get_variable()} is 
                                             contained within the clause more than 
                                             once with opposite signs.""")
    
    def __filter_duplicates(self):
        """Removes any duplicates from clause attribute"""
        seen = set()
        self.__clause = [obj for obj in self.__clause if 
                         not (obj in seen or seen.add(obj))]

    def __str__(self) -> str:
        """Returns: string representation of the Literals in clause attribute"""
        return f"{[str(lit) for lit in self.__clause]}"
    
    def __iter__(self):
        """Returns: a List iterator for clause attribute"""
        return iter(self.__clause)

    def ADD(self, item: Union['Clause', Literal]) -> 'Clause':
        """Adds item to the clause attribute if it does not cause a contradiction 
        and is not already in clause
        
        Raises: 
            AttributeError if contradiction is found
            TypeError if wrong type given as item"""
        new_clause = copy.copy(self)
        if isinstance(item, Literal):
            matched = False
            for lit in new_clause:
                if lit == item:
                    if lit.get_sign() != item.get_sign():
                        raise AttributeError(("""The Clause contains a Literal with 
                                this variable of opposite sign: Contradiction"""))
                    else:
                        matched = True
            if not matched:
                self.__clause.append(item)
        elif isinstance(item, Clause):
            if item.is_empty():
                raise AttributeError("""An empty Clause object cannot be 
                                     added to a Clause object""")
            for i in item:
                matched = False
                for lit in new_clause:
                    if lit == i:
                        if lit.get_sign() != i.get_sign():
                            raise AttributeError("""Contradiction: The 
                                                 Clause contains a Literal with this 
                                                 variable of opposite sign.""")
                        else:
                            matched = True
                if not matched:
                    self.__clause.append(i)
        else:
            raise TypeError("""Clause object only accepts Literal or non-negated 
                            Clause objects as input.""")
        return new_clause

    def remove(self, item: Literal) -> 'Clause':
        """removes item from clause attribute
        Returns: new clause same as original but with item removed"""
        if not isinstance(item, Literal):
            raise TypeError("Only Literal object types may be removed from a Clause")
        reduced_clause = copy.copy(self)
        reduced_clause._Clause__clause.remove(item) 
        return reduced_clause

    def NOT(self) -> set:
        """Negates the clause and returns the negation as a set
        Does not change actual clause attribute

        Moves negations inside clause e.g. :
            ~(~a) = a
            ~(a v b) = ~a ∧ ~b"""
        negated = set(copy.copy(self))
        for lit in negated:
            lit.NOT()
        return negated
    
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
        cl_cp = []
        for lit in self.__clause:
            lit_cp = copy.copy(lit)
            cl_cp.append(lit_cp)
        return Clause(cl_cp)