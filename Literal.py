import copy

class Literal(object):
    """Literal object in a conjunctive normal form proposition
    
    Attributes:
        variable: a name representing the literal
        sign: represents if the literal is negated (- for negated, + for not negated)
        internal_status: boolean value representing the internal state of the literal
        external_status: boolean value representing the external state of the literal"""
    
    def __init__(self, variable: str):
        """args:
                variable: a name representing the literal
            Ex"""
        if not isinstance(variable, str):
            raise TypeError("Literal object only excepts a string as an argument.")
        self.__variable = variable
        self.__sign = "+"
        self.__internal_status = None
        self.__external_status = None # calculated based on sign and status

    def __str__(self) -> str:
        """Returns: string representation of the Literal variable and its sign"""
        return self.__sign + self.__variable
    
    def __repr__(self):
        """Returns: string representation of the Literal variable and its sign"""
        return self.__sign + self.__variable
    
    def NOT(self) -> 'Literal':
        """Negates the literal, flips the sign, changes the external status if the
        literal has a status.
        given a Literal '+a':
        ~(a) == ~a => NOT(a) == -a
        ~(~a) == a => NOT(NOT(a)) == +a
        """
        lit_cp = copy.copy(self)
        lit_cp.__flip_sign()
        if lit_cp.get_internal_status is not None:
            lit_cp.__set_external_status()
        return lit_cp
    
    def get_variable(self) -> str:
        """Returns: string representation of the literal name"""
        return self.__variable
    
    def __flip_sign(self):
        """Makes the sign of the Literal the opposite to what it is set to before being called"""
        self.__sign = '-' if self.__sign == '+' else '+'
    
    def get_sign(self) -> str:
        """Returns: string representation of the literal sign"""
        return 'pos' if self.__sign == '+' else 'neg'
    
    def set_internal_status(self, val=True):
        """Sets the status of the literal to val, sets the external status
        
        args:
            val: boolean to set the literal status to; default is True"""
        if not isinstance(val, bool):
            raise TypeError("set_internal_status only takes bool type")
        self.__internal_status = val
        self.__set_external_status()

    def get_internal_status(self) -> bool:
        """Returns: the boolean value of the literal instance attribute status"""
        return self.__internal_status
    
    def get_external_status(self) -> bool:
        """Returns: the boolean value of the literal instance attribute 
        external_status"""
        return self.__external_status
    
    def __set_external_status(self):
        """sets the external status of the literal based on the sign and 
        status instance attributes"""
        if self.__internal_status is None:
            pass
        elif self.__internal_status == True:
            self.__external_status = self.__sign == '+'
        elif self.__internal_status == False:
            self.__external_status = self.__sign == '-'

    def __eq__(self, other: 'Literal',) -> bool:
        """Returns: a boolean representing if the variables of two literals are
        the same"""
        if not isinstance(other, Literal):
            return False
        same = True
        same = False if self.get_variable() != other.get_variable() else same
        same = False if self.get_sign() != other.get_sign() else same
        same = False if self.get_internal_status() != other.get_internal_status() else same
        return same

    def __hash__(self) -> int:
        """Returns: hash value of the Literal based on the variable attribute"""
        return hash(self.__sign + self.__variable)
    
    def __copy__(self) -> 'Literal':
        """performs a shallow copy of the Literal and its attributes
        Returns: a shallow copy of the Literal"""
        cp = Literal(self.__variable)
        cp.__sign = self.__sign
        cp.__internal_status = self.__internal_status
        cp.__external_status = self.__external_status
        return cp

    def __deepcopy__(self, memo) -> 'Literal':
        """performs a deep copy of the Literal and its attributes
        since the attributes are all immutable, it is the same as a shallow copy
        Returns: a deep copy of the Literal"""
        cp = Literal(self.__variable)
        memo[id(self)] = cp
        cp.__sign = self.__sign
        cp.__internal_status = self.get_internal_status()
        cp.__external_status = self.get_external_status()
        return cp
    
    def __bool__(self):
        """Returns boolean representation of the status"""
        return True if self.__internal_status else False