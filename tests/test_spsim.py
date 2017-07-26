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


def test_ignore_case():
    sim = SpSim(ignore_case=True)
    assert sim('telephone', 'telefone') == 1 - 2/len('telephone')
    sim.learn([('telephone', 'telefone')])
    assert sim('telephone', 'telefone') == 1.0
    assert sim('TELEPHONE', 'TELEFONE') == 1.0

    sim = SpSim(ignore_case=False)
    assert sim('telephone', 'telefone') == 1 - 2/len('telephone')
    sim.learn([('telephone', 'telefone')])
    assert sim('telephone', 'telefone') == 1.0
    assert sim('TELEPHONE', 'TELEFONE') == 1 - 2/len('TELEPHONE')
    sim.learn([('TELEPHONE', 'TELEFONE')])
    assert sim('TELEPHONE', 'TELEFONE') == 1.0


def test_ignore_accents():
    sim = SpSim(ignore_accents=True)
    assert sim('atom', 'átomo') == 1 - 1/len('átomo')
    sim = SpSim(ignore_accents=False)
    assert sim('atom', 'átomo') == 1 - 2/len('átomo')


def test_group_vowels():
    sim = SpSim(group_vowels=False)
    sim.learn([('phase', 'fase')])
    assert sim('phone', 'fone') == 1 - 2/len('phone')

    sim = SpSim(group_vowels=True)
    sim.learn([('phase', 'fase')])
    assert sim('phone', 'fone') == 1.0


def test_trace():
    sim = SpSim()
    result = []
    sim.learn([('phase', 'fase')], trace_fn=lambda *args: result.append(args))
    assert result == [('phase', 'fase', 'ph\tf', None, '^a')]


def test_debug():
    sim = SpSim([('phase', 'fase')])

    known = []
    unknown = []
    sim('telephone', 'telefone', known=known, unknown=unknown)
    assert known == []
    assert unknown == [('ph\tf', 'eo')]

    known = []
    unknown = []
    sim('phase', 'fase', known=known, unknown=unknown)
    assert known == [('ph\tf', '^a')]
    assert unknown == []


def test_no_empty():
    sim = SpSim(no_empty=False)
    sim.learn([('immediate', 'imediato'), ('contractual', 'contratual')])
    assert 'm\t' in sim.diffs
    assert 'mm\tm' not in sim.diffs
    assert 'c\t' in sim.diffs
    assert 'act\tat' not in sim.diffs

    sim = SpSim(no_empty=True)
    sim.learn([('immediate', 'imediato'), ('contractual', 'contratual')])
    assert 'm\t' not in sim.diffs
    assert 'mm\tm' in sim.diffs
    assert 'c\t' not in sim.diffs
    assert 'act\tat' in sim.diffs

    sim = SpSim(no_empty=True)
    # this is an artificial test case but it is needed for 100% code coverage
    # it tests a branch that would only be executed if stringology.align.align()
    # changed its behaviour and instead of align('abc', 'abbc') => ('ab c', 'abbc')
    # it would return align('abc', 'abbc') => ('a bc', 'abbc')
    sim.learn([('a bc', 'abbc')])
    assert '\tc' not in sim.diffs
    assert 'b\tbb' in sim.diffs
