"""Test suite for dpll.py"""

import pytest
from dpll import DPLL
from Literal import Literal
from Clause import Clause


def test_DPLL_instance():
    dpll = DPLL()
    assert isinstance(dpll, DPLL)
