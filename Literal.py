import copy

class Literal(object):
    """Literal object in a conjunctive normal form proposition
    
    Instance Attributes:
        variable: a name representing the literal
        sign: represents if the literal is negated (- for negated, + for not negated)
        status: boolean value representing the internal state of the literal
        calculated_val: boolean value representing the outward state of the literal"""
    
    def __init__(self, variable: str):
        """args:
                variable: a name representing the literal"""
        if not isinstance(variable, str):
            raise TypeError("Literal object only excepts a string as an argument.")
        self.__variable = variable
        self.__sign = "+"
        self.__status = None
        self.__calculated_val = None # calculated based on sign and status

    def __str__(self) -> str:
        """returns:
                string representation of the sign and name of the literal"""
        return self.__sign + self.__variable
    
    def NOT(self):
        """Negates the literal, flips the sign, changes the calculated value if the
        literal has a status.
        given a literal +a:  
        ~(~a) == a => NOT(NOT(a)) == +a
        ~(a) == ~a => NOT(a) == -a
        """
        lit_cp = copy.copy(self)
        lit_cp.flip_sign()
        if lit_cp.get_status is not None:
            lit_cp.set_calculated_val()
        return lit_cp
    
    def get_variable(self) -> str:
        """Returns: string representation of the literal name"""
        return self.__variable
    
    def flip_sign(self):
        """Makes the sign of the Literal the opposite to what it is set to before being called"""
        self.__sign = '-' if self.__sign == '+' else '+'
    
    def get_sign(self) -> str:
        """Returns: string representation of the literal sign"""
        return 'pos' if self.__sign == '+' else 'neg'
    
    def set_status(self, val=True):
        """Sets the status of the literal to val, sets the calculated value
        
        args:
            val: boolean to set the literal status to; default is True"""
        if not isinstance(val, bool):
            raise TypeError("set_status only takes bool type")
        self.__status = val
        self.set_calculated_val()

    def get_status(self) -> bool:
        """Returns: the boolean value of the literal instance attribute status"""
        return self.__status
    
    def get_calculated_val(self) -> bool:
        """Returns: the boolean value of the literal instance attribute 
        calculated_val"""
        return self.__calculated_val
    
    def set_calculated_val(self):
        """sets the calculated value of the literal based on the sign and 
        status instance attributes"""
        if self.__status is None:
            pass
        elif self.__status == True:
            self.__calculated_val = self.__sign == '+'
        elif self.__status == False:
            self.__calculated_val = self.__sign == '-'

    def __eq__(self, other: 'Literal',) -> bool:
        """Returns: a boolean representing if the variables of two literals are
        the same"""
        return self.get_variable() == other.get_variable()

    def __hash__(self) -> int:
        """Returns: hash value of the Literal based on the variable attribute"""
        return hash(self.__variable)
    
    def __copy__(self) -> 'Literal':
        """performs a shallow copy of the Literal and its attributes
        Returns: a copy of the Literal"""
        cp = Literal(self.__variable)
        if self.__sign == '-':
            cp.flip_sign()
        if self.__status is not None:
            cp.set_status(self.__status)
            cp.set_calculated_val()
        return cp
    
    def __bool__(self):
        """Returns boolean representation of the status"""
        return True if self.__status else False