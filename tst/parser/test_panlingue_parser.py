#test.py
# Run these tests with the command: python -m unittest test_panlingue_parser.py
import unittest
from src.parser import panlingue_parser as panlingue

def add(a, b):
    return a + b

class TestPanlingueParser(unittest.TestCase):
    def setUp(self):
        self.parser = panlingue.panlingue_parser()

    def test_word_tokenize(self):
        text = "Hello, world! This is a test."
        expected_tokens = ["Hello,", "world!", "This", "is", "a", "test."]
        self.assertEqual(self.parser.word_tokenize(text), expected_tokens)

    def test_adjective_identification(self):
        adjectives = ['novik', 'duniatik', 'internasianal', 'natural']
        for adj in adjectives:
            self.assertEqual(self.parser.identify_word_class(adj), "A")

    def test_subject_fronted_verb_identification(self):
        verbs = ['parlar', 'vider', 'volir', 'evolur']
        for verb in verbs:
            self.assertEqual(self.parser.identify_word_class(verb), "V")

    def test_object_fronted_verb_identification(self):
        verbs = ['parlas', 'vides', 'volis', 'evolus']
        for verb in verbs:
            self.assertEqual(self.parser.identify_word_class(verb), "V")

    def test_noun_identification(self):
        nouns = ['kitabe', 'kaze', 'doste', 'ban']
        for noun in nouns:
            self.assertEqual(self.parser.identify_word_class(noun), "N")

    def test_personal_pronoun_identification(self):
        pronouns = ['mi', 'tu', 'ho', 'mimen', 'tumen', 'homen']
        for pronoun in pronouns:
            self.assertEqual(self.parser.identify_word_class(pronoun), "PRP")

    def test_empty_string_identification(self):
        self.assertEqual(self.parser.identify_word_class(""), "")

    def test_tag_word_classes(self):
        tokens = ['mi', 'parlar', 'novik', 'kitabe']
        expected_tagged = [('PRP', 'mi'), ('V', 'parlar'), ('A', 'novik'), ('N', 'kitabe')]
        self.assertEqual(self.parser.tag_word_classes(tokens), expected_tagged)

    def test_pronoun_SVO_clause(self):
        tokens = ["mi", "amar", "tu"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (PRP mi)) (VP (V amar) (NP (PRP tu))))")

    def test_pronoun_SOV_clause(self):
        tokens = ["mi", "tu", "amas"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (PRP mi)) (VP (NP (PRP tu)) (V amas)))")

    def test_pronoun_OVS_clause(self):
        tokens = ["tu", "amas", "mi"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (VP (NP (PRP tu)) (V amas)) (NP (PRP mi)))")

    def test_pronoun_OSV_clause(self):
        # Note: Currently we don't deal with constituent movement in the syntax tree.
        tokens = ["tu", "mi", "amar"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (PRP tu)) (NP (PRP mi)) (VP (V amar)))")

    def test_pronoun_VOS_clause(self):
        tokens = ["amar", "tu", "mi"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (VP (V amar) (NP (PRP tu))) (NP (PRP mi)))")

    def test_noun_SVO_clause(self):
        tokens = ["jen", "volir", "parlar", "novik", "basa"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (N jen)) (VP (V volir) (VP (V parlar) (NP (A novik) (N basa)))))")

if __name__ == '__main__':
    unittest.main()