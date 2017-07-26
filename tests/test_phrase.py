import pytest
from spsim import PhraseSpSim


def test_equal():
    sim = PhraseSpSim()
    assert sim('', '') == 1.0
    assert sim('abc', 'abc') == 1.0
    assert sim('abc def', 'abc def') == 1.0
    assert sim(['a'], 'a') == 1.0
    assert sim('a', ['a']) == 1.0
    assert sim(['a'], ['a']) == 1.0

def test_reorderings():
    sim = PhraseSpSim()
    assert sim('abc def', 'def abc') == 1.0
    assert sim('telephone', 'telefone') == 1 - 2/len('telephone')
    assert sim('my', 'o meu') == 1 - 3/len('omeu')
    sim.learn([('telephone', 'telefone')])
    assert sim('telephone', 'telefone') == 1.0
    assert sim('my telephone', 'o meu telefone') == 1 - 3/len('omeutelefone')
    sim.learn([('my', 'meu')])
    assert sim('my telephone', 'o meu telefone') == 1 - 1/len('omeutelefone')

    sim = PhraseSpSim()
    assert sim('a b c', 'c b') == 1.0 - 1/3


def test_compounds():
    sim = PhraseSpSim()
    assert sim('abc' , 'a b c') == 1.0
    assert sim('a b c' , 'abc') == 1.0


def test_args():
    sim = PhraseSpSim()
    with pytest.raises(ValueError):
        sim(1, '')
    with pytest.raises(ValueError):
        sim('', {})

    assert sim('', 'a') == 0.0
    assert sim('a', '') == 0.0
