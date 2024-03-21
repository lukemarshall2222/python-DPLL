from Clause import Clause
from Literal import Literal
from dpll import DPLL
from typing import Union

def implies(clause1: Union[Clause, Literal], clause2: Union[Clause, Literal], dpll=None) -> list[Clause]:
    """Translates an implication statement into a number of Clauses in conjunctive 
    normal form

    args:
        clause1: Clause used as the first item in the implication
        clause2: Clause used as the second item in the implication
        dpll: default value None. A DPLL which the translated implication may be added to
    
    Returns: 
        List of Clauses that can be used to replace the implication in a 
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

def bicond(clause1: Union[Clause, Literal], clause2: Union[Clause, Literal], dpll=None) -> list[Clause]:
    """Translates a biconditional statement into two implications, calls implies()
    to translate implications into conjunctive normal form and add them to a 
    DPLL

    args:
        clause1: Clause used as the first item in the biconditional
        clause2: Clause used as the second item in the biconditional
        dpll: default value None. A DPLL that the translated biconditional may be added to.

    Returns: 
        List of Clauses that can be used to replace the biconditional in a 
    conjunctive normal form proposition"""

    res_clauses1 = implies(clause1, clause2, dpll)
    res_clauses2 = implies(clause2, clause1, dpll)

    if dpll:
        if not isinstance(dpll, DPLL):
            raise TypeError("Biconditionals can only be used with DPLL objects")
        
    return res_clauses1 + res_clauses2 

def AND(*args: Union[Literal, Clause], clause=None, dpll=None) -> list[Clause]:
    """Translates an AND statement into its constituent clauses. If a clause and dpll are given 
    in the keyword arguments, the AND statement will be added to the clause, translated, and 
    added to the dpll. If only a clause is gieven the AND statement will be translated and the 
    resultant clauses returned, ready to add individually to a dpll. If only a dpll is given,
    the elements of args will be added individually to the dpll.
    
    args:
        *args: a list of Literals and/or Clauses used to make up the AND statement
        clause: default value None. A Clause which the AND statement may be added to
        dpll: default value None. A clause which the translated AND stament may be added to
        
    Returns:
        List of Clauses resulting from the translating of the AND statements"""
    new_clauses = []
    for arg in args:
        if not isinstance(arg, (Literal, Clause)):
            raise TypeError("AND only accepts Literals and/or Clauses")
        elif clause:
            new_clauses.append(Clause(arg, clause))
        else:
            new_clauses.append(arg)
    if dpll and isinstance(dpll, DPLL):
        [dpll.ADD(item) for item in new_clauses]
    return new_clauses
            
