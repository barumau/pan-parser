#test.py
# Run these tests with the command: python -m unittest test_panglo_parser.py
import unittest
from src.parser import panglo_parser as panglo

class TestPangloParser(unittest.TestCase):
    def setUp(self):
        self.parser = panglo.panglo_parser()

    def test_word_tokenize(self):
        text = "halo, globe! dis es un teste."
        expected_tokens = ["halo,", "globe!", "dis", "es", "un", "teste."]
        self.assertEqual(self.parser.word_tokenize(text), expected_tokens)

    def test_2_word_NP(self):
        tokens = ["de", "tok"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (D de) (N tok)))")

    def test_another_2_word_NP(self):
        tokens = ["un", "tok"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (D un) (N tok)))")

    def test_imperative_VO_VP(self):
        tokens = ["tok", "de", "panglo"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (VP (V tok) (NP (D de) (N panglo))))")

    def test_request_VP(self):
        tokens = ["ples", "tok", "de", "panglo"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (VP (V ples) (VP (V tok) (NP (D de) (N panglo)))))")

    def test_pronoun_SVO_clause(self):
        tokens = ["mi", "love", "yu"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (PRP mi)) (VP (V love) (NP (PRP yu))))")

    def test_pronoun_noun_SVO_clause(self):
        tokens = ["mi", "tok", "de", "panglo"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (PRP mi)) (VP (V tok) (NP (D de) (N panglo))))")

    def test_noun_SVO_clause(self):
        tokens = ["de", "jen", "wil", "tok", "de", "panglo"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (D de) (N jen)) (VP (V wil) (V tok) (NP (D de) (N panglo))))")

    def test_pronoun_SOV_clause(self):
        tokens = ["mi", "yu", "love"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (PRP mi)) (VP (NP (PRP yu)) (V love)))")

    def test_pronoun_noun_SOV_clause(self):
        tokens = ["mi", "un", "fem", "du", "love"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (PRP mi)) (VP (NP (D un) (N fem)) (V du) (V love)))")

    def test_noun_noun_SOV_clause(self):
        tokens = ["de", "nam", "un", "fem", "du", "love"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (D de) (N nam)) (VP (NP (D un) (N fem)) (V du) (V love)))")

    def test_possessive_pronoun_SVO_clause(self):
        tokens = ["mi","se", "frende", "du", "love", "yu", "se", "frende"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (PRP$ mi se) (N frende)) (VP (V du) (V love) (NP (PRP$ yu se) (N frende))))")

    def test_possessive_pronoun_SOV_clause(self):
        tokens = ["mi","se", "frende", "yu", "se", "frende", "du", "love"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (PRP$ mi se) (N frende)) (VP (NP (PRP$ yu se) (N frende)) (V du) (V love)))")

    def test_unmarked_object_NP_in_SVO(self):
        tokens = ["mi", "tok", "panglo"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (PRP mi)) (VP (V tok) (NP (N panglo))))")

    def test_verb_series(self):
        tokens = ["mi", "wan", "du", "tok", "de", "globe", "tok"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (PRP mi)) (VP (V wan) (VP (V du) (V tok) (NP (D de) (N globe) (N tok)))))")

    def test_long_unmarked_object_NP_in_SVO(self):
        tokens = ["mi", "tok", "nova", "globe", "tok"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (PRP mi)) (VP (V tok) (NP (N nova) (N globe) (N tok))))")

    def test_unmarked_object_NP_in_request_VO(self):
        tokens = ["ples", "tok", "panglo"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (VP (V ples) (VP (V tok) (NP (N panglo)))))")

    def test_long_unmarked_object_NP_in_request_VO(self):
        tokens = ["ples", "tok", "nova", "globe", "tok"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (VP (V ples) (VP (V tok) (NP (N nova) (N globe) (N tok)))))")


if __name__ == '__main__':
    unittest.main()