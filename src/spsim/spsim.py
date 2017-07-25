from stringology.align import align, mismatches
from stringology.text import remove_accents


class SpSim:
    """
    SpSim is a spelling similarity measure for identifying cognates by
    learning cross-language spelling differences.

    >>> sim = SpSim()
    >>> sim('phase', 'fase')
    0.6

    Learning contextualized spelling differences from an example:

    >>> sim.learn([('alpha', 'alfa')])
    >>> sorted(sim.diffs.items())
    [('ph\\tf', 'la')]

    SpSim has learned that 'ph' may be replaced by 'f' if 'ph' comes after 'l'
    and before 'a'.

    Generalizing the admissible contexts of known spelling differences:

    >>> sim.learn([('phase', 'fase')])
    >>> sorted(sim.diffs.items())
    [('ph\\tf', '*a')]

    SpSim has learned that 'ph' may be replaced by 'f' if it comes before 'a'.

    >>> sim.learn([('photo', 'foto')])
    >>> sorted(sim.diffs.items())
    [('ph\\tf', '**')]

    SpSim has learned that 'ph' may be replaced by 'f'.

    >>> sim('phenomenal', 'fenomenal')
    1.0

    """

    def __init__(self,
                 examples=None,
                 ignore_case=True,
                 ignore_accents=True,
                 group_vowels=False,
                 no_empty=False):
        self.ignore_case = ignore_case
        self.ignore_accents = ignore_accents
        self.group_vowels = group_vowels
        self.no_empty = no_empty
        self.diffs = {}
        if examples:
            self.learn(examples)

    def __call__(self, a, b, known=None, unknown=None):
        a, b = self._prepare(a, b)
        dist = 0  # total distance
        for nchars, diff, ctxt in self._get_diffs(a, b):
            if not SpSim._match_context(ctxt, self.diffs.get(diff, None)):
                dist += nchars
                if unknown is not None:
                    unknown.append((diff, ctxt))
            elif known is not None:
                known.append((diff, ctxt))
        return 1.0 - dist / max(1, len(a), len(b))

    def learn(self, examples, trace_fn=None):
        for a, b in examples:
            a, b = self._prepare(a, b)
            for _, diff, ctxt in self._get_diffs(a, b):
                before = self.diffs.get(diff, None)
                after = SpSim._generalize_context(before, ctxt)
                self.diffs[diff] = after
                if trace_fn is not None:
                    trace_fn(a, b, diff, before, after)

    def _prepare(self, a, b):
        if self.ignore_case:
            a, b = a.lower(), b.lower()
        if self.ignore_accents:
            a, b = remove_accents(a), remove_accents(b)
        return a, b

    def _get_diffs(self, a, b):
        alignment = align(" ^" + a + "$ ", " ^" + b + "$ ", gap=" ")
        for mma, mmb in mismatches(*alignment, context=2):
            nchars = len(mma) - 4  # discount the left and right context chars
            diffa = mma[2:-2].replace(" ", "")
            diffb = mmb[2:-2].replace(" ", "")
            ctxtl = mma[1]
            ctxtr = mma[-2]
            if self.no_empty and (not diffa or not diffb):
                if diffa.startswith(ctxtl) or diffb.startswith(ctxtl):
                    diffa = mma[1:-2].replace(" ", "")
                    diffb = mmb[1:-2].replace(" ", "")
                    ctxtl = mma[0]
                elif diffa.endswith(ctxtr) or diffb.endswith(ctxtr):
                    diffa = mma[2:-1].replace(" ", "")
                    diffb = mmb[2:-1].replace(" ", "")
                    ctxtr = mma[-1]
                else:
                    diffa = mma[1:-1].replace(" ", "")
                    diffb = mmb[1:-1].replace(" ", "")
                    ctxtl = mma[0]
                    ctxtr = mma[-1]
            ctxtl = self._get_context_repr(ctxtl)
            ctxtr = self._get_context_repr(ctxtr)
            yield nchars, diffa + "\t" + diffb, ctxtl + ctxtr

    def _get_context_repr(self, char):
        # TODO: add vowels for other alphabets
        if self.group_vowels and char in "aeiou":
            return "a"  # vowel representative
        return char

    @staticmethod
    def _match_context(ctxt, learned):
        return (
            learned and
            learned[0] in "*" + ctxt[0] and
            learned[1] in "*" + ctxt[1]
        )

    @staticmethod
    def _generalize_context(learned, ctxt):
        if not learned:
            return ctxt
        lft = "*" if learned[0] != ctxt[0] else learned[0]
        rgt = "*" if learned[1] != ctxt[1] else learned[1]
        return lft + rgt
