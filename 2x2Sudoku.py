from Literal import Literal
from Clause import Clause
from dpll import DPLL


def main():
    dpll = DPLL()

    # Every square has at least one value
    for r in range(1, 3): # row
        for c in range(1, 3): # column
            new_cl = Clause()
            for v in range(1, 3): # value
                variable = f"x_{r}_{c}_{v}"
                new_lit = Literal(variable)
                new_cl.ADD(new_lit)
            dpll.ADD(new_cl)

    # Every square has at most one value          
    for r in range(1, 3): # row
        for c in range(1, 3): # column
            for v_prime in range(1, 3): # compare value, works as ceiling to avoid redundant clauses
                var_two = f"x_{r}_{c}_{v_prime}"
                lit_two = Literal(var_two)
                two_neg = lit_two.NOT()
                for v in range(1, v_prime): # second compare value
                    var_one = f"x_{r}_{c}_{v}"
                    lit_one = Literal(var_one)
                    one_neg = lit_one.NOT()
                    new_cl = Clause(one_neg, two_neg)
                    dpll.ADD(new_cl)
    
    # Every row contains all the values
    for r in range(1, 3): # row
        for v in range(1, 3): # value
            new_cl = Clause()
            for c in range(1,3): # column
                variable = f"x_{r}_{c}_{v}"
                new_lit = Literal(variable)    
                new_cl.ADD(new_lit)
            dpll.ADD(new_cl)
                
    # Every column has all the values
    for c in range(1, 3): # column
        for v in range(1, 3): # value
            new_cl = Clause()
            for r in range(1, 3): # row
                variable = f"x_{r}_{c}_{v}"
                new_lit = Literal(variable)
                new_cl.ADD(new_lit)
            dpll.ADD(new_cl)

    dpll.set_initial_conditions(x_1_1_1=True)
    vars = dpll.solve_for_variables()
    return vars

if __name__ == '__main__':
    print(main())