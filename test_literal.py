import pytest
from Literal import Literal

def test_literal_instance():
    # test the types of objects
    literal = Literal('a')
    assert isinstance(literal, Literal)

def test_literal_init():
    # testing the Literal constructor
    a = Literal('a')
    assert a.get_variable() == 'a'
    assert a.get_sign() == 'pos'
    assert a.get_status() is None
    assert a.get_calculated_val() is None
    with pytest.raises(TypeError):
        b = Literal(7)

def test_literal_NOT():
    # test of the Literal NOT method
    a = Literal('a')
    assert a.get_sign() == 'pos'
    a = a.NOT()
    assert a.get_sign() == 'neg'

def test_literal_status_val():
    # test literal set_status and get_status methods
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

def test_literal_bool():
    """Tests literal bool method"""
    a = Literal('a')
    assert not bool(a)
    a.set_status()
    assert bool(a)
