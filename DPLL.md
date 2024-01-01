# Davis-Putnam-Logemann-Loveland (DPLL) Algorithm 

## Purpose
The purpose of a dpll algorithm is as a tool used to discover whether or not a logical proposition is satisfiable. 

## Conjunctive Normal Form
The proposition used in the DPLL needs to be in conjunctive normal form (CNF) in order for the algorithm to work. CNF propositions consist of a list of clauses. Each clause consists of one or more literals. A literal consists of a variable that identifies it; and an internal state, being one of either true, false, or NULL. The external status of a literal may diverge from its internal status by use of negation on the literal. A clause containing only one literal is a unit clause, and is represented in a proposition by the literal itself, outside of any clause. Clauses in the proposition are represented as a list of literals; and a status, being one of either true, false, or NULL. The external status of a clause is determined by the combined extrenal values of its constituent literals. The only logical operators allowed in the propition are **AND**s and **OR**s. **AND**s are implicit within the proposition between each of the clauses, including pure clauses. **OR**s are implicit within the clauses in between each of the literals. Clauses cannot be nested.

## Method
How the DPLL algorithm works to determine the satisfiability of a proposition is through the
use of two logical hueristics, and guess and check. The hueristics depend on basic properties of propositions, clauses, and literals:
1. If the external value of a unit clause is true it may be removed from the proposition
because it can no longer cause the proposition to be unsatisfiable. 
2. If the external value of any single literal contained within a Clause is true, the status of the clause is therefore true and the clause may be removed from the proposition because it can no longer cause the proposition to be unsatisfiable.
    - A clause is also true by tautology if it contains two literals with the same variable, but one is negated and the other is not.
3. All literals with the same variable have the same underlying boolean value, but may have different external values depending on any negations. 
4. If the external value of a Literal contained within a Clause is false, the Literal may be removed from the Clause because it can no longer contribute to the clause being true.
    - Removals from inside a clause are allowed because either the clause has a value of false, and each of its literals have external values of false, meaning the last one remaining after removing the rest will be false, rendering the proposition unsatisfiable; or the status of the clause is true, and at least one literal has an external value of true, and it will be found faster by culling the clause of false valued literals.
5. An empty proposition is by satisfiable by definition.
6. If any one clause, including unit clauses. within the propsition has a external status of false, the entire proposition is unsatisfiable. Every clause must have an external value of true for the proposition to be satisfiable. 

The proposition is solved by recursion using the unit clause heuristic, 
the pure clause heuristic, and guess and check. The goal is to remove all clauses from the proposition using the heuristics and targeted guessing the prove each one is true. 

### Unit Clause Hueristic
All unit clauses in a proposition must have an external status of true for the proposition 
to be satisfiable. The unit clause heuristic is used to set all unit clauses so their external 
values are true. If a literal is not negated, its variable is given the value of true; if it is negated, it is given the value of false. The unit clauses are then removed from the proposition, and the rest of the clauses are seached for any Literals with the same variable. If the found literal has the same negation as the unit clause, the clause containing it is removed as it has been made true by the valuation of this single true literal it contains; if it has the opposite negation, it is removed from the clause because its external value is false and therefore cannot count towards the clause being true. If two unit clauses contain the same variable but opposite signs, a truth value cannot be given to the variable that causes the external value of both literals to be true, this causes a contradiction within the proposition and it is deemed unsatisfiable as one or the other unit clause must be false. 

### Pure Clause Hueristic
The pure clause heuristic is used to find literals with a given variable that have all
either been negated or are all not negated throughout the entire proposition, the same within every clause. The value of the variable is set such that the external value for every literal with that variable has an external value of true, allowing each clause containing one of them to be removed from the proposition.

### Guess and Check
If neither of the logical hueristics may be used (e.g. in the case of no unit or pure
clauses remaining in the proposition), a variable may be chosen to guess a value. The chosen variable is given a value, true or false, and the clause and proposition are simplified by searching for literals with that same variable and making the appropriate removals. After this the hueristics are used recursively again until the propostion is deemed satisfiable or not. If it is satisfiable with the guess, the guess is kept, and the result is returned. If it is not satisfiable, the guess is switched, and the result of this new valuation is returned no matter what.   

## Solving for Variables
The DPLL algorithm works by assigning truth values to the variables through the use of the
hueristics and guess and check. These assignments are kept track of in this solver through the use of an object attribute; as the heuristics and guesses take place, the assignments are placed as values to their corresponding variable keys. The proper value assignments for each of the variables may be returned if the proposition is satisfiable, after the solver has deemed it so.

#### Author
Luke Marshall
### Contact 
lukemarshall2222@gmail.com