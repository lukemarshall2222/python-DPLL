# Davis-Putnam-Logemann-Loveland (DPLL) Solver

## Purpose
The purpose of this project is to implement a DPLL algorithm in a DPLL solver object. The algorithm is used to find if a given proposition is satisfiable or unsatisfiable. See DPLL.md for more details on the DPLL algorithm and propositions.

## Usage
The solver imvolves the usage of three custom objects: Literal, Clause, and DPLL. Each has its own attributes and methods that contribute to the solver being able to process the objects and reach a conclusion.

A Literal object is the most basic foundational tool of the solver. Each contains four attributes, along with methods to manipulate and access those attributes. The attributes consist of two states, a sign, and a variable. The variable is used to represent the Literals which are all of a kind. The sign is used to signify if a Literal has been negated. The two states of a Literal are an internal state labeled as `status`, and an external state labeled as `calculated_val`; both are represented by boolean values or None. The internal state of Literals with the a given variable are the same throughout a proposition, but their extrenal states may differ. The external state of a Literal is calculated using the sign and status attributes. If the sign is positive, the external state of the Literal is the same as the internal state. If the sign is negative, the Literal has been negated and the external state is opposite of the internal state. The variable of a Literal is initialized with the object; it is recommended that the object be assigned to a name that is the same as its variable, e.g.
                    `a = Literal('a')`
                    `b = Literal('b')`
                    `foo = Literal('foo')` etc.
The status of a Literal may be set using the `set_status()` method, with the default argument being True. The sign of a Literal may be flipped using the `NOT()` method which serves the effect of negating the Literal. The external state of the Literal is calculated automatically whenever changes are made to either the internal state or the sign and when the external state is accessed through `calculated_val`. 

