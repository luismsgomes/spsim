"""
Usage: spsim <examples-file> [<input-file> [<output-file>]]
"""

import docopt
import openfile
import logging
import sys
from spsim import PhraseSpSim


logger = logging.getLogger("spsim")


def main(argv=sys.argv):
    logging.basicConfig()
    opts = docopt.docopt(__doc__)
    sim = PhraseSpSim()
    with (openfile.openfile(opts["<examples-file>"])) as lines:
        sim.learn(
            line.rstrip("\n").split("\t")[:2] for line in lines if "\t" in line
        )
    inputfile = openfile.openfile(opts["<input-file>"])
    outputfile = openfile.openfile(opts["<output-file>"], "wt")
    with inputfile, outputfile:
        for num, line in enumerate(inputfile, start=1):
            cols = line.rstrip('\n').split('\t')
            if 2 > len(cols):
                logger.warning(
                    'line %d of %s has less than 2 columns; skipping',
                    num, opts["<input-file>"]
                )
                continue
            cols.append(sim(cols[0], cols[1]))
            print(*cols, sep='\t', file=outputfile)


if __name__ == '__main__':
    main()
