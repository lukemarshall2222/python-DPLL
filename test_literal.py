import pytest
import copy
from Literal import Literal

def test_literal_instance():
    # test the type of a Literal
    literal = Literal('a')
    assert isinstance(literal, Literal)

def test_literal_init():
    # test the Literal constructor
    a = Literal('a')
    assert a.get_variable() == 'a'
    assert a.get_sign() == 'pos'
    assert a.get_status() is None
    assert a.get_calculated_val() is None
    with pytest.raises(TypeError):
        b = Literal(7)

def test_literal_str():
    # test the Literal string representation
    a = Literal('a')
    b = Literal('b')
    b = b.NOT()
    assert str(a) == '+a'
    assert str(b) == '-b'

def test_literal_NOT():
    # test of the Literal NOT method
    a = Literal('a')
    assert a.get_sign() == 'pos'
    a = a.NOT()
    assert a.get_sign() == 'neg'

def test_literal_get_variable():
    # test the Literal get_variable method
    a = Literal('a')
    b = Literal('z')
    assert a.get_variable() == 'a'
    assert b.get_variable() == 'z'

def test_get_sign():
    # test the Literal get_sign method
    a = Literal('a')
    b = Literal('b')
    b = b.NOT()
    assert a.get_sign() == 'pos'
    assert b.get_sign() == 'neg'

def test_literal_status_and_val():
    # test literal set_status, get_status, set_calculated_val, and get_calculated_val methods
    a = Literal('a')
    a.set_status()
    print(a)
    assert a.get_sign() == 'pos'
    assert a.get_status() == True
    assert a.get_calculated_val() == True
    b = a.NOT()
    print(b)
    assert b.get_sign() == 'neg'
    assert b.get_status() == True
    assert b.get_calculated_val() == False
    c = b.NOT()
    c.set_status(False)
    assert c.get_sign() == 'pos'
    assert c.get_status() == False
    assert c.get_calculated_val() == False
    d = c.NOT()
    assert d.get_sign() == 'neg'
    assert d.get_status() == False
    assert d.get_calculated_val() == True

def test_literal_eq():
    # test the Literal eq method
    a = Literal('a')
    b = Literal('a')
    assert a == b
    b = b.NOT()
    assert a != b

def test_literal_hash():
    # test the Literal hash method
    a = Literal('a')
    b = Literal('a')
    sett = {a, b}
    assert len(sett) == 1
    b = b.NOT()
    sett = {a, b}
    assert len(sett) == 2
    
def test_literal_copy():
    # test the Literal shallow copy 
    a = Literal('a')
    a_cp = copy.copy(a)
    assert a.get_variable() == a_cp.get_variable()
    assert a.get_sign() == a_cp.get_sign()
    assert a.get_status() == a_cp.get_status()
    assert a.get_calculated_val() == a_cp.get_calculated_val()
    a = a.NOT()
    assert a.get_sign() != a_cp.get_sign()

def test_literal_bool():
    """test literal bool representation"""
    a = Literal('a')
    assert not bool(a)
    a.set_status()
    assert bool(a)


