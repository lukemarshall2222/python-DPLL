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
        self.__status = None
        for arg in args:
            self.clause.append(arg)

    def set_status(self):
        val = False
        for literal in self.clause:
            if literal.get_status():
                val = True
        self.__status = val

    def get_status(self):
        self.set_status()
        return self.__status

    def ADD(self, item: 'Literal'):
        self.clause.append(item)
        self.set_status()


    def NOT(self):
        """Move negations inside e.g. :
            a) ~(~a) = a
            c) ~(a v b) = ~a ∧ ~b"""
        negated = set()
        for instance in self.clause:
            try: 
                if isinstance(instance, Clause):
                    raise Exception
            except Exception:
                print('An attempt was made to negate a nested clause which would lead to the outer clause not being in conjunctive normal form.' 
                      + 'Simplify or rearrange to avoid negating a nested clause')
                raise Exception
            negated.add(instance.NOT())
        self.set_status()
        return negated

        
class Literal(object):

    def __init__(self, literal) -> None:
        self.variable = str(literal)
        self.sign = "+"
        self.__status = None

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
    
    def set_status(self, val: bool):
        self.__status = val

    def get_status(self):
        return self.__status

    def __eq__(self, literal1: 'Literal', literal2: 'Literal') -> bool:
        return literal1.variable == literal2.variable
