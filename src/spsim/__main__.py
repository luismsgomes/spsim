"""
Usage: spsim [options] <examples-file> [<input-file> [<output-file>]]

Options
    --phrases  Assume that input contains phrases instead of words.
    --case     Be case sensitive.
    --accents  Be sensitive to accents.
    --debug    Output two additional columns with known and unknown
               differences found on each word pair.
               Warning: this option will not work correctly with --phrases.
"""

import logging
import sys
import docopt
import openfile
from spsim import PhraseSpSim, SpSim


LOGGER = logging.getLogger("spsim")


def main(argv=sys.argv):
    logging.basicConfig()
    opts = docopt.docopt(__doc__)
    cls = PhraseSpSim if opts["--phrases"] else SpSim
    sim = cls(
        ignore_case=not opts["--case"],
        ignore_accents=not opts["--accents"],
    )
    with (openfile.openfile(opts["<examples-file>"])) as lines:
        sim.learn(
            line.rstrip("\n").split("\t")[:2] for line in lines if "\t" in line
        )
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
