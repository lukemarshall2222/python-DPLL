"""
Luke Marshall
DPLL solver

ANDs are implicit in the dpll array between each of the clauses, ORs are implicit in the clause arrays
"""

class DPLL(object):

    def __init__(self) -> None:
        self.clauses = []

    def ADD(self, clause):
        if isinstance(clause, set): # negating a clause produces separte negated literals that must be added individually
            while len(clause != 0):
                self.clauses.append(clause.pop())
        else: 
            self.clauses.append(clause)

class Clause(object):

    def __init__(self) -> None:
        self = []

    def NOT(self, clause):
        if isinstance(clause, Literal):
            return clause.set_sign_neg()
        elif isinstance(clause, Clause):
            negated = set()
            for literal in clause:
                literal.set_sign_neg()
                negated.add(literal)
            return negated

    def AND(self, *args):
        for arg in args:
            if isinstance(arg, Literal):

        
    
    def OR(self, *args):
        clause = []
        for arg in args:
            clause.append(arg)
        return clause

        


class Literal(object):

    def __init__(self, literal) -> None:
        self.variable = literal
        self.sign = "+"

    def __str__(self) -> str:
        return self.sign + f"{self.variable}"
    
    def set_sign_neg(self):
        self.sign = '-'
    
    def get_sign(self):
        return 'positive' if self.sign == '+' else 'negative'
    
    def is_neg(self):
        return self.sign == '-'
    
    def is_pos(self):
        return self.sign == '+'
    
    def clauses(*args):
        """Returns a list of clauses with the same names as those given to the function"""
        clauses = []
        for arg in args:
            arg = Clause()
            clauses.append(arg)
        return clauses

    def literals(*args):
        literals = []
        for arg in args:
            arg = Literal()
            literals.append(arg)
        return literals
