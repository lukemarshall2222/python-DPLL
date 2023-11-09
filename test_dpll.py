"""Test suite for dpll.py"""

import pytest
from dpll import DPLL, Literal, Clause

def test_instances():
    # test the types of objects
    dpll = DPLL()
    clause = Clause()
    literal = Literal('a')
    assert isinstance(dpll, DPLL)
    assert isinstance(clause, Clause)
    assert isinstance(literal, Literal)

def test_literal_init():
    # testing the Literal constructor
    a = Literal('a')
    assert a.get_variable() == 'a'
    assert a.get_sign() == 'pos'
    assert a.get_status() is None
    assert a.get_calculated_val() is None

def test_literal_NOT():
    a = Literal('a')
    assert a.get_sign() == 'pos'
    a.NOT()
    assert a.get_sign() == 'neg'

def test_literal_status_val():
    a = Literal('a')
    a.set_status()
    assert a.get_sign() == 'pos'
    assert a.get_status() == True
    assert a.get_calculated_val() == True
    a.NOT()
    assert a.get_sign() == 'neg'
    assert a.get_status() == True
    assert a.get_calculated_val() == False
    a.NOT()
    a.set_status(False)
    assert a.get_sign() == 'pos'
    assert a.get_status() == False
    assert a.get_calculated_val() == False
    a.NOT()
    assert a.get_sign() == 'neg'
    assert a.get_status() == False
    assert a.get_calculated_val() == True

def test_clause_init():
    # testing the clause constructor
    a = Literal('a')
    b = Literal('b')
    c = Literal('c')
    cl = Clause(a, b, c)
    arr = ['a', 'b', 'c']
    for i in range(len(cl)): # also checks __len__ and __getitem__ methods
        assert arr[i] == cl[i].get_variable()
    assert cl.get_status() == None # also partially tests get_status and set_status (used in get_status)

def test_clause_status():
    a = Literal('a')
    b = Literal('b')
    c = Literal('c')
    cl = Clause(a, b, c)
    assert cl.get_status() == None
    a.set_status()
    assert cl.get_status()
    a.NOT()
    assert cl.get_status() == None
    b.set_status(False)
    c.set_status(False)
    assert not cl.get_status()
    b.NOT()
    assert cl.get_status()
    d = Literal('d')
    cl.ADD(d) # also tests adding a literal to a clause
    d.set_status()
    assert cl.get_status()
    d.NOT()
    b.NOT()
    assert not cl.get_status()

def test_clause_add():
    a = Literal('a')
    b = Literal('b')
    c = Literal('c')
    d = Literal('d')
    e = Literal('e')
    cl1 = Clause(a, b)
    cl2 = Clause(c, d)
    a.set_status(False)
    b.set_status(False)
    arr = [a, b]
    for i in range(len(cl1)):
        assert cl1[i] == arr[i]
    assert not cl1.get_status()
    arr.append(c)
    arr.append(d)
    cl1.ADD(cl2)
    for i in range(len(cl1)):
        assert cl1[i] == arr[i]
    assert cl1.get_status() == None
    e.set_status()
    arr.append(e)
    cl1.ADD(e)
    for i in range(len(cl1)):
        assert cl1[i] == arr[i]
    assert cl1.get_status()
    e.NOT()
    assert not cl1.get_status()
    cl3 = Clause()
    with pytest.raises(AttributeError):
        cl1.ADD(cl3)
    a2 = Literal('a')
    a2.NOT()
    print(a2.get_sign())
    print(a.get_sign())
    with pytest.raises(AttributeError):
        cl1.ADD(a2)
    with pytest.raises(AttributeError):
        cl1.ADD(Clause(a2))
    cl3 = Clause(Literal('f'), Literal('g')).NOT()
    with pytest.raises(TypeError):
        cl1.ADD(cl3)

