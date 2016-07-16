from spsim import SpSim


def test_equal():
    sim = SpSim()
    assert sim('', '') == 1.0
    assert sim('abc', 'abc') == 1.0


def test_unrelated():
    sim = SpSim()
    assert sim('abc', '') == 0.0
    assert sim('', 'abc') == 0.0
    assert sim('abc', 'def') == 0.0


def test_learning_ph():
    sim = SpSim()
    assert sim('telephone', 'telefone') == 1 - 2/len('telephone')
    sim.learn([('telephone', 'telefone')])
    assert sim('telephone', 'telefone') == 1.0
    # test constructor with examples:
    assert sim.diffs == SpSim([('telephone', 'telefone')]).diffs
    # sim has learned epho -> efo but not ^pha -> ^fa
    assert sim('phase', 'fase') == 1 - 2/len('phase')
    sim.learn([('phase', 'fase')])
    # sim has now learned ph -> f
    assert sim('phase', 'fase') == 1.0
    assert sim('Daphnias', 'Dafnias') == 1.0
