"""
Luke Marshall
DPLL solver

ANDs are implicit in the dpll array between each of the clauses, ORs are implicit in the clause arrays
"""

class DPLL(object):

    def __init__(self) -> None:
        self.proposition = []

    def ADD(self, clause):
        if isinstance(clause, set): # negating a clause produces separted negated literals that must be added individually
            while len(clause != 0):
                self.clauses.append(clause.pop())
        else: 
            self.proposition.append(clause)

    def sat(self):
        """Returns if the proposition is solvable or not"""
        pass

class Clause(object):

    def __init__(self, *args) -> None:
        self.clause = [] 
        for arg in args:
            self.clause.append(arg)


    def NOT(self):
        """Move negations inside e.g. :
            a) ~(~a) = a
            c) ~(a v b) = ~a ∧ ~b"""
        negated = set()
        for instance in self.clause:
            negated.add(instance.NOT())
        return negated

        
class Literal(object):

    def __init__(self, literal) -> None:
        self.variable = str(literal)
        self.sign = "+"

    def __str__(self) -> str:
        return self.sign + f"{self.variable}"
    
    def NOT(self):
        # ~(~a) == a
        # ~(a) == ~a
        self.sign = '-' if self.sign == '+' else ''
    
    def get_sign(self):
        print('This literal has a sign that is ' + 'positive' if self.sign == '+' else 'negative')
    
    def is_neg(self):
        return self.sign == '-'
    
    def is_pos(self):
        return self.sign == '+'
