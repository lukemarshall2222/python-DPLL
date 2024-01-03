"""Test suite for dpll.py"""

import pytest
from dpll import DPLL
from Literal import Literal
from Clause import Clause


def test_DPLL_instance():
    dpll = DPLL()
    assert isinstance(dpll, DPLL)

def test_DPLL_proposition_init():
    a = Literal('a')
    b = Literal('b')
    c = Literal('c')
    d = Literal('d')
    cl = Clause(a, b, c, d)
    neg_cl = cl.NOT()
    dpll = DPLL(a, b, c, d, cl, neg_cl)
    arr = [a, b, c, d]
    for lit in arr:
        assert lit in dpll
        assert lit.NOT() in dpll
    assert cl in dpll

def test_DPLL_variables_init():
    a = Literal('a')
    b = Literal('b')
    c = Literal('c')
    d = Literal('d')
    cl = Clause(a, b, c, d)
    neg_cl = cl.NOT()
    dpll = DPLL(a, b, c, d, cl, neg_cl)
    arr = [a, b, c, d]
    vars = dpll.get_variables()
    assert isinstance(vars, dict)
    assert len(vars) == 4
    for lit in arr:
        assert lit.get_variable() in vars

def test_dpll_proposition_add():
    a = Literal('a')
    b = Literal('b')
    c = Literal('c')
    d = Literal('d')
    cl = Clause(a, b, c, d)
    neg_cl = cl.NOT()
    dpll = DPLL()
    dpll.ADD(a)
    dpll.ADD(b)
    dpll.ADD(c)
    dpll.ADD(d)
    arr = [a, b, c, d]
    for lit in arr:
        print(lit.NOT())
    for lit in arr:
        assert lit in dpll
    dpll.ADD(neg_cl)
    for lit in arr:
        assert lit.NOT() in dpll
    dpll.ADD(cl)
    assert cl in dpll

def test_dpll_variables_add():
    a = Literal('a')
    b = Literal('b')
    c = Literal('c')
    d = Literal('d')
    e = Literal('e')
    x = Literal('x')
    y = Literal('y')
    z = Literal('literal')
    arr = [a, b, c, d, e, x, y, z]
    dpll = DPLL()
    for lit in arr:
        dpll.ADD(lit)
    vars = dpll.get_variables()
    assert isinstance(vars, dict)
    for lit in arr:
        assert lit.get_variable() in vars

def test_dpll_get_proposition():
    a = Literal('a')
    b = Literal('b')
    c = Literal('c')
    d = Literal('d')
    cl = Clause(a, b, c, d)
    neg_cl = cl.NOT()
    dpll = DPLL(a, b, c, d, cl)
    arr = [a, b, c, d, cl]
    prop = dpll.get_proposition()
    assert isinstance(prop, list)
    assert arr == prop
    dpll.ADD(neg_cl)
    for i in range(0, 4):
        arr.append(arr[i].NOT())
    prop = dpll.get_proposition()
    assert arr[:5] == prop[:5]
    for i in range(6, len(arr)):
        assert arr[i] in prop[5:]

def test_dpll_disregard():
    a = Literal('a')
    b = Literal('b')
    c = Literal('c')
    d = Literal('d')
    cl = Clause(a, b, c, d)
    neg_cl = cl.NOT()
    dpll = DPLL(a, b, c, d, cl, neg_cl)
    arr = [c, cl, b.NOT(), d, c.NOT(), a, d.NOT(), a.NOT(), b]
    length = len(dpll)
    for item in arr:
        assert len(dpll) == length # also tests len method
        assert item in dpll
        dpll._DPLL__disregard(item)
        assert item not in dpll
        length -= 1
    vars = dpll.get_variables()
    assert len(vars) == 4

def test_dpll_is_empty():
    a = Literal('a')
    dpll = DPLL()
    assert dpll.is_empty()
    dpll.ADD(a)
    assert not dpll.is_empty()
    dpll2 = DPLL(a)
    assert not dpll2.is_empty()

def test_dpll_solve_empty():
    dpll = DPLL()
    sat = dpll.solve()
    assert sat == 'sat'

def test_dpll_solve_most_basic():
    a = Literal('a')
    dpll = DPLL(a)
    sat = dpll.solve()
    assert sat == 'sat'

def test_dpll_solve_basic_contradiction():
    a = Literal('a')
    a_neg = a.NOT()
    dpll = DPLL(a, a_neg)
    sat = dpll.solve()
    assert sat == 'unsat'

def test_dpll_solve_middling_contradiction():
    a = Literal('a')
    a_neg = a.NOT()
    cl = Clause(a_neg)
    dpll = DPLL(a, cl)
    sat = dpll.solve()
    assert sat == 'unsat'

def test_basic_unit_clause_solve():
    a = Literal('a')
    b = Literal('b')
    c = Literal('c')
    c_neg = c.NOT()
    d = Literal('d')
    e = Literal('e')
    e_neg = e.NOT()
    dpll = DPLL(a, b, c_neg, d, e_neg)
    sat = dpll.solve()
    assert sat == 'sat'

def test_basic_pure_clause_solve():
    a = Literal('a')
    a2 = Literal('a')
    c = Literal('c')
    c_neg = c.NOT()
    d = Literal('d')
    e = Literal('e')
    cl = Clause(a, c, d)
    cl2 = Clause(a2, c_neg, e)
    dpll = DPLL(cl, cl2)
    sat = dpll.solve()
    assert sat == 'sat'

def test_solve_middling_prop():
    a = Literal('a')
    a_neg = a.NOT()
    b = Literal('b')
    b_neg = b.NOT()
    c = Literal('c')
    c_neg = c.NOT()
    d = Literal('d')
    d_neg = d.NOT()
    e = Literal('e')
    e_neg = e.NOT()
    cl = Clause(a, b_neg, c)
    cl2 = Clause(a_neg, d)
    cl3 = Clause(b, c_neg, e)
    cl4 = Clause(e_neg, d_neg)
    dpll = DPLL(cl, cl2, cl3, cl4)
    sat = dpll.solve()
    assert sat == 'sat'

def test_solve_middling_prop_2():
    a = Literal('a')
    a_neg = a.NOT()
    b = Literal('b')
    b_neg = b.NOT()
    c = Literal('c')
    c_neg = c.NOT()
    d = Literal('d')
    d_neg = d.NOT()
    e = Literal('e')
    e_neg = e.NOT()
    f = Literal('f')
    f_neg = f.NOT()
    cl = Clause(a, b_neg, c)
    cl2 = Clause(a_neg, e)
    cl3 = Clause(b, c_neg, f_neg)
    cl4 = Clause(e, d_neg, f)
    dpll = DPLL(cl, d, cl2, cl3, cl4, e_neg)
    sat = dpll.solve()
    assert sat == 'sat'

def test_solve_middling_prop_3():
    a = Literal('a')
    a_neg = a.NOT()
    b = Literal('b')
    b_neg = b.NOT()
    c = Literal('c')
    c_neg = c.NOT()
    d = Literal('d')
    d_neg = d.NOT()
    e = Literal('e')
    e_neg = e.NOT()
    cl = Clause(a, b, c_neg)
    cl2 = Clause(a, b_neg)
    cl3 = Clause(d_neg, e)
    cl4 = Clause(d, e_neg)
    dpll = DPLL(cl, cl2, c, cl3, cl4, a_neg, b)
    sat = dpll.solve()
    assert sat == 'unsat'

def test_solve_hard_prop():
    a = Literal('a')
    b = Literal('b')
    b_neg = b.NOT()
    c = Literal('c')
    c_neg = c.NOT()
    d = Literal('d')
    e = Literal('e')
    e_neg = e.NOT()
    f = Literal('f')
    g  = Literal('g')
    g_neg = g.NOT()
    cl = Clause(a, b_neg, c)
    cl2 = Clause(c_neg, d, e)
    cl3 = Clause(f, a)
    cl3_neg = cl3.NOT()
    cl4 = Clause(b, e_neg)
    cl5 = Clause(f, g_neg, a)
    cl6 = Clause(c, g)
    cl7 = Clause(d, b_neg)
    dpll = DPLL(cl, cl2, cl3_neg, cl4, cl5, cl6, cl7)
    sat = dpll.solve()
    assert sat == 'sat'

def test_solve_hard_prop_2():
    a = Literal('a')
    a_neg = a.NOT()
    b = Literal('b')
    b_neg = b.NOT()
    c = Literal('c')
    c_neg = c.NOT()
    d = Literal('d')
    d_neg = d.NOT()
    e = Literal('e')
    e_neg = e.NOT()
    f = Literal('f')
    f_neg = f.NOT()
    g = Literal('g')
    g_neg = g.NOT()
    h = Literal('h')
    h_neg = h.NOT()
    cl = Clause(a, b_neg, c, d_neg)
    cl2 = Clause(a_neg, e, f, g_neg)
    cl3 = Clause(b, c_neg, d, h_neg)
    cl4 = Clause(c, f_neg, b, e)
    cl5 = Clause(e_neg, g, h, a_neg)
    cl6 = Clause(d, h_neg, g, a)
    cl7 = Clause(c_neg, f, e_neg, h)
    dpll = DPLL(cl, cl2, cl3, cl4, cl5, cl6, cl7)
    sat = dpll.solve()
    print(dpll.get_variables())
    assert sat == 'sat'

def test_solve_hard_prop_3():
    a = Literal('a')
    a_neg = a.NOT()
    b = Literal('b')
    b_neg = b.NOT()
    c = Literal('c')
    c_neg = c.NOT()
    d = Literal('d')
    d_neg = d.NOT()
    e = Literal('e')
    e_neg = e.NOT()
    f = Literal('f')
    f_neg = f.NOT()
    g = Literal('g')
    g_neg = g.NOT()
    h = Literal('h')
    h_neg = h.NOT()
    cl = Clause(a, b_neg, c, d_neg)
    cl2 = Clause(a_neg, e, f, g_neg)
    cl3 = Clause(b, c_neg, d, h_neg)
    cl4 = Clause(c, f_neg, b, e)
    cl5 = Clause(e_neg, g, h, a_neg)
    cl6 = Clause(d, h_neg, g, a)
    cl7 = Clause(c_neg, f, e_neg, h)
    cl8 = Clause(a_neg, b_neg, c_neg, d)
    cl9 = Clause(a, e_neg, f_neg, g)
    cl10 = Clause(b_neg, c, d_neg, h)
    cl11 = Clause(e, g_neg, h_neg, a)
    cl12 = Clause(c_neg, f, b_neg, e_neg)
    dpll = DPLL(cl, cl2, cl3, cl4, cl5, cl6, cl7, cl8, cl9, cl10, cl11, cl12, a_neg, b, c_neg, d)
    sat = dpll.solve()
    assert sat == 'unsat'

def test_basic_solve_by_tautology():
    a = Literal('a')
    a_neg = a.NOT()
    cl = Clause(a, a_neg)
    dpll = DPLL(cl)
    sat = dpll.solve()
    assert sat == 'sat'

def test_middling_solve_by_tautology():
    a = Literal('a')
    a_neg = a.NOT()
    b = Literal('b')
    b_neg = b.NOT()
    cl = Clause(a, a_neg)
    cl2 = Clause(b, b_neg)
    dpll = DPLL(cl, cl2)
    sat = dpll.solve()
    assert sat == 'sat'

def test_middling_solve_unsat():
    a = Literal('a')
    a_neg = a.NOT()
    b = Literal('b')
    b_neg = b.NOT()
    c = Literal('c')
    c_neg = c.NOT()
    cl = Clause(a, b)
    cl2 = Clause(a_neg, c)
    cl3 = Clause(b_neg, c_neg)
    cl4 = Clause(a_neg, b_neg)
    cl5 = Clause(a, c_neg)
    cl6 = Clause(a_neg, b)
    cl7 = Clause(a, b_neg)
    dpll = DPLL(cl, cl2, cl3, cl4, cl5, cl6, cl7)
    sat = dpll.solve()
    assert sat == 'unsat'

def test_solve_for_variables():
    a = Literal('a')
    a_neg = a.NOT()
    b = Literal('b')
    b_neg = b.NOT()
    c = Literal('c')
    c_neg = c.NOT()
    d = Literal('d')
    d_neg = d.NOT()
    e = Literal('e')
    e_neg = e.NOT()
    f = Literal('f')
    f_neg = f.NOT()
    g = Literal('g')
    g_neg = g.NOT()
    h = Literal('h')
    h_neg = h.NOT()
    cl = Clause(a, b_neg, c, d_neg)
    cl2 = Clause(a_neg, e, f, g_neg)
    cl3 = Clause(b, c_neg, d, h_neg)
    cl4 = Clause(c, f_neg, b, e)
    cl5 = Clause(e_neg, g, h, a_neg)
    cl6 = Clause(d, h_neg, g, a)
    cl7 = Clause(c_neg, f, e_neg, h)
    cl8 = Clause(a_neg, b_neg, c_neg, d)
    cl9 = Clause(a, e_neg, f_neg, g)
    cl10 = Clause(b_neg, c, d_neg, h)
    cl11 = Clause(e, g_neg, h_neg, a)
    cl12 = Clause(c_neg, f, b_neg, e_neg)
    dpll = DPLL(cl, cl2, cl3, cl4, cl5, cl6, cl7, cl8, cl9, cl10, cl11, cl12, a_neg, b, c_neg)
    vars = dpll.solve_for_variables()
    assert isinstance(vars, dict)
    for var in vars:
        assert vars[var] in (True, False, 'either')

def test_solve_for_variables_2():
    a = Literal('a')
    a_neg = a.NOT()
    dpll = DPLL(a, a_neg)
    vars = dpll.solve_for_variables()
    assert vars is None

def solve_example():
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
    cl = Clause(a, b_neg, c)
    cl2 = Clause(a_neg, d)
    cl3 = Clause(b, c_neg, e)
    cl4 = Clause(d_neg, e_neg)
    dpll = DPLL(cl, cl2, cl3, cl4)
    vars = dpll.solve_for_variables()