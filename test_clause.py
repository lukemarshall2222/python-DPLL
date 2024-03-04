import pytest
import copy
from Literal import Literal
from Clause import Clause

def test_clause_instance():
    # test the type of a Clause
    clause = Clause()
    assert isinstance(clause, Clause)

def test_clause_init():
    # test the clause constructor
    a = Literal('a')
    b = Literal('b')
    c = Literal('c')
    d = Literal('d')
    a2 = Literal('a')
    cl = Clause(a, b)
    arr = [a, b]
    assert cl == arr
    cl1 = Clause(c, d)
    arr += [c, d]
    cl2 = Clause(a, b, cl1)
    assert cl2 == arr
    a2 = a2.NOT()
    cl2 = Clause(a, b, c, d, a2)
    arr.append(a2)
    assert cl2 == arr
    cl2 = Clause(a, b, b)
    arr2 = [a, b]
    assert cl2 == arr2
    with pytest.raises(TypeError):
        Clause('a')

def test_clause_init_status():
    # test the status after initialization
    a = Literal('a')
    b = Literal('b')
    c = Literal('c')
    d = Literal('d')
    a2 = Literal('a')
    a2 = a2.NOT()
    cl = Clause(a, b, a2)
    assert cl._Clause__tautology_check() == True
    assert cl.get_status() == True
    cl2 = Clause(a, b)
    assert cl2._Clause__tautology_check() == False
    assert cl2.get_status() == None
    c.set_internal_status()
    cl3 = Clause(c, d)
    assert cl3.get_status() == True
    c = c.NOT()
    d.set_internal_status(False)
    cl4 = Clause(c, d)
    assert cl4.get_status() == False

def test_clause_add():
    # test clause ADD method
    a = Literal('a')
    b = Literal('b')
    c = Literal('c')
    d = Literal('a')
    cl = Clause()
    cl2 = Clause(b, c)
    cl.ADD(a)
    assert len(cl) == 1
    assert cl[0] == a
    cl.ADD(cl2)
    arr = [a, b, c]
    assert cl == arr
    cl.ADD(d)
    assert cl == arr
    with pytest.raises(TypeError):
        cl.ADD('a')

def test_clause_add_status():
    # test the clause effect of clause add method on the clause status attribute
    a = Literal('a')
    b = Literal('b')
    c = Literal('c')
    d = Literal('d')
    a2 = a.NOT()
    cl = Clause()
    cl.ADD(a)
    assert cl.get_status() == None
    cl.ADD(a2)
    assert cl._Clause__tautology_check() == True
    assert cl.get_status() == True
    cl2 = Clause()
    cl2.ADD(b)
    cl2.ADD(c)
    b.set_internal_status()
    c.set_internal_status()
    assert cl2.get_status() == True
    b.set_internal_status(False)
    c.set_internal_status(False)
    assert cl2.get_status() == False
    cl3 = Clause(a, d)
    cl2.ADD(cl3)
    assert cl2.get_status() == None

def test_clause_remove():
    # test the clause remove method
    a = Literal('a')
    b = Literal('b')
    c = Literal('c')
    d = Literal('b')
    cl = Clause(a, b, c)
    arr = [a, c]
    cl = cl.remove(b)
    for i, lit in enumerate(cl):
        assert lit == arr[i]
    with pytest.raises(TypeError):
        cl.remove('a')
    with pytest.raises(ValueError):
        cl.remove(d)
    cl = cl.remove(a)
    cl = cl.remove(c)
    assert cl.is_empty()

def test_clause_remove_status():
    # test the clause effect of clause remove method on the clause status attribute
    a = Literal('a')
    b = Literal('b')
    c = Literal('c')
    d = Literal('d')
    a2 = a.NOT()
    cl = Clause(a, b, c, d, a2)
    assert cl.get_status() == True
    cl = cl.remove(a2)
    assert cl.get_status() == None
    cl = cl.remove(a)
    a.set_internal_status()
    cl.ADD(a)
    assert cl.get_status() == True
    cl = cl.remove(a)
    assert cl.get_status() == None
    cl = cl.remove(b)
    cl = cl.remove(c)
    cl = cl.remove(d)
    assert cl.get_status() == False
    b.set_internal_status(False)
    c.set_internal_status(False)
    cl.ADD(b)
    cl.ADD(c)
    assert cl.get_status() == False

def test_clause_not():
    # test the clause not method
    a = Literal('a')
    b = Literal('b')
    c = Literal('c')
    cl = Clause(a, b, c)
    cl_neg = cl.NOT()
    assert isinstance(cl_neg, set)
    for lit in cl_neg:
        assert lit.get_sign() == 'neg'
    a = a.NOT()
    b = b.NOT()
    c = c.NOT()
    cl2 = Clause(a, b, c)
    cl2_neg = cl2.NOT()
    assert isinstance(cl2_neg, set)
    for lit in cl2_neg:
        assert lit.get_sign() == 'pos'

def test_get_clause():
    # test the clause get_clause method
    a = Literal('a')
    b = Literal('b')
    c = Literal('z')
    cl = Clause(a, b, c)
    assert cl.get_clause() == [a, b, c]

def test_is_empty():
    # test the clause is_empty method
    a = Literal('a')
    cl = Clause()
    assert cl.is_empty()
    cl.ADD(a)
    assert not cl.is_empty()

def test_len():
    # test the clause len method
    a = Literal('a')
    b = Literal('b')
    c = Literal('c')
    d = Literal('d')
    cl = Clause(a, b, c)
    assert len(cl) == 3
    cl.ADD(d)
    assert len(cl) == 4
    cl = cl.remove(a)
    assert len(cl) == 3

def test_clause_copy():
    # test the clause shallow copy method
    a = Literal('a')
    b = Literal('b')
    b = b.NOT()
    c = Literal('c')
    d = Literal('d')
    d = d.NOT()
    cl = Clause(a, b, c, d)
    cl2 = copy.copy(cl)
    assert cl == cl2

def test_clause_eq():
    # test the clause eq method
    a = Literal('a')
    b = Literal('b')
    c = Literal('a')
    d = Literal('b')
    arr = [a, b]
    cl = Clause(a, b)
    cl2 = Clause(c, d)
    assert arr == cl
    assert arr == cl2
    assert cl == cl2

def test_clause_contains():
    # test the clause contains method
    a = Literal('a')
    b = Literal('b')
    c = Literal('c')
    d = Literal('d')
    cl = Clause(a, b, c, d)
    arr = [a, b, c, d]
    for lit in arr:
        assert lit in cl