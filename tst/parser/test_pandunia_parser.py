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
        text = "sal, dunia! ye es teste."
        expected_tokens = ["sal,", "dunia!", "ye", "es", "teste."]
        self.assertEqual(self.parser.word_tokenize(text), expected_tokens)

    def test_determiner_NP(self):
        tokens = ["la", "loge"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (D la) (N loge)))")

    def test_that_determiner_overrides_V_in_NP(self):
        tokens = ["un", "loge"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (D un) (N loge)))")

    def test_imperative_V(self):
        tokens = ["loge"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (VP (V loge)))")

    def test_imperative_VO_VP(self):
        tokens = ["loge", "pandunia"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (VP (V loge) (NP (N pandunia))))")

    def test_imperative_VO_VP_with_determiner_NP_object(self):
        tokens = ["loge", "la", "dunia", "basa"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (VP (V loge) (NP (D la) (N dunia) (N basa))))")

    def test_request_VP(self):
        tokens = ["cing", "loge", "la", "pandunia"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (VP (V cing) (VP (V loge) (NP (D la) (N pandunia)))))")

    def test_pronoun_SVO_clause(self):
        tokens = ["mi", "ame", "tu"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (PRP mi)) (VP (V ame) (NP (PRP tu))))")

    def test_pronoun_noun_SVO_clause(self):
        tokens = ["mi", "loge", "la", "pandunia"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (PRP mi)) (VP (V loge) (NP (D la) (N pandunia))))")

    def test_noun_SVO_clause(self):
        tokens = ["la", "jen", "fu", "loge", "la", "pandunia"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (D la) (N jen)) (VP (V fu) (V loge) (NP (D la) (N pandunia))))")

    def test_pronoun_SOV_clause(self):
        tokens = ["mi", "tu", "ame"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (PRP mi)) (VP (NP (PRP tu)) (V ame)))")

    def test_pronoun_noun_SOV_clause(self):
        tokens = ["mi", "un", "fem", "sta", "ame"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (PRP mi)) (VP (NP (D un) (N fem)) (V sta) (V ame)))")

    def test_noun_noun_SOV_clause(self):
        tokens = ["la", "nam", "un", "fem", "sta", "ame"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (D la) (N nam)) (VP (NP (D un) (N fem)) (V sta) (V ame)))")

    def test_possessive_pronoun_SVO_clause(self):
        tokens = ["mi","su", "doste", "sta", "ame", "tu", "su", "doste"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (D mi su) (N doste)) (VP (V sta) (V ame) (NP (D tu su) (N doste))))")

    def test_possessive_pronoun_SOV_clause(self):
        tokens = ["mi","su", "doste", "tu", "su", "doste", "sta", "ame"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (D mi su) (N doste)) (VP (NP (D tu su) (N doste)) (V sta) (V ame)))")

    def test_unmarked_object_in_SVO(self):
        tokens = ["mi", "loge", "pandunia"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (PRP mi)) (VP (V loge) (NP (N pandunia))))")

    def test_unmarked_object_NP_in_SVO(self):
        tokens = ["mi", "loge", "pandunia"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (PRP mi)) (VP (V loge) (NP (N pandunia))))")

    def test_long_unmarked_object_NP_in_SVO(self):
        tokens = ["mi", "loge", "nova", "dunia", "basa"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (NP (PRP mi)) (VP (V loge) (NP (N nova) (N dunia) (N basa))))")

    def test_unmarked_object_NP_in_request_VO(self):
        tokens = ["cing", "loge", "pandunia"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (VP (V cing) (VP (V loge) (NP (N pandunia)))))")

    def test_long_unmarked_object_NP_in_request_VO(self):
        tokens = ["cing", "loge", "nova", "dunia", "basa"]
        result = self.parser.parse_into_syntax_tree(tokens)
        self.assertEqual(result, "(S (VP (V cing) (VP (V loge) (NP (N nova) (N dunia) (N basa)))))")

    # TODO: Support the pivot construction, as in 'cing lase dunia loge' ('Please let the world talk').
    #def test_pivot_construction(self):
    #    tokens = ["cing", "lase", "dunia", "loge"]
    #    result = self.parser.parse_into_syntax_tree(tokens)
    #    self.assertEqual(result, "(S (VP (V cing) (VP (V lase) ((NP (N dunia)) (VP (V loge)))))")


if __name__ == '__main__':
    unittest.main()