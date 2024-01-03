# Davis-Putnam-Logemann-Loveland (DPLL) Solver

## Purpose
The purpose of this project is to implement a DPLL algorithm in a **DPLL** solver object. The algorithm is used to find if a given proposition is satisfiable or unsatisfiable. See [DPLL.md](https://github.com/lukemarshall2222/python-DPLL/blob/main/DPLL.md) for more details on the DPLL algorithm and propositions.

## Implementation
The solver involves the usage of three custom objects: **Literal**, **Clause**, and **DPLL**. Each has its own attributes and methods that contribute to the solver being able to process the objects and reach a conclusion.

### Literals
A **Literal** object is the most basic foundational tool of the solver. Each contains four attributes, along with methods to manipulate and access those attributes. 

#### Literal Attributes
The attributes consist of two statuses, a sign, and a variable:
- The variable is used to represent the **Literal**s which are all of a kind.
    - The variable of a **Literal** is initialized with the object; it is recommended that the object be assigned to a name that is the same as its variable, e.g.
                `a = Literal('a')`
                `b = Literal('b')`
                `foo = Literal('foo')` etc. 
- The sign is used to signify if a **Literal** has been negated. 
- The two statuses of a **Literal** are:
    - an internal status stored as the `internal_status` attribute 
        - The internal status of all **Literal**s with a given variable are the same throughout a proposition, but their external statuses may differ.
    - an external status stored as the `external_status` attribute
        - The external status of a **Literal** is calculated using the `sign` and `internal_status` attributes.
        - If the sign is positive, the external status of the **Literal** is the same as the internal status. 
    - both statuses are represented by boolean values or `None` 

 #### Important Literal Methods       
- The status of a **Literal** may be set using the `set_internal_status()` method, with the default argument being `True`. 
- The sign of a **Literal** may be flipped using the `NOT()` method which serves the effect of negating the **Literal**. 
    - The `NOT()` method produces a new **Literal**, a copy which has the same variable and internal state, but with opposite sign. 
    - This is to avoid changing a proposition after the **Literal** has been added to it. 
- The external state of the **Literal** is calculated automatically whenever changes are made to either the internal state or the sign and when the external state is accessed through the `get_external_status()` method.

### Clauses
A **Clause** object is a secondary list tool of the solver. Each **Clause** consists of a list of **Literal** objects, and a status. Each **Clause** contains two attributes, along with methods to manipulate and access those attributes. 

#### Clause Attributes
The two attributes are:
- a list of **Literal**s called `clause` 
- a boolean value called `status` 
    - `status` is contributed to by the external statuses of each of the **Literal**s contained within the 'clause' attribute.
    - It is set each time new **Literal**s are introduced, and whenever it is accessed through the `get_status()` method. 

#### Important Clause Methods
- There are two ways to add a **Literal** to the **Clause**: 
    - The first is on initialization of the **Clause** e.g. `cl = Clause(a, b)`.
    - The second is through the use of the `ADD()` method e.g. `cl.ADD(foo)`. 
    - Other **Clause** objects may be added to a **Clause** in the same way that a **Literal** is; each **Literal** within the added **Clause** is simply added individually; the **Clause**s are not nested. 
- The `remove()` method returns a copy of the **Clause** object, with the only difference being the `clause` attribute of the new Clause does not contain the **Literal** given as an argument. - The `NOT()` method returns a set consisting of the **Literal**s within the `**Clause**` attribute, each negated. 
    - A negated **Clause** may not be added to another **Clause**. 
- The immutability of the **Clause** object is to avoid changing a proposition as a side affect. - The **Clause** class also contains many of the basic list methods such as `contains`, 'eq`, and an iterator through the `clause` attribute. 

### DPLL
A **DPLL** object consists of two lists of **Literal** and/or **Clause** objects, and a dict of the variables in every **Literal** in the lists of objects. Each **DPLL** contains three attributes, along with methods to manipulate and access those attributes. 

#### DPLL Attributes
The three attributes are:
- A list of **Literal**s and/or **Clause**s called `proposition`
- A dict of all the variables contained within the `proposition` attribute, called `variables`
- A copy of the original proposition before any dpll algorithm steps take place. 
    - The `original` list is used to replace the proposition after any method involving use of the dpll algorithm is called so that subsequent calls do not differ in result. 

#### Important DPLL Methods
- **Literal**s and **Clause**s may be added to the `proposition` attribute in two ways:
    - The **DPLL** object may be initialized with **Literal**s and/or **Clause**s as arguments e.g. `dpll = DPLL(foo, cl)` which adds them to `proposition`, 
    - or they may be added to the **DPLL** object with the `ADD()` method e.g. `dpll.ADD(a)`
    - Each new **Literal** added, on its own or within a **Clause**, contributes its variable to the `variables` attribute. 
    - Negated **Clauses** can be added to the **DPLL** in the same two ways. 
- **Literal**s and **Clause**s within the `proposition` attribute of a **DPLL** object are somewhat permanent in that they may be removed from the `proposition` attribute through the private `disregard()` method, but the variables they contain will remain in the `varibales` attribute and the clause itself will remain in the `original` attribute. 
- In order to fully remove a **Literal** or a **Clause**, the **DPLL** object must be reinitialized without the objects. 
- The main two methods of a **DPLL** object are the `solve()` and `solve_for_variables()` methods:
    - The `solve()` method uses the DPLL algorithm in order to find the satisfiability of its proposition
        - Returns 'sat' if it is satisfiable, and 'unsat' if it is unsatisfiable. 
        - This method uses the `unit_clause_heuristic()` and 'pure_clause_heuristic()' methods along with a built-in guess and check in order to assign values to the **Literal** variables
        - The `simplify()` method is then used to disregard the proper **Literal**s and **Clause**s according to their external statuses. 
        - See [DPLL.md](https://github.com/lukemarshall2222/python-DPLL/blob/main/DPLL.md) for more in-depth explanation of these processes. 
    - The value assignments are tracked using the `variables` attribute which may be returned with the proper assignments if the result of the `solve()` call is 'sat', using the `solve_for_variables()` method; otherwise the result of this method is `None`. 
- The **DPLL** class also contains many of the basic list methods such as `contains`, `len`, and an iterator through the `clause` attribute. 

## Usage
In order to use the solver you must first translate a proposition into conjunctive normal form, see [DPLL.md](https://github.com/lukemarshall2222/python-DPLL/blob/main/DPLL.md). 
 proposition in conjunctive normal form:  (A ∨ ¬B ∨ C) ∧ (¬A ∨ D) ∧ (B ∨ ¬C ∨ E) ∧ (¬D ∨ ¬E)
 1. Translate the proposition into **Literal**, **Clause**, and **DPLL** objects
    - start with defining all the Literals and their negations:
    ```python
    a = Literal('a')
    b = Literal('b')
    c = Literal('c')
    d = Literal('d')
    e = Literal('e')
    a_neg = a.NOT()
    b_neg = b.NOT()
    c_neg = c.NOT()
    d_neg = d.NOT()
    e_neg = e.NOT()
    ```
    - use the Literals to create the Clauses:
    ```python
    cl = Clause(a, b_neg, c)
    cl2 = Clause(a_neg, d)
    cl3 = Clause(b, c_neg, e)
    cl4 = Clause(d_neg, e_neg)
    ```
    - use the Literals and Clauses to make the proposition inside a DPLL object:
    ```python
    dpll = DPLL(cl, cl2, cl3, cl4)
    ```
2. Use DPLL methods to solve and solve for variables:
    - Solve result only:
    ```python
    dpll.solve()
    'sat'
    ```
        - will return 'unsat' if the proposition is unsatisfiable
    - Solve variables and result:
    ```python
    dpll.solve_for_variables()
    { 'a': False, 'b': False, 'c': True, 'd': False, 'e': True }
    ```
        - will return `None` if the proposition is unsatisfiable




### Author
Luke Marshall
### Contact 
lukemarshall2222@gmail.com


