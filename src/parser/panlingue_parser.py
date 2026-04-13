"""Parser for Panlingue, a constructed globally sourced international auxiliary language with word-class marking.

It parses input sentences in Panlingue to identify parts of speech and phrase structure,
aiming to determine the word order (SVO, SOV, etc.) of the input text.
It can output the parsed structure in NLTK tree format that is suitable for visualization with tools like svgling.

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

class panlingue_parser:
    cls_determiners = ['un', 'du', 'tri', 'car', 'ye', 'vo', 'la', 'si']
    cls_TAM_markers = ['sta', 'ha', 'fu']
    cls_personal_pronouns = ['mi', 'tu', 'ho', 'mimen', 'tumen', 'homen']

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
        Identify Panlingue words by ending and return corresponding word class.
        
        Panlingue word class markers:
        - Verbs end in -Vr or -Vs → V
        - Adjectives and adverbs end in -ik or -al → A
        - Nouns end in any other way (none of the above) → N
        """
        if not word:
            return ""
        
        word_lower = word.lower().translate(str.maketrans('', '', string.punctuation))
        
        if word_lower in self.cls_personal_pronouns:
            return "PRP"

        syllable_count = self.count_syllables(word_lower)
        # Verb: Head-initial verb (VO) ends in -Vr
        if syllable_count > 1 and word_lower.endswith('r') and word_lower[-2] in 'aeiou':
            return "V"
        # Verb: Head-final verb (OV) ends in -Vs
        if syllable_count > 1 and word_lower.endswith('s') and word_lower[-2] in 'aeiou':
            return "V"
            
        # Adjective: ends in -ik or -al
        if syllable_count > 1 and (word_lower.endswith('ik') or word_lower.endswith('al')):
            return "A"
        
        # Default: noun
        return 'N'

    def tag_word_classes(self, tokens):
        tagged_tokens = []
        for token in tokens:
            word_class = self.identify_word_class(token)
            tagged_tokens.append((word_class, token))
        return tagged_tokens
    
    def construct_phrases(self, tagged_tokens):
        current_phrase = None
        for word_class, word in tagged_tokens:
            if word_class == "PRP":
                if current_phrase is not None:
                    self.phrases.append(current_phrase)
                # Pronoun is a self-contained noun phrase
                current_phrase = Phrase("NP")
                current_phrase.constituent_type = "Subject"
                current_phrase.pos_word_pairs.append((word_class, word))
            elif word_class == "V":
                if current_phrase is not None:
                    self.phrases.append(current_phrase)
                # Start a new verb phrase
                current_phrase = Phrase("VP")
                current_phrase.constituent_type = "Verb"
                current_phrase.pos_word_pairs.append((word_class, word))
            elif word_class in ["A", "N"]:
                if current_phrase is not None and current_phrase.phrase_type == "VP":
                    self.phrases.append(current_phrase)
                    current_phrase = None
                if current_phrase is None:
                    # If we haven't started a phrase yet, start a noun phrase
                    current_phrase = Phrase("NP")
                # Add adjectives and nouns to the current phrase
                current_phrase.pos_word_pairs.append((word_class, word))
            else:
                # For any other word class, we can decide how to handle it (e.g., ignore or create a new phrase)
                pass

        if current_phrase is not None:
            self.phrases.append(current_phrase)

    def determine_constituent_order(self):
        head_initial = True
        for phrase in self.phrases:
            if phrase.phrase_type == 'NP':
                self.word_order += 'N'
            elif phrase.phrase_type == 'VP':
                self.word_order += 'V'
                if phrase.pos_word_pairs[0][1].endswith('s'):
                    head_initial = False
            else:
                self.word_order += 'X' # Unrecognized phrase type for word order determination

        if re.match('NVV*N', self.word_order):
            return 'SVO' if head_initial else 'OVS' #Transitive clause
        elif re.match('NNVV*', self.word_order):
            return 'OSV' if head_initial else 'SOV' #Transitive clause
        elif re.match('VV*NN', self.word_order):
            return 'VOS' if head_initial else 'VSO' #Transitive clause
        elif re.match('VV*N', self.word_order):
            return 'VO' if head_initial else 'OV' #Intransitive or imperative clause
        elif re.match('NVV*', self.word_order):
            return 'OV' if head_initial else 'OV' #Intransitive or imperative clause
        else:
            return None #Unrecognized word order


    def build_syntax_tree(self):
        constituent_order = self.determine_constituent_order()
        print(f"Determined constituent order: {constituent_order}")
        sentence = '(S'

        if constituent_order in ['SOV', 'OVS', 'VSO']:
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
                if phrase.phrase_type == 'VP':
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
        """Parse the input tokens in Panlingue into a syntax tree in NLTK format."""
        tagged_tokens = self.tag_word_classes(tokens)
        self.construct_phrases(tagged_tokens)
        print(tagged_tokens)
        return self.build_syntax_tree()
