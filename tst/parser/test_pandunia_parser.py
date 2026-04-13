#test.py
# Run these tests with the command: python -m unittest test_pandunia_parser.py
import unittest
from src.parser import pandunia_parser as pandunia

def add(a, b):
    return a + b

class TestPanduniaParser(unittest.TestCase):
    def setUp(self):
        self.parser = pandunia.pandunia_parser()

    def test_word_tokenize(self):
        text = "Hello, world! This is a test."
        expected_tokens = ["Hello,", "world!", "This", "is", "a", "test."]
        self.assertEqual(self.parser.word_tokenize(text), expected_tokens)

    def test_2_word_NP(self):
        tokens = ["la", "basa"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (D la) (N basa)))")

    def test_another_2_word_NP(self):
        tokens = ["un", "basa"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (D un) (N basa)))")

    def test_imperative_VO_VP(self):
        tokens = ["basa", "la", "pandunia"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (VP (V basa) (NP (D la) (N pandunia))))")

    def test_request_VP(self):
        tokens = ["cing", "basa", "la", "pandunia"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (VP (V cing) (VP (V basa) (NP (D la) (N pandunia)))))")

    def test_pronoun_SVO_clause(self):
        tokens = ["mi", "ama", "tu"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (PRP mi)) (VP (V ama) (NP (PRP tu))))")

    def test_pronoun_noun_SVO_clause(self):
        tokens = ["mi", "basa", "la", "pandunia"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (PRP mi)) (VP (V basa) (NP (D la) (N pandunia))))")

    def test_noun_SVO_clause(self):
        tokens = ["la", "jen", "fu", "basa", "la", "pandunia"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (D la) (N jen)) (VP (V fu) (V basa) (NP (D la) (N pandunia))))")

    def test_pronoun_SOV_clause(self):
        tokens = ["mi", "tu", "ama"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (PRP mi)) (VP (NP (PRP tu)) (V ama)))")

    def test_pronoun_noun_SOV_clause(self):
        tokens = ["mi", "un", "fem", "sta", "ama"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (PRP mi)) (VP (NP (D un) (N fem)) (V sta) (V ama)))")

    def test_noun_noun_SOV_clause(self):
        tokens = ["la", "nam", "un", "fem", "sta", "ama"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (D la) (N nam)) (VP (NP (D un) (N fem)) (V sta) (V ama)))")

    def test_possessive_pronoun_SVO_clause(self):
        tokens = ["mi","su", "doste", "sta", "ama", "tu", "su", "doste"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (PRP$ mi su) (N doste)) (VP (V sta) (V ama) (NP (PRP$ tu su) (N doste))))")

    def test_possessive_pronoun_SOV_clause(self):
        tokens = ["mi","su", "doste", "tu", "su", "doste", "sta", "ama"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (PRP$ mi su) (N doste)) (VP (NP (PRP$ tu su) (N doste)) (V sta) (V ama)))")

    def test_unmarked_object_in_SVO(self):
        tokens = ["mi", "basa", "pandunia"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (PRP mi)) (VP (V basa) (NP (N pandunia))))")

    def test_unmarked_object_NP_in_SVO(self):
        tokens = ["mi", "basa", "pandunia"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (PRP mi)) (VP (V basa) (NP (N pandunia))))")

    def test_long_unmarked_object_NP_in_SVO(self):
        tokens = ["mi", "basa", "nova", "dunia", "basa"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (PRP mi)) (VP (V basa) (NP (N nova) (N dunia) (N basa))))")

    def test_unmarked_object_NP_in_request_VO(self):
        tokens = ["cing", "basa", "pandunia"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (VP (V cing) (VP (V basa) (NP (N pandunia)))))")

    def test_long_unmarked_object_NP_in_request_VO(self):
        tokens = ["cing", "basa", "nova", "dunia", "basa"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (VP (V cing) (VP (V basa) (NP (N nova) (N dunia) (N basa)))))")


if __name__ == '__main__':
    unittest.main()