"""
Usage: spsim [options] <examples-file> [<input-file> [<output-file>]]

Options
    --trace <fname>
                Save learned differences into specified file.
    --phrases   Assume that input contains phrases instead of words.
    --case      Be case sensitive.
    --accents   Be sensitive to accents.
    --debug     Output two additional columns with known and unknown
                differences found on each word pair.
                Warning: this option will not work correctly with --phrases.
    --vowels    Group vowels.
    --no-empty  Ensure differences are not empty on any side.
"""

import logging
import docopt
import openfile
from spsim import PhraseSpSim, SpSim


LOGGER = logging.getLogger("spsim")


def read_examples(fname):
    with (openfile.openfile(fname)) as lines:
        for line in lines:
            columns = line.rstrip("\n").split("\t")
            if len(columns) >= 2:
                yield columns[:2]


def main():
    logging.basicConfig()
    opts = docopt.docopt(__doc__)
    cls = PhraseSpSim if opts["--phrases"] else SpSim
    sim = cls(
        ignore_case=not opts["--case"],
        ignore_accents=not opts["--accents"],
        group_vowels=opts["--vowels"],
        non_empty_diffs=opts["--no-empty"],
    )
    examples = read_examples(opts["<examples-file>"])
    if opts["--trace"]:
        with (openfile.openfile(opts["--trace"], "wt")) as out:
            def trace(a, b, diff, before, after):
                diffa, diffb = diff.split("\t")
                after_repr = "%s[%s]%s <=> %s[%s]%s" % (
                    after[0], diffa, after[1],
                    after[0], diffb, after[1],
                )
                if before and before != after:
                    before_repr = "%s[%s]%s <=> %s[%s]%s" % (
                        before[0], diffa, before[1],
                        before[0], diffb, before[1],
                    )
                    out.write("%s<=>%s => %s => %s\n" % (
                        a, b, before_repr, after_repr
                    ))
                else:
                    out.write("%s<=>%s => %s\n" % (a, b, after_repr))

            sim.learn(examples, trace_fn=trace)
    else:
        sim.learn(examples)
    inputfile = openfile.openfile(opts["<input-file>"])
    outputfile = openfile.openfile(opts["<output-file>"], "wt")
    debug = opts["--debug"]
    with inputfile, outputfile:
        for num, line in enumerate(inputfile, start=1):
            cols = line.rstrip('\n').split('\t')
            if len(cols) < 2:
                LOGGER.warning(
                    'line %d of %s has less than 2 columns; skipping',
                    num, opts["<input-file>"]
                )
                continue

            if debug:
                known, unknown = [], []
                cols.append(sim(cols[0], cols[1], known=known, unknown=unknown))
                cols.append(" ".join(d.replace("\t", "<=>") for d in known))
                cols.append(" ".join(d.replace("\t", "<?>") for d in unknown))
            else:
                cols.append(sim(cols[0], cols[1]))
            print(*cols, sep='\t', file=outputfile)


if __name__ == '__main__':
    main()
