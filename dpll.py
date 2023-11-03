"""

Luke Marshall
DPLL solver

ANDs are implicit in the dpll array between each of the clauses, ORs are implicit in the clause arrays
"""

class Literal(object):

    def __init__(self, literal) -> None:
        self.__variable = str(literal)
        self.sign = "+"
        self.__status = None
        self.__calculated_val = None

    def __str__(self) -> str:
        return self.sign + f"{self.get_variable()}"
    
    def NOT(self):
        # ~(~a) == a
        # ~(a) == ~a
        self.sign = '-' if self.sign == '+' else ''

    def get_variable(self):
        return self.__variable
    
    def get_sign(self):
        return 'pos' if self.sign == '+' else 'neg'
    
    def is_pos(self):
        return self.__calculated_val
    
    def set_status(self, val=True):
        try:
            if not isinstance(val, bool):
                raise TypeError
        except TypeError:
            print('set_status only takes a boolean value as an argument.')
            raise TypeError
        self.__status = val

    def get_status(self):
        return self.__status
    
    def get_calculated_val(self):
        return self.__calculated_val
    
    def set_calculated_val(self):
        if self.__status == True:
            self.__calculated_val = self.sign == '+'
        elif self.__status == False:
            self.__calculated_val = self.sign == '-'
        else: 
            self.__calculated_val = None

    def __eq__(self, other: 'Literal',) -> bool:
        return self.get_variable() == other.get_variable()


class DPLL(object):

    def __init__(self, *args) -> None:
        self.variables = {}
        self.proposition = [arg for arg in args]
        for clause in self.proposition:
            if not isinstance(clause, Literal) and not isinstance(clause, Clause):
                print("The proposition only takes Literal and Clause objects.")
                raise TypeError
            elif isinstance(clause, Literal):
                if not clause.get_variable() in self.variables:
                    self.variables[clause.get_variable()] = None
            else:
                for lit in clause:
                    if not lit.get_variable() in self.variables:
                        self.variables[lit.get_variable()] = None


    def ADD(self, clause):
        if isinstance(clause, set): # negating a clause produces separted negated literals that must be added individually
            while len(clause != 0):
                x = clause.pop()
                if not isinstance(x, Clause) and not isinstance(x, Literal):
                    print("DPLL proposition can only be made up of Literal and Clause objects.")
                    raise TypeError
                x_var = x.get_variable()
                if not x_var in self.variables:
                    self.variables[x_var] = None
                self.proposition.append(x)
        elif isinstance(clause, Literal):
            if not clause.get_variable() in self.variables:
                self.variables[clause.get_variable()] = None
            self.proposition.append(clause) # add the literal directly to the proposition
        elif isinstance(clause, Clause):
            for lit in clause:
                if not lit.get_variable() in self.variables:
                    self.variables[lit.get_variable()] = None
            self.proposition.append(clause) # add the clause directly to the proposition
        else:
            print("DPLL proposition can only be made up of Literal and Clause objects.")
            raise TypeError
        
    def remove(self, clause):
        if clause in self.proposition:
            self.proposition.remove(clause)
        else:
            return False
        return True
    
    def __iter__(self):
        return iter(self.proposition)
    
    def __getitem__(self, index):
        return self.proposition[index]

    def sat(self):
        """Returns if the proposition is solvable or not"""
        # check if all the clauses in the proposition are true, if they are, the proposition is satis
        sat = True
        unsat = True
        for clause in self.proposition:
            if isinstance(clause, Literal):
                sat = False if clause.get_calculated_val() == False else sat
                unsat = False if clause.get_calculated_val() == True else unsat
            elif isinstance(clause, Clause):
                sat = False if clause.get_status() == False else sat
                unsat = False if clause.get_status() == True else unsat
        if sat:
            return "sat"
        elif unsat:
            return "unsat"
        
        # apply unit clause heristic
        res = self.unit_clause_heuristic()
        if res:
            return sat()
        
        res2 = self.pure_clause_hueristic()
        if res2:
            return sat() 
        
        prop_cp = self.proposition.copy()
        least = len(self.proposition[0])
        guess = self.proposition[0][0].get_variable()
        for clause in self.proposition:
            if len(clause) < least:
                least = len(clause)
                guess = clause[0].get_variable()
        for clause in self.proposition:
            for lit in clause:
                if lit.get_variable() == guess:
                    lit.set_status()
        res3 = sat()
        if res3 == 'sat':
            return res3
        else:
            self.proposition = prop_cp
        for clause in self.proposition:
            for lit in clause:
                if lit.get_variable() == guess:
                    lit.set_status(False)
        return sat()


    def pure_clause_hueristic(self) -> bool:
        # check if a variable shows up only in its positive or negative form in the proposition
        changed = False
        var_signs = {}
        var_uniformity = {}
        for clause in self.proposition:
            assert isinstance(clause, Clause), "non-Clause found during pure clause check"
            for lit in clause:
                assert isinstance(lit, Literal), "non-Literal found within a clause"
                lit_var = lit.get_variable()
                lit_sign = lit.get_sign()
                if lit_var in var_signs:
                    var_uniformity[lit_var] = False if var_signs[lit_var] == lit_sign else var_uniformity[lit_var]
                else:
                    var_signs[lit_var] = lit_sign
                    var_uniformity[lit_var] = True
        for clause in self.proposition:
            for lit in clause:
                assert isinstance(lit, Literal)
                lit_var = lit.get_variable()
                lit_sign = lit.get_sign()
                if var_uniformity[lit_var]:
                    self.variables[lit_var] = True if lit_sign == 'pos' else 'False'
                    self.proposition.remove(clause)
                    break
        return changed
        


    def unit_clause_heuristic(self):
        changed = False
        uclauses = {}
        for clause in self.proposition:
            if isinstance(clause, Literal):
                lit_var = clause.get_variable()
                lit_sign = clause.get_sign()
                if lit_var in uclauses:
                    if lit_sign != uclauses[lit_var]:
                        # two unit clauses with same variable but opposite sign 
                        # unsat by contradiction
                        return 'unsat'
                else:
                    uclauses[lit_var] = lit_sign
                    self.variables[lit_var] = True if lit_sign == 'pos' else False
                self.proposition.remove(clause)
                changed = True
        for clause in self.proposition:
            if isinstance(clause, Clause):
                for lit in clause:
                    assert isinstance(lit, Literal), "This Clause contains an object that is not a Literal."
                    lit_var = lit.get_variable()
                    if lit_var in uclauses:
                        if lit.get_sign() == uclauses[lit_var]:
                            self.proposition.remove(clause)
                            break
                        else:
                            clause.remove(lit)
                            continue
        return "changed" if changed else "unchanged"

class Clause(object):

    def __init__(self, *args) -> None:
        self.__clause = []
        self.__status = None
        for arg in args:
            if isinstance(arg, Literal):
                self.__clause.append(arg)
            elif isinstance(arg, Clause):
                for lit in arg:
                    self.__clause.append(lit)
            else:
                print("Clause object only accepts Literal or Clause objects as input.")
                raise TypeError

    def set_status(self):
        val = False
        for literal in self.__clause:
            if literal.get_calculated_val():
                val = True
        self.__status = val

    def get_status(self):
        self.set_status()
        return self.__status
    
    def ADD(self, item):
        if isinstance(item, Literal):
            self.__clause.append(item)
        elif isinstance(item, Clause):
            if item.is_empty():
                print("An empty Clause object cannot be added to a Clause object")
                raise AttributeError
            for lit in item:
                self.__clause.append(lit)
        else:
            print("Clause object only accepts Literal or Clause objects as input.")
            raise TypeError
        self.set_status()

    def remove(self, literal):
        if literal in self.__clause:
            self.__clause.remove(literal)
        else:
            return False
        return True 

    def NOT(self):
        """Move negations inside e.g. :
            a) ~(~a) = a
            c) ~(a v b) = ~a ∧ ~b"""
        negated = set()
        for instance in self.__clause:
            negated.add(instance.NOT())
        self.set_status()
        return negated
    
    def is_empty(self):
        return len(self.__clause) == 0
    
    def __len__(self):
        return len(self.__clause)
    
    def __iter__(self):
        return iter(self.__clause)
    
    def __getitem__(self, index):
        return self.__clause[index]

        

