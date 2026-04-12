#!/usr/bin/env python3
"""
Pan-parser - a parser for clauses in Pandunia and Panlingue.

This script tokenizes input text sentence by sentence, identifies phrases, and outputs syntax trees in text and SVG formats.

Example usage:
    python src/parser/main.py pandunia "mi pote basa la pandunia."

    Output:
    Parsing sentence: 'mi pote basa la pandunia.'
    Syntax tree: '(S (NP (PRP mi)) (VP (V pote) (VP (V basa) (NP (D la) (N pandunia.)))))'
"""

import sys
import svgling
import nltk
import pandunia_parser as pandunia
import panlingue_parser as panlingue

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

def parse_pandunia(sentence):
    parser = pandunia.pandunia_parser()
    tree_string = parser.tag_sentence(parser.word_tokenize(sentence))
    return tree_string

def parse_panlingue(sentence):
    parser = panlingue.panlingue_parser()
    tree_string = parser.tag_sentence(parser.word_tokenize(sentence))
    return tree_string

def main():
    """Main function to handle command-line execution."""
    if len(sys.argv) < 3:
        print("Usage: python main.py <language> \"Your text in the chosen language here\"")
        print("Example: python main.py panlingue \"me vero pota loga panlingue e no siti ali base.\"")
        print("Example: python main.py pandunia \"mi pote basa la pandunia. cing basa la pandunia! mi ame tu. mi tu ame.\"")
        sys.exit(1)

    # Get the input text from command-line arguments
    language = sys.argv[1].lower()
    input_text = ' '.join(sys.argv[2:])

    # Perform POS tagging sentence by sentence
    sentences = split_into_sentences(input_text)

    if language not in ['pandunia', 'panlingue']:
        print(f"Language '{language}' is not supported. Currently, only 'pandunia' and 'panlingue' are supported.")
        sys.exit(1)

    i = 0
    for sentence in sentences:
        print(f"Parsing sentence: '{sentence}'")
        if language == 'pandunia':
            tree_string = parse_pandunia(sentence)
        else:
            tree_string = parse_panlingue(sentence)
        print(f"Syntax tree: '{tree_string}'")
        filename = 'output/' + language + '/' +str(i) + '_' + sentence.strip('.').strip('!').strip('?').strip(',').replace(' ', '_') + '.svg'
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