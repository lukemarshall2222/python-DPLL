# Davis-Putnam-Logemann-Loveland (DPLL) Algorithm 

## Purpose
The purpose of a dpll algorithm is as a tool used to discover if a proposition is satisfiable or unsatisfiable. 

## Conjunctive Normal Form
The input for a DPLL is a proposition. The proposition used in the DPLL needs to be in conjunctive normal form (CNF) in order for the algorithm to work. CNF propositions consist of a list of clauses. Each clause consists of one or more literals. A literal consists of a variable that identifies it; and an internal status, being one of either true or false if it is known, or NULL if it is unknown. The external status of a literal may diverge from its internal status by use of negation on the literal. A clause containing only one literal is a unit clause, and is represented in a proposition by the literal itself, outside of any clause. Clauses in the proposition are represented as a list of literals and a status. The status may be one of either true or false if it is known, or NULL if it is unknown. The external status of a clause is determined by the combined external statuses of its constituent literals. The only logical operators allowed in the propition are **AND**s and **OR**s. **AND**s are implicit within the proposition between each of the clauses, including unit clauses. **OR**s are implicit within the clauses in between each of the literals. Clauses cannot be nested. There are methods of translating any logical proposition that are not in CNF into propsitions in CNF. [See here for instructions on how to do so.](https://users.aalto.fi/~tjunttil/2020-DP-AUT/notes-sat/cnf2.html)

## Method
The DPLL algorithm works to determine the satisfiability of a proposition in CNF through the
use of two logical hueristics, along with guess and check. The hueristics depend on basic properties of propositions, clauses, and literals:
1. If a proposition is satisfiable, any one of its subpropositions will also be satisfiable.
2. An empty proposition is satisfiable by definition.
3. If the external value of a unit clause is true it may be removed from the proposition
because it can no longer cause the proposition to be unsatisfiable. 
    - Clauses may be removed from a proposition if they are deemed true because the new proposition is a subproposition of the original. If it is satisfiable without the true clause, it would be satisfiable with it as well; and if it is unsatisfiable, it would be unsatisfiable with the true clause as well. 
4. If the external status of any single literal contained within a clause is true, the status of the clause is also true and the clause may be removed from the proposition because it can no longer cause the proposition to be unsatisfiable.
    - A clause is also true by tautology if it contains two literals with the same variable, but one is negated and the other is not.
5. All literals with the same variable have the same underlying boolean value, but may have different external status depending on any negations. 
6. If the external value of a Literal contained within a clause is false, the Literal may be removed because it can no longer contribute to the clause being true.
    - Removals from inside a clause are allowed because either the clause has a value of false, and each of its literals have external values of false, meaning the last one remaining after removing the rest will be false, rendering the proposition unsatisfiable; or the status of the clause is true, and at least one literal has an external status of true, and it will be found easier by culling the clause of false valued literals.

The proposition is solved using a depth-first search by assigning values to variables using the unit clause heuristic, the pure clause heuristic, and guess and check. The goal is to remove all clauses from the proposition using the heuristics and targeted guessing to prove that the proposition is satisfiable. 

### Unit Clause Hueristic
All unit clauses in a proposition must have an external status of true for the proposition 
to be satisfiable. The unit clause heuristic is used to set all unit clauses so their external 
values are true. If a literal is not negated, its variable is given the value of true; if it is negated, it is given the value of false. The unit clauses are then removed from the proposition, and the rest of the clauses are seached for any literals with the same variable as any one of the unit clauses. If a literal is found which has the variable of one of the unit clauses, and it has the same negation as the unit clause, the clause containing the found literal is removed from the proposition as the clause has been made true by the valuation of this single true literal it contains; if it has the opposite negation, the found literal is removed from the clause because its external status is false and therefore cannot count towards the clause being true. If two unit clauses contain the same variable but opposite signs, a truth value cannot be given to the variable that causes the external value of both unit clauses to be true, this causes a contradiction within the proposition and it is deemed unsatisfiable as one or the other unit clause must be false. This should be reapeated until all unit clauses are removed.

### Pure Clause Hueristic
The pure clause heuristic is used to find literals with a given variable that have all
either been negated or are all not negated throughout the entire proposition, the same within every clause. The value of the variable is set such that the external value for every literal with that variable has an external value of true, allowing each clause containing one of them to be removed from the proposition. The UHC should preceed each use of this hueristic.

### Guess and Check
If neither of the logical hueristics may be used (e.g. in the case of no unit or pure
clauses remaining in the proposition), a variable may be chosen to guess a value. The chosen variable is given a value, true or false, and the clause and proposition are simplified by searching for literals with that same variable and making the appropriate removals. After this the hueristics and more guess and check are used recursively again until the propostion is deemed satisfiable or not. If it is satisfiable with the guess, the guess is kept, and the result is returned. If it is not satisfiable, the guess is switched, and the result of this new valuation is returned no matter what.   

## Solving for Variables
The DPLL algorithm works by assigning truth values to the variables through the use of the
hueristics and guess and check. These assignments are kept track of in this solver through the use of an object attribute; as the heuristics and guesses take place, the assignments are placed as values to their corresponding variable keys. The proper value assignments for each of the variables may be returned if the proposition is satisfiable, after the solver has deemed it so.

#### Author
Luke Marshall
### Contact 
lukemarshall2222@gmail.com