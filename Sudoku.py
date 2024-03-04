"""
Luke Marshall

Sudoku solver using DPLL object
"""
from Literal import Literal
from Clause import Clause
from dpll import DPLL

def main():
    
    dpll = DPLL()

    # Every square has at least one value, v . A Literal variable for the Sudoku puzzle
    # represents a square on the board x_row_column_value 
    # ⋀ 1≤row≤9, 1≤column≤9 ('x_1_1_1' v 'x_1_1_2' v ... v 'x_1_1_9' ) ⋀ ...
                                # ... ⋀ ('x_9_9_1' v 'x_9_9_2' v ... v 'x_9_9_9' )
    # a Literal with the external value of True means that there is a value of v in a square 
    # identified by row, column coordinates
    for r in range(1, 10): # row
        for c in range(1, 10): # column
            new_cl = Clause()
            for v in range(1, 10): # value
                variable = f"x_{r}_{c}_{v}"
                new_lit = Literal(variable)
                new_cl.ADD(new_lit)
                print(len(new_cl))
            dpll.ADD(new_cl)

    # Every square has at most one value, v.
    # ⋀ 1≤row≤9, 1<=column<=9, 1≤value<v'≤9 (~'x_1_1_1' v ~'x_1_1_2') ⋀ (~'x_1_1_1' v ~'x_1_1_3') 
                # ⋀ ... ⋀ (~'x_9_9_8' v ~'x_9_9_9')
    # Given a puzzle with a number of squares filled in, this will start the process of assigning
    # truth values to the unknowns e.g. if x_9_9_9 == True then x_9_9_# is False if # != 9, and 
    # none of the squares in any of the groups with the (9, 9) square can have the value of 9 
    for r in range(1, 10): # row
        for c in range(1, 10): # column
            for v_prime in range(1, 10): # compare value, works as ceiling to avoid redundant clauses
                var_two = f"x_{r}_{c}_{v_prime}"
                lit_two = Literal(var_two)
                two_neg = lit_two.NOT()
                for v in range(1, v_prime): # second compare value
                    var_one = f"x_{r}_{c}_{v}"
                    lit_one = Literal(var_one)
                    one_neg = lit_one.NOT()
                    new_cl = Clause(one_neg, two_neg)
                    print(len(new_cl))
                    dpll.ADD(new_cl)

    # Every row contains all the values (1-9)
    # ⋀ 1≤row<=n, 1≤value≤n ('x_1_1_1' v 'x_1_2_1' v ... v 'x_1_9_1' ) ⋀ ...
                                # ... ⋀ ('x_9_1_9' v 'x_9_2_9' v ... v 'x_9_9_9' ) 
    for r in range(1, 10): # row
        for v in range(1, 10): # value
            new_cl = Clause()
            for c in range(1,10): # column
                variable = f"x_{r}_{c}_{v}"
                new_lit = Literal(variable)    
                new_cl.ADD(new_lit)
            dpll.ADD(new_cl)

    # Every column contains all the values (1-9)
    # ⋀ 1≤column<=n, 1≤value≤n ('x_1_1_1' v 'x_2_1_1' v ... v 'x_9_1_1' ) ⋀ ...
                                # ... ⋀ ('x_1_9_9' v 'x_2_9_9' v ... v 'x_9_9_9' )
    for c in range(1, 10): # column
        for v in range(1, 10): # value
            new_cl = Clause()
            for r in range(1, 10): # row
                variable = f"x_{r}_{c}_{v}"
                new_lit = Literal(variable)
                new_cl.ADD(new_lit)
            dpll.ADD(new_cl)

    # Every block contains all the values (1-9)
    # create a list of the block goups of squares by their coordinates:
    row_nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    blocks = []
    for iteration in range(3):
        boxes = [[], [], []]
        for r in range(3):
            for c in range(1, 10):
                if c < 4:
                    boxes[0].append(f"x_{row_nums[r]}_{c}")
                elif c < 7:
                    boxes[1].append(f"x_{row_nums[r]}_{c}")
                else:
                    boxes[2].append(f"x_{row_nums[r]}_{c}")
        for box in boxes:
            blocks.append(box)
        del row_nums[:3]
    # blocks is now a list of the 9 block groups of the puzzle
    # need to define each of these as a set of 9 clauses each, where the value is the same 
    # in each clause
    for block in blocks: # take the coordinates in the block and add a value (1-9) to the end
        for v in range(1, 10): # value
            new_cl = Clause()
            for coordinates in block:
                variable = f"{coordinates}_{v}"
                new_lit = Literal(variable)
                new_cl.ADD(new_lit)
            dpll.ADD(new_cl)

    dpll.set_initial_conditions(x_1_1_2=True, x_1_7_9=True, x_1_9_3=True, 
                                x_2_3_9=True, x_2_4_5=True, x_2_5_3=True, x_2_9_4=True, 
                                x_3_4_7=True, 
                                x_4_6_2=True, x_4_9_8=True,
                                x_5_1_1=True, x_5_4_3=True, x_5_5_8=True, x_5_8_5=True, 
                                x_6_3_3=True, x_6_6_7=True,
                                x_7_3_2=True, x_7_4_9=True, x_7_5_4=True, x_7_9_5=True,
                                x_8_6_8=True,
                                x_9_2_6=True, x_9_8_1=True)
    
    # dpll.set_initial_conditions(x_1_1_4=True, x_1_3_2=True, x_1_7_3=True, x_1_8_8=True, 
    #                             x_2_1_1=True, x_2_3_9=True, x_2_4_6=True, x_2_6_7=True, x_2_7_4=True,
    #                             x_3_3_8=True, x_3_4_3=True, x_3_7_1=True, x_3_9_6=True, 
    #                             x_4_2_9=True, x_4_5_3=True, x_4_9_4=True, 
    #                             x_5_2_2=True, x_5_3_3=True, x_5_4_9=True, x_5_5_6=True, x_5_6_4=True, x_5_7_7=True, x_5_8_1=True, 
    #                             x_6_1_8=True, x_6_5_1=True, x_6_8_6=True, 
    #                             x_7_1_9=True, x_7_3_7=True, x_7_6_6=True, x_7_7_5=True, 
    #                             x_8_3_5=True, x_8_4_8=True, x_8_6_9=True, x_8_7_6=True, x_8_9_2=True, 
    #                             x_9_2_4=True, x_9_3_6=True, x_9_7_8=True, x_9_9_9=True)
    
    vars = dpll.solve_for_variables()
    return vars


if __name__ == '__main__':
   print(main())
