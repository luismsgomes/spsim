
import munkres
from spsim.spsim import SpSim


class PhraseSpSim:
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
    '''
    def __init__(self, examples=None):
        self._sim = SpSim(examples=examples)
        self._dist_cache = {}

    def __call__(self, a, b):
        if isinstance(a, str):
            a, b = a.split(), b.split()
        # compute the length of the longest phrase (excluding spaces)
        L = max(sum(map(len, a)), sum(map(len, b)))
        if 1 == len(a) == len(b): return 1.0 - self._dist(a[0], b[0]) / L
        # let's obtain the (square) distance matrix
        if len(a) > len(b): b.extend(['']*(len(a)-len(b)))
        elif len(a) < len(b): a.extend(['']*(len(b)-len(a)))
        M = [[self._dist(p, q) for q in b] for p in a]
        # now compute the one to one assignment between a and b that
        # minimizes the sum of distances (this is "the assignment problem")
        D = sum(M[row][col] for row, col in munkres.Munkres().compute(M))
        # sometimes we might have a distance that is greater than the length
        # of either expressions if we happen to have a compound word in one
        # side; therefore we must limit D to be at most equal to L;
        # to mitigate this problem we should split compounds beforehand
        if D > L: D = L
        return 1.0 - D / L

    def _dist(self, a, b):
        # first check if this is a obvious case (those aren't cached)
        if a == b: return 0
        if '' == a: return len(b)
        if '' == b: return len(a)

        key = a + '\t' + b
        d = self._dist_cache.get(key, None)
        if d is None:
            d = (1.0 - self._sim(a, b)) * max(len(a), len(b))
            self._dist_cache[key] = d
        return d

    def learn(self, examples):
        self._sim.learn(examples)
        self._dist_cache.clear()