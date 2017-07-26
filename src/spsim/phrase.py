import itertools

import munkres
from spsim.spsim import SpSim


class PhraseSpSim(SpSim):
    '''
    Measures the similarity between pairs of phrases using SpSim for comparing
    words.

    A phrase is a sequence one or more words.

                January 2010, Luís Gomes <luismsgomes@gmail.com>

    Works as follows:
    1 - Compute the distance between each word A of one phrase and each word B
        of the  other phrase using (1 - SpSim(A, B)) * max(len(A), len(B)).
    2 - Compute the one-to-one assignment of words from one phrase to words
        of the other phrase that minimizes the sum of all pair distances. If
        the phrases have a different number of words, then we add null words
        to the shortest phrase. The distance between any word C and null is
        len(C).
    3 - The similarity score is computed as 1 - D/L, where D is the minimum
        total distance (computed in 2) and L is the length of the longest
        phrase, excluding whitespace.

    Step 2 is computed using the Munkres algorithm (aka Hungarian). Note that
    the problem solved in step 2 is widely known as "the assignment problem".

    >>> sim = PhraseSpSim()
    >>> sim.learn([('photo', 'foto'), ('alpha', 'alfa'), ('pangea', 'pangeia')])
    >>> sorted(sim.diffs.items())
    [('\\ti', 'ea'), ('ph\\tf', '**')]

    SpSim has learned that 'ph' may be replaced by 'f' and 'ea' by 'eia'.

    >>> sim('phenomenal idea', 'ideia fenomenal')
    1.0

    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __call__(self, a, b, known=None, unknown=None):
        # TODO: update known and unknown lists, when given
        if isinstance(a, str):
            a = a.split()
        if isinstance(b, str):
            b = b.split()
        if not isinstance(a, (list, tuple)) or not isinstance(b, (list, tuple)):
            raise ValueError
        if a == b:
            return 1.0
        if not a or not b:
            return 0.0
        if len(a) == 1 or len(b) == 1:
            if len(a) == len(b):  # == 1
                sim = SpSim.__call__(self, a[0], b[0])
            else:
                sim = self._match_compound(a, b)
                if sim < 1.0:
                    sim = max(sim, self._match_words(a, b))
        else:
            sim = self._match_words(a, b)
        return sim

    def _match_compound(self, a, b):
        assert len(a) == 1 or len(b) == 1
        if len(a) == 1:
            return max(
                SpSim.__call__(self, a[0], ''.join(bp))
                for bp in itertools.permutations(b)
            )
        return max(
            SpSim.__call__(self, ''.join(ap), b[0])
            for ap in itertools.permutations(a)
        )

    def _match_words(self, a, b):
        # compute the length of the longest phrase (excluding spaces)
        L = max(sum(map(len, a)), sum(map(len, b)))
        # let's obtain the (square) distance matrix
        if len(a) > len(b):
            b.extend(['']*(len(a)-len(b)))
        elif len(a) < len(b):
            a.extend(['']*(len(b)-len(a)))
        M = [[self._dist(p, q) for q in b] for p in a]
        # now compute the one to one assignment between a and b that
        # minimizes the sum of distances (this is "the assignment problem")
        D = sum(M[row][col] for row, col in munkres.Munkres().compute(M))
        return 1.0 - D / L
