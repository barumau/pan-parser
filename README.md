# Syntax Parsers for Pan-Languages

Pan-languages are a family of three constructed auxiliary languages, Pandunia, Panglo and Panlingue,
that have mostly similar words, and mostly similar word orders, but fundamentally different ways to encode syntactic roles.
The purpose of this repository is, on one hand, to code their grammars in syntax parsers in Python for mutual comparison,
and, on the other hand, to develop common utility tools for computational processing of these languages.

## About the Pan-languages

Currently the parser supports the following languages:

1.  Pandunia

    The syntax of Pandunia is based on default word classes.
    The main distinction runs between structure words and content words.

    Structure words are closed classes of words,
    including pronouns, numerals, conjunctions and
    pure verbs, which include copula verbs and auxiliary verbs.

    Content words have a natural default word class.

    -   Thing words are syntactically nominals.
    -   Quality words can be syntactically modifiers (adjectives and adverbs) or nominals.
    -   Action words can be syntactically either verbs (actions) or nominals (products of actions).

2.  Panglo

    The syntax of Panglo is based heavily on structure words.
    Content words are part of speech agnostic.
    Their syntactic role depends on surrounding structure words and on word order.
    For example, noun phrases begin with a determiner,
    and verb phrases begin with a tense/aspect/mood marker or they are immediately preceded by a personal pronoun.

3.  Panlingue

    The syntax of Panlingue is based on word-class markers (or part of speech (PoS) markers) and word order.
    Verbs end in *-a* or *-u*, adverbs end in *-o*, adjectives end in *-i*,
    and nouns end *-e* or in any other letter than the previously mentioned endings.

## Applications

### Making syntax trees

The panlingual parser creates syntax trees in textual NLTK format and in gaphical tree format.
The program takes two parameters: language name and the text to be parsed inside double quotes.

Type `python src/parser/parse.py` without any parameters to get usage instructions.

Example usage:

    $ python src/parser/parse.py pandunia "mi pote loge dunia basa."

    Parsing sentence: 'mi pote loge dunia basa.'
    [('PRP', 'mi'), ('V', 'pote'), ('V', 'loge'), ('N', 'dunia'), ('N', 'basa.')]
    Determined constituent order: SVO
    Syntax tree: '(S (NP (PRP mi)) (VP (V pote) (VP (V loge) (NP (N dunia) (N basa.)))))'

It also creates `./output/pandunia/0_mi_pote_loge_dunia_basa.svg` file,
which is a graphical representation of the syntax tree, as below.

![](output/pandunia/0_mi_pote_loge_dunia_basa.svg)
