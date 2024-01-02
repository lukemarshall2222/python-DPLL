import copy

class Literal(object):
    """Literal object in a conjunctive normal form proposition
    
    Attributes:
        variable: a name representing the literal
        sign: represents if the literal is negated (- for negated, + for not negated)
        internal_status: boolean value representing the internal state of the literal
        external_status: boolean value representing the external state of the literal"""
    
    def __init__(self, variable: str):
        """ Constructor method for a Literal object.
        args:
                variable: a name representing the literal
        It is recommended to use the same name for the Literal as its variable.

        Examples:
        >>> a = Literal('a')
        >>> lit1 = Literal('lit1')"""

        if not isinstance(variable, str):
            raise TypeError("Literal object only excepts a string as an argument.")
        self.__variable = variable
        self.__sign = "+"
        self.__internal_status = None
        self.__external_status = None # calculated based on sign and status

    def __str__(self) -> str:
        """Returns: string representation of the Literal variable and its sign
        
        Examples:
        >>> a = Literal('a')
        >>> str(a)
        '+a'
        >>> print(a)
        '+a'
        """
        return self.__sign + self.__variable
    
    def __repr__(self):
        """Returns: string representation of the Literal variable and its sign
        Examples:
        >>> a = Literal('a')
        >>> repr(a)
        '+a'
        """
        return self.__sign + self.__variable
    
    def NOT(self) -> 'Literal':
        """Negates the Literal, flips the sign, changes external_status if the
        Literal has an internal_status that is not None.

        given a Literal '+a':
        ~(a) == ~a => NOT(a) == -a
        ~(~a) == a => NOT(NOT(a)) == +a

        Examples:
        >>> a = Literal('a')
        >>> print(a)
        '+a'
        >>> a2 = a.NOT()
        >>> print(a2)
        '-a'
        """
        lit_cp = copy.copy(self)
        lit_cp.__flip_sign()
        if lit_cp.get_internal_status is not None:
            lit_cp.__set_external_status()
        return lit_cp
    
    def get_variable(self) -> str:
        """Returns: string representation of the Literal variable
        
        Examples:
        >>> a = Literal('a')
        >>> a.get_variable()
        'a'

        >>> lit1 = Literal('lit1')
        >>> lit1.get_variable()
        'lit1'
        """
        return self.__variable
    
    def __flip_sign(self):
        """Makes the sign of the Literal the opposite of what it is set to before being called.
        
        e.g.
          if the Literal sign is '+', it will flip to '-'
          if the Literal sign is '-', it will flip to '+'
          """
        self.__sign = '-' if self.__sign == '+' else '+'
    
    def get_sign(self) -> str:
        """Returns: string representation of the Literal sign
        
        Examples:
        >>> a = Literal('a')
        >>> a.get_sign()
        'pos'

        >>> a2 = a.NOT()
        >>> a2.get_sign()
        'neg
        """
        return 'pos' if self.__sign == '+' else 'neg'
    
    def set_internal_status(self, val=True):
        """Sets the status of the Literal to val, sets external_status
        
        args:
            val: boolean to set the Literal status to; default is True
            
        Examples:
        >>> a = Literal('a')
        >>> a.set_internal_status()
        >>> a.__internal_status == True
        True
        
        >>> a.set_internal_status(False)
        >>> a.__internal_status == False
        True
        """
        if not isinstance(val, bool):
            raise TypeError("set_internal_status only accepts bool type.")
        self.__internal_status = val
        self.__set_external_status()

    def get_internal_status(self) -> bool:
        """Returns: the boolean value assigned to the Literal internal_status attribute
        
        Examples:
        >>> a = Literal('a')
        >>> a.set_internal_status()
        >>> a.get_internal_status()
        True
        
        >>> b = Literal('b')
        >>> b.set_internal_status(False)
        >>> b.get_internal_status()
        False
        """
        return self.__internal_status
    
    def __set_external_status(self):
        """Sets external_status of the Literal based on its sign and status attributes
        
        Examples:
        >>> a = Literal('a')
        >>> a.set_internal_status()
        >>> a.get_sign()
        'pos'
        >>> a.__set_external_status()
        >>> a.__external_status == True
        True
        
        >>> a2 = a.NOT()
        >>> a2.___set_external_status()
        >>> a.__external_status == False
        True
        """
        if self.__internal_status is None:
            pass
        elif self.__internal_status == True:
            self.__external_status = self.__sign == '+'
        elif self.__internal_status == False:
            self.__external_status = self.__sign == '-'

    
    def get_external_status(self) -> bool:
        """Returns: the boolean value of the Literal external_status attribute
        
        Examples:
        >>> a = Literal('a')
        >>> a.set_internal_status()
        >>> a.get_sign()
        'pos'
        >>> a.__set_external_status()
        >>> a.get_external_status()
        True
        
        >>> a2 = a.NOT()
        >>> a2.___set_external_status()
        >>> a.get_external_status()
        False
        """
        return self.__external_status
    
    def __eq__(self, other: 'Literal',) -> bool:
        """Returns: a boolean representing if the variables of two Literals are
        the same
        
        Examples:
        >>> a = Literal('a')
        >>> a2 = Literal('a')
        >>> a == a2
        True

        >>> b = Literal('b')
        >>> a == b
        False
        """
        if not isinstance(other, Literal):
            return False
        same = True
        same = False if self.get_variable() != other.get_variable() else same
        same = False if self.get_sign() != other.get_sign() else same
        same = False if self.get_internal_status() != other.get_internal_status() else same
        return same

    def __hash__(self) -> int:
        """Returns: hash value of the Literal based on the variable attribute
        
        Used to place Literals in hashtables such as sets and dicts.
        """
        return hash(self.__sign + self.__variable)
    
    def __copy__(self) -> 'Literal':
        """Performs a shallow copy of the Literal and its attributes.
        Returns: a shallow copy of the Literal
        
        Example:
        >>> a = Literal('a')
        >>> a2 = copy.copy(a)
        >>> a.get_variable() == a2.get_variable()
        True
        >>> a.get_sign() == a2.get_sign()
        True
        >>> a.get_internal_status() == a2.get_internal_status()
        True
        >>> a.get_external_status() == a2.get_external_status()
        True
        """
        cp = Literal(self.__variable)
        cp.__sign = self.__sign
        cp.__internal_status = self.__internal_status
        cp.__external_status = self.__external_status
        return cp

    def __deepcopy__(self, memo) -> 'Literal':
        """performs a deep copy of the Literal and its attributes
        since the attributes are all immutable, it is the same as a shallow copy
        Returns: a deep copy of the Literal
        
        Example:
        >>> a = Literal('a')
        >>> a2 = copy.copy(a)
        >>> a.get_variable() == a2.get_variable()
        True
        >>> a.get_sign() == a2.get_sign()
        True
        >>> a.get_internal_status() == a2.get_internal_status()
        True
        >>> a.get_external_status() == a2.get_external_status()
        True
        """
        cp = Literal(self.__variable)
        memo[id(self)] = cp
        cp.__sign = self.__sign
        cp.__internal_status = self.get_internal_status()
        cp.__external_status = self.get_external_status()
        return cp
    
    def __bool__(self):
        """Returns boolean representation of the Literal internal_status attribute
        
        Example:
        >>> a = Literal('a')
        >>> a.set_internal_status()
        >>> bool(a)
        True
        """
        return True if self.__internal_status else False