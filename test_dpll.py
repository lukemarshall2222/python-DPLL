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
