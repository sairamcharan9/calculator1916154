'''Testing Calculator'''
from calculator import add,subtraction

def test_addition():
    '''Testing addition function'''    
    assert add(2,2) == 4

def test_subtraction():
    '''Testing addition function'''
    assert subtraction(3,1) == 2
