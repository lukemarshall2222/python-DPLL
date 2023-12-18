# TODO fix implication function
# def implies(clause1: Clause, clause2: Clause, proposition=None) -> Clause:
#     res_clause = Clause()
#     if isinstance(clause1, Clause):
#         for lit in clause1:
#             res_clause.ADD(lit)
#     elif isinstance(clause1, Literal):
#         res_clause.ADD(clause1)
#     else:
#         print("Implication can only be between Literals and Objects")
#         raise TypeError
#     res_clause.NOT()
#     if isinstance(clause2, Clause):
#         for lit in clause2:
#             res_clause.ADD(lit)
#     elif isinstance(clause2, Literal):
#         res_clause.ADD(clause2)
#     else:
#         print("Implication can only be between Literals and Objects")
#         raise TypeError
#     return res_clause

# TODO implement a biconditional function
# def bicond(clause1: Clause, clause2: Clause, proposition=None) -> tuple(Clause):
#     ''''''
#     res_clause1 = implies(clause1, clause2)
#     res_clause2 = implies(clause1, clause2)
#     if proposition is not None:
#         assert isinstance(proposition, DPLL)
#         proposition.ADD(res_clause1)
#         proposition.ADD(res_clause2)
#     return (res_clause1, res_clause2)

# def solve(*args: Literal):
