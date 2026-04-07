#!/usr/bin/env python3
"""
Pan-parser - a parser for clauses in Pandunia.

This script tokenizes input text sentence by sentence, identifies phrases, and outputs syntax trees in text and SVG formats.

Example usage:
    python src/parser/main.py pandunia "mi pote basa la pandunia."

    Output:
    Parsing sentence: 'mi pote basa la pandunia.'
    Syntax tree: '(S (NP (PRP mi)) (VP (V pote) (VP (V basa) (NP (D la) (N pandunia.)))))'

    "mi pote basa la pandunia. cing basa la pandunia! mi ama tu. mi tu ama. mi marce. mi su doste fu vide tu su doste. mi su doste tu su doste fu vide."

"""

import sys
import string
import svgling
import nltk
import pandunia_parser as pandunia

consonants = 'bcdfghjklmnpqrstvwxyz'
vowels = 'aeiou'

def split_into_sentences(text):
    """
    Split the input text into sentences based on punctuation.

    Args:
        text (str): The input text to split.

    Returns:
        list: A list of sentences.
    """
    sentences = []
    current_sentence = ""
    for char in text:
        current_sentence += char
        if char in '.!?':
            sentences.append(current_sentence.strip())
            current_sentence = ""
    if current_sentence:
        sentences.append(current_sentence.strip())
    return sentences

def word_tokenize(text):
    """
    Tokenize the input text into words.

    Args:
        text (str): The input text to tokenize.

    Returns:
        list: A list of tokens.
    """
    # Simple tokenization based on whitespace and punctuation
    tokens = text.split()
    return tokens

def count_syllables(lower_token):
    """
    Count the number of syllables in a token.

    Args:
        lower_token (str): The token in lowercase.

    Returns:
        int: The number of syllables in the token.
    """
    syllables = 0
    if lower_token[0] in vowels:
        syllables += 1

    if len(lower_token) > 1:
        for i in range(len(lower_token) - 1):
            if lower_token[i] in consonants and lower_token[i+1] in vowels:
                syllables += 1
    return syllables

def get_PoS_of_monosyllabic(lower_token):
    # Placeholder implementation - replace with actual logic
    if lower_token in ['e', 'o', 'pero']:
        return 'C'  # Conjunction
    elif lower_token in ['me', 'tu', 'ho']:
        return 'PR'  # Pronoun
    elif lower_token in ['no']:
        return 'AV'  # Adverb
    elif lower_token in ['un', 'du', 'tri', 'car']:
        return 'NU'  # Numeral
    else:
        return 'N'  # Noun

def get_PoS_of_polysyllabic(lower_token):
    last = lower_token[-1]
    beforelast = lower_token[-2]
    if beforelast in consonants and last == 'a':
        return 'V-a'  # Agent-fronted verb
    elif beforelast in consonants and last == 'u':
        return 'V-u'  # Patient-fronted verb
    elif beforelast in consonants and last == 'i':
        return 'AJ'  # Adjective
    elif beforelast in consonants and last == 'o':
        return 'AV'  # Adverb
    else:
        return 'N'  # Noun

def pos_tag_panlingue(tokens):
    """
    Perform part-of-speech tagging on the list of tokens.

    Args:
        tokens (list): A list of tokens to tag.
    Returns:
        list: A list of [word, tag] pairs.
    """
    pos_tags = []
    for token in tokens:
        if token in string.punctuation:
            pos_tags.append([token, ''])
            continue
        lower_token = token.lower()
        syllables = count_syllables(lower_token)

        if syllables == 1:
            pos_tags.append([token, get_PoS_of_monosyllabic(lower_token)])
        else:
            pos_tags.append([token, get_PoS_of_polysyllabic(lower_token)])
    return pos_tags

def main():
    """Main function to handle command-line execution."""
    if len(sys.argv) < 3:
        print("Usage: python main.py <language> \"Your text in the chosen language here\"")
        print("Example: python main.py panlingue \"me vero pota loga panlingue e no siti ali base.\"")
        print("Example: python main.py pandunia \"mi pote basa la pandunia. cing basa la pandunia! mi ame tu. mi tu ame.\"")
        sys.exit(1)

    # Get the input text from command-line arguments
    language = sys.argv[1]
    input_text = ' '.join(sys.argv[2:])

    # Perform POS tagging sentence by sentence
    sentences = split_into_sentences(input_text)

    if language.lower() != 'pandunia':
        print(f"Language '{language}' is not supported. Currently, only 'pandunia' is supported.")
        sys.exit(1)

    i = 0
    for sentence in sentences:
        print(f"Parsing sentence: '{sentence}'")
        parser = pandunia.pandunia_parser()
        tree_string = parser.tag_sentence(parser.word_tokenize(sentence))
        print(f"Syntax tree: '{tree_string}'")
        filename = str(i) + '_' + sentence.strip('.').strip('!').strip('?').strip(',').replace(' ', '_') + '.svg'
        x = nltk.Tree.fromstring(tree_string)
        svgling.draw_tree(x, leaf_nodes_align=True).saveas(filename, pretty=True)
        i += 1

        #svgling.draw_tree(tree, leaf_nodes_align=True).saveas("parsed_sentence.svg", pretty=True)
        #parser = pandunia.first_pandunia_parser()
        #pos_tags = parser.pos_tag_text(sentence)
        #parser.print_PoS_tags_below_words(pos_tags)
        #parser.identify_phrases(pos_tags)

    # Toimii!
    #svgling.draw_tree(("S", ("NP", ("D", "the"), ("N", "elephant")), ("VP", ("V", "saw"), ("NP", ("D", "the"), ("N", "rhinoceros"))))).saveas("demotree.svg", pretty=True)

    # Toimii myös!
    #x = nltk.Tree.fromstring("(S (NP (D the) (N elephant)) (VP (V saw) (NP (D the) (N rhinoceros))))")
    #svgling.draw_tree(x, leaf_nodes_align=True).saveas("demotree2.svg", pretty=True)


if __name__ == "__main__":
    main()