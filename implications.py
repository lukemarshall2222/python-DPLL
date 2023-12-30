from Clause import Clause
from Literal import Literal
from dpll import DPLL

def implies(clause1: Clause, clause2: Clause, dpll=None) -> list[Clause]:
    """Translates an implication statement into a number of Clauses in conjunctive 
    normal form
    
    Returns: a list of Clauses that can be used to replace the implication in a 
    conjunctive normal form proposition"""
    
    new_clauses = []
    if isinstance(clause1, Clause) and isinstance(clause2, (Literal, Clause)):
        cl1_neg = clause1.NOT()
        for lit in cl1_neg:
            new_clauses.append(Clause(lit, clause2))
    elif isinstance(clause1, Literal) and isinstance(clause2, (Literal, Clause)):
        cl1_neg = clause1.NOT()
        new_clauses.append(Clause(cl1_neg, clause2))
    else:
        raise TypeError("Implications can only be between Literals and/or Clauses")
    
    if dpll is not None:
        if not isinstance(dpll, DPLL):
            raise TypeError("Biconditionals can only be used with DPLL objects")
        
        for clause in new_clauses:
            dpll.ADD(clause)

    return new_clauses

def bicond(clause1: Clause, clause2: Clause, dpll=None) -> list[Clause]:
    """Translates a biconditional statement into two implications, calls implies()
    to translate implications into conjunctive normal form and add them to a 
    DPLL
    
    Returns: a list of Clauses that can be used to replace the biconditional in a 
    conjunctive normal form proposition"""

    res_clauses1 = implies(clause1, clause2)
    res_clauses2 = implies(clause1, clause2)

    if dpll is not None:
        if not isinstance(dpll, DPLL):
            raise TypeError("Biconditionals can only be used with DPLL objects")
        
    return res_clauses1 + res_clauses2 
