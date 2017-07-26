=======
 spsim
=======

``spsim`` is a Python 3 module that implements a spelling similarity measure
for identifying cognates across languages, taking into account spelling
differences that are characteristic of each language pair, as described
in [Gomes2011]_.

Note: in the examples below, `$` denotes the Bash prompt and a Linux, MacOs or similar \*nix environment is assumed.

Install as usual::

    $ pip3 install spsim

Example command line usage::

    $ # first let's get some pairs of words that may be cognates:
    $ wget http://research.variancia.com/spsim/maybe_enpt.txt
    $ cat maybe_enpt.txt
    pharmacy    farmácia
    arithmetic  aritmética

    $ # If we don't give any example cognates, SpSim will be equivalent to
    $ #             1 - edit_distance / max_len_of_strings
    $ echo "" > empty.txt
    $ spsim empty.txt maybe_enpt.txt
    pharmacy    farmácia    0.375
    arithmetic  aritmética  0.7

    $ now let's get some example cognates:
    $ wget http://research.variancia.com/spsim/examples_enpt.txt
    $ cat examples_enpt.txt
    alcohol     álcool
    alpha       alfa
    anomaly     anomalia
    mathematics matemática
    methodology metodologia
    metric      métrica
    morphine    morfina
    photos      fotos

    $ # by giving these examples to spsim, it will learn to ignore certain differences:
    $ spsim examples_enpt.txt maybe_enpt.txt
    pharmacy    farmácia    1.0
    arithmetic  aritmética  1.0


.. [Gomes2011] Measuring Spelling Similarity for Cognate Identification,
    Luís Gomes and Gabriel Pereira Lopes
    in *Progress in Artificial Intelligence, 15th Portuguese Conference in
    Artificial Intelligence, EPIA 2011, Lisboa, Portugal, October 2011*,
    http://www.springerlink.com/content/gtl56j3l06906020/

