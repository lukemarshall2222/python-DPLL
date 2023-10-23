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
                x = clause.pop()
                if not isinstance(x, Clause) and not isinstance(x, Literal):
                    print("DPLL proposition can only be made up of Literal and Clause objects.")
                    raise TypeError
                self.clauses.append(x)
        elif isinstance(clause, Literal) or isinstance(clause, Clause):

            self.proposition.append(clause) # a single clause must be added to a proposition directly
        else:
            print("DPLL proposition can only be made up of Literal and Clause objects.")
            raise TypeError

    def sat(self):
        """Returns if the proposition is solvable or not"""
        # check if all the clauses in the proposition are true, if they are, the proposition is satis
        sat = True
        for clause in self.proposition:
            if isinstance(clause, Literal):
                sat = False if clause.get_calculated_val() == False else sat
            elif isinstance(clause, Clause):
                sat = False if clause.get_status() == False else sat
        if sat:
            return True
        
        # set the unit clauses to true
        self.unit_clause_heuristic()

        # check to make sure all the unit clauses with the same variable have the same underlying boolean value
        uclauses = {}
        for clause in self.proposition:
            if isinstance(clause, Literal):
                var = clause.get_variable()
                if var in uclauses:
                    if clause.get_status() != uclauses[var]:
                        return 'unsat'
                    else:
                        continue
                else:
                    uclauses[var] = clause.get_status()
                    continue



        
    def unsat(self):
        # TODO check if any of the calculated values of a literal contradict
        pass

    def unit_clause_heuristic(self)
        # check the unit if any of the unit clauses are the only time that the literal shows up in the proposition
        # to see if unit clause heuristic may be implemented
        unit_clauses = set()
        for clause in self.proposition:
            if isinstance(clause, Literal):
                unit_clauses.add(clause.get_variable())
        for clause in self.proposition:
            if isinstance(clause, Clause):
                for lit in clause:
                    var = lit.get_variable()
                    if var in unit_clauses:
                        unit_clauses.remove(var)
        if len(unit_clauses) > 0:
            for lit in unit_clauses:
                if lit.is_pos():
                    lit.set_status(True)
                else:
                    lit.set_status(False)
                assert lit.get_calculated_val() == True

class Clause(object):

    def __init__(self, *args) -> None:
        self.clause = []
        self.__status = None
        for arg in args:
            if isinstance(arg, Literal):
                self.clause.append(arg)
            elif isinstance(arg, Clause):
                for lit in arg:
                    self.clause.append(lit)
            else:
                print("Clause object only accepts Literal or Clause objects as input.")
                raise TypeError

    def set_status(self):
        val = False
        for literal in self.clause:
            if literal.get_calculated_val():
                val = True
        self.__status = val

    def get_status(self):
        self.set_status()
        return self.__status

    def ADD(self, item):
        if isinstance(item, Literal):
            self.clause.append(item)
        elif isinstance(item, Clause):
            if item.is_empty():
                print("An empty Clause object cannot be added to a Clause object")
                raise AttributeError
            for lit in item:
                self.clause.append(lit)
        else:
            print("Clause object only accepts Literal or Clause objects as input.")
            raise TypeError
        self.set_status()

    def NOT(self):
        """Move negations inside e.g. :
            a) ~(~a) = a
            c) ~(a v b) = ~a ∧ ~b"""
        negated = set()
        for instance in self.clause:
            negated.add(instance.NOT())
        self.set_status()
        return negated
    
    def is_empty(self):
        return len(self.clause) == 0

        
class Literal(object):

    def __init__(self, literal) -> None:
        self.__variable = str(literal)
        self.sign = "+"
        self.__status = None
        self.__calculated_val = None

    def __str__(self) -> str:
        return self.sign + f"{self.variable}"
    
    def NOT(self):
        # ~(~a) == a
        # ~(a) == ~a
        self.sign = '-' if self.sign == '+' else ''

    def get_variable(self):
        return self.__variable
    
    def get_sign(self):
        print('This literal has a sign that is ' + 'positive' if self.sign == '+' else 'negative')
    
    def is_neg(self):
        return self.sign == '-'
    
    def is_pos(self):
        return self.sign == '+'
    
    def set_status(self, val: bool):
        try:
            if not isinstance(val, bool):
                raise TypeError
        except TypeError:
            print('set_status only take a boolean value as an argument.')
            raise TypeError
        self.__status = val

    def get_status(self):
        return self.__status
    
    def get_calculated_val(self):
        return self.__calculated_val
    
    def set_calculated_val(self)
        if self.__status == True:
            self.__calculated_val = self.sign == '+'
        elif self.__status == False:
            self.__calculated_val = self.sign == '-'
        else: 
            self.__calculated_val = None

    def __eq__(self, literal1: 'Literal', literal2: 'Literal') -> bool:
        return literal1.variable == literal2.variable
