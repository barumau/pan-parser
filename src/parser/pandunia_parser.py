"""Parser for Pandunia, a constructed globally sourced international auxiliary language.

It parses input sentences in Pandunia to identify parts of speech and phrase structure,
aiming to determine the word order (SVO, SOV, etc.) of the input text.
It can output the parsed structure in NLTK tree format that is suitable for visualization with tools like svgling.

The syntax of Pandunia is structured by word order and natural word classes.
Words that describe actions and states are verbs, words that describe contrete and abstract things are nouns,
and words that describe qualities are modifiers (adjectives or adverbs).
The word order is determined by the position of the verb, as there are no clear function words marking phrases.
The first verb in the sentence is likely to be the main verb, while any auxiliary verbs are likely to be before it.
The first noun phrase is likely to be the subject, while any noun phrases after the first verb are likely to be objects.

CC-BY 2026 Risto Kupsala (https://github.com/barumau)
"""
import string
import re

class Phrase:
    def __init__(self, phrase_type):
        self.phrase_type = phrase_type
        self.constituent_type = None
        self.pos_word_pairs = []

    def print_pos_word_pairs(self):
        result = ''
        for pair in self.pos_word_pairs:
            result += f" ({pair[0]} {pair[1]})"
        return result

class pandunia_parser:
    cls_determiners = ['un', 'du', 'tri', 'car', 'ye', 'vo', 'la', 'si']
    cls_TAM_markers = ['sta', 'ha', 'fu']
    cls_personal_pronouns = ['mi', 'tu', 'ho', 'mimen', 'tumen', 'homen']
    cls_copula_verbs = ['es', 'ekua']
    cls_verbs = ['es', 'ekua', 'sta', 'ha', 'fu', 'evolu', 'voli', 'lase', 'loge', 'vide', 'pote', 'ame', 'cing', 'loge']
    cls_adjectives = ['bon', 'dus', 'dai', 'lit']
    cls_head_final_possessive_marker = 'su'
    cls_head_initial_possessive_marker = 'da'

    def __init__(self):
        self.phrases = []
        self.word_order = ''

    def word_tokenize(self, text):
        # Simple tokenization based on whitespace.
        tokens = text.split()
        return tokens

    def count_syllables(self, lower_token):
        """
        Count the number of syllables in a token.

        Args:
            lower_token (str): The token in lowercase.

        Returns:
            int: The number of syllables in the token.
        """
        syllables = 0
        consonants = "bcdfghjklmnpqrstvwxyz"
        vowels = "aeiou"
        if lower_token[0] in vowels:
            syllables += 1

        if len(lower_token) > 1:
            for i in range(len(lower_token) - 1):
                if lower_token[i] in consonants and lower_token[i+1] in vowels:
                    syllables += 1
        return syllables

    def identify_word_class(self, word: str) -> str:
        """
        Identify Pandunia words by root or ending and return corresponding word class.
        
        Pandunia word class markers:
        - Verbs end in -ifa or -iza
        - Adjectives and adverbs end in -ik or -al → A
        - Nouns end in any other way (none of the above) → N
        """
        if not word:
            return ""
        
        word_lower = word.lower().translate(str.maketrans('', '', string.punctuation))
        
        if word_lower in self.cls_personal_pronouns:
            return "PRP"
        elif word_lower in self.cls_determiners:
            return "D"
        elif word_lower in self.cls_head_final_possessive_marker:
            return "su"
        elif word_lower in self.cls_head_initial_possessive_marker:
            return "da"
        elif word_lower in self.cls_verbs:
            return "V"
        elif word_lower in self.cls_adjectives:
            return "A"

        syllable_count = self.count_syllables(word_lower)
        if syllable_count > 1:
            if word_lower.endswith('ifa') or word_lower.endswith('iza'):
                return "V"
            elif (word_lower.endswith('ik') or word_lower.endswith('al')):
                return "A"
        
        # Default: noun
        return 'N'

    def tag_word_classes(self, tokens):
        tagged_tokens = []
        for token in tokens:
            word_class = self.identify_word_class(token)
            tagged_tokens.append((word_class, token))
        return tagged_tokens
    
    def close_current_phrase(self, current_phrase):
        if current_phrase is not None:
            self.phrases.append(current_phrase)
        return None

    def start_new_NP(self, constituent_type=None):
        phrase = Phrase("NP")
        phrase.constituent_type = constituent_type
        return phrase

    def start_new_VP(self, phrase_type="VP"):
        phrase = Phrase(phrase_type)
        phrase.constituent_type = "Verb"
        return phrase

    def process_pronoun(self, current_phrase, word):
        current_phrase = self.close_current_phrase(current_phrase)
        current_phrase = self.start_new_NP("Subject")
        current_phrase.pos_word_pairs.append(("PRP", word))
        return current_phrase

    def process_verb(self, current_phrase, word):
        if current_phrase is not None:
            if current_phrase.phrase_type == "VP" and current_phrase.pos_word_pairs[-1][1] in self.cls_TAM_markers:
                current_phrase.pos_word_pairs.append(("V", word))
                return current_phrase
            elif current_phrase.phrase_type == "NP" and current_phrase.pos_word_pairs[-1][1] in self.cls_determiners:
                current_phrase.pos_word_pairs.append(("N", word))
                return current_phrase
            else:
                current_phrase = self.close_current_phrase(current_phrase)
        phrase_type = "CopP" if word in self.cls_copula_verbs else "VP"
        current_phrase = self.start_new_VP(phrase_type)
        current_phrase.pos_word_pairs.append(("V", word))
        return current_phrase

    def process_possessive_marker(self, current_phrase, word):
        if current_phrase is not None and len(current_phrase.pos_word_pairs) > 0:
            old_token = current_phrase.pos_word_pairs[-1][1]
            current_phrase.pos_word_pairs.pop()
            current_phrase.pos_word_pairs.append(("D", old_token + " " + word))
        else:
            print(f"Warning: Found head-final possessive marker '{word}' without a preceding noun.")
        return current_phrase

    def process_determiner(self, current_phrase, word):
        if current_phrase is not None:
            if current_phrase.phrase_type == "VP":
                current_phrase = self.close_current_phrase(current_phrase)
            elif current_phrase.phrase_type == "NP" and current_phrase.pos_word_pairs and current_phrase.pos_word_pairs[-1][0] != "D":
                self.phrases.append(current_phrase)
                current_phrase = self.start_new_NP("Subject")
        if current_phrase is None:
            current_phrase = self.start_new_NP()
        current_phrase.pos_word_pairs.append(("D", word))
        return current_phrase

    def process_adj_noun(self, current_phrase, word_class, word):
        if current_phrase is not None and current_phrase.phrase_type in ["VP", "CopP"]:
            current_phrase = self.close_current_phrase(current_phrase)
        if current_phrase is not None and current_phrase.phrase_type == "NP":
            if current_phrase.pos_word_pairs and current_phrase.pos_word_pairs[-1][0] == "PRP":
                current_phrase = self.close_current_phrase(current_phrase)
        if current_phrase is None:
            current_phrase = self.start_new_NP()
        current_phrase.pos_word_pairs.append((word_class, word))
        return current_phrase

    def construct_phrases(self, tagged_tokens):
        current_phrase = None
        for word_class, word in tagged_tokens:
            if word_class == "PRP":
                current_phrase = self.process_pronoun(current_phrase, word)
            elif word_class == "V":
                current_phrase = self.process_verb(current_phrase, word)
            elif word_class == "su":
                current_phrase = self.process_possessive_marker(current_phrase, word)
            elif word_class == "D":
                current_phrase = self.process_determiner(current_phrase, word)
            elif word_class in ["A", "N"]:
                current_phrase = self.process_adj_noun(current_phrase, word_class, word)
            else:
                pass

        if current_phrase is not None:
            self.phrases.append(current_phrase)

    def determine_constituent_order(self):
        for phrase in self.phrases:
            if phrase.phrase_type == 'NP':
                self.word_order += 'N'
            elif phrase.phrase_type in ["VP", "CopP"]:
                self.word_order += 'V'
            else:
                self.word_order += 'X' # Unrecognized phrase type for word order determination

        if re.match('NVV*N', self.word_order):
            return 'SVO' #Transitive clause
        elif re.match('NNVV*', self.word_order):
            return 'SOV' #Transitive clause
        elif re.match('VV*NN', self.word_order):
            return 'VOO' #Transitive clause with indirect object
        elif re.match('VV*N', self.word_order):
            return 'VO' #Imperative clause
        elif re.match('NVV*', self.word_order):
            return 'SV' #Intransitive clause
        elif self.word_order == 'NN':
            return 'ZeroCopula' #Noun phrase only
        else:
            return None #Unrecognized word order


    def build_syntax_tree(self):
        constituent_order = self.determine_constituent_order()
        print(f"Determined constituent order: {constituent_order}")
        sentence = '(S'

        if constituent_order is 'ZeroCopula' and len(self.phrases) == 2:
            sentence += ' (NP' + self.phrases[0].print_pos_word_pairs() + ') (CopP (V ∅) (NP' + self.phrases[1].print_pos_word_pairs() + ')))'
            return sentence

        if constituent_order in ['SOV']:
            beginning_of_VP = constituent_order.find('V') - 1
            for i in range(len(self.phrases)):
                phrase = self.phrases[i]

                if i == beginning_of_VP:
                    sentence += ' (VP'

                if phrase.phrase_type == 'VP':
                    sentence += phrase.print_pos_word_pairs()
                else:
                    sentence += ' (' + phrase.phrase_type + phrase.print_pos_word_pairs() + ')'

                if i == beginning_of_VP + 1:
                    sentence += ')'
        else:
            VPs_to_close = 0
            for i in range(len(self.phrases)):
                phrase = self.phrases[i]
                sentence += ' (' + phrase.phrase_type + phrase.print_pos_word_pairs()
                if phrase.phrase_type in ["VP", "CopP"]:
                    VPs_to_close += 1
                else:
                    sentence += ')'
                    for _ in range(VPs_to_close):
                        sentence += ')'
                    VPs_to_close = 0

            # Close any remaining open VP parentheses for OSV order
            for _ in range(VPs_to_close):
                sentence += ')'

        sentence += ')'
        return sentence

    def parse_into_syntax_tree(self, tokens):
        """Parse the input tokens in Pandunia into a syntax tree in NLTK format."""
        tagged_tokens = self.tag_word_classes(tokens)
        self.construct_phrases(tagged_tokens)
        print(tagged_tokens)
        return self.build_syntax_tree()
