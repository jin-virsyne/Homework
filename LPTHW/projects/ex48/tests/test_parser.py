from ex48.parser import *
import pytest

def test_simple_sentence():
    x = Parser.parse_sentence([('verb', 'run'), ('direction', 'north')])
    assert x.subject == 'player'
    assert x.verb == 'run'
    assert x.object == 'north'
    
def test_complex_sentence():
    x = Parser.parse_sentence([('noun', 'bear'), ('verb', 'eat'), 
                        ('stop', 'the'),('noun', 'honey')])
    assert x.subject == 'bear'
    assert x.verb == 'eat'
    assert x.object == 'honey'
    
def test_exception():
    with pytest.raises(Exception):
        Parser.parse_sentence([('verb', 'run'), ('verb', 'run')])