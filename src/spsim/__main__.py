import sys
from spsim import PhraseSpSim

def main(argv=sys.argv):
    if len(argv) != 3:
        print('Usage: spsim <examplesfile> <inputfile>', file=sys.stderr)
        sys.exit(2)
    exfile, infile = argv[1:]
    sim = PhraseSpSim()
    with (open(exfile)) as lines:
        sim.learn(
            line.rstrip("\n").split("\t") for line in lines if "\t" in line
        )
    with (sys.stdin if infile == '-' else open(infile)) as lines:
        for n, line in enumerate(lines, start=1):
            cols = line.strip().split('\t')
            if 2 > len(cols):
                msg = 'Error: Line {:d} of {} has less than 2 columns.'
                sys.exit(msg.format(n, infile))
            cols.append(sim(cols[0], cols[1]))
            print(*cols, sep='\t')


if __name__ == '__main__':
    main()
