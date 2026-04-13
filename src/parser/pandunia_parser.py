"""Parser for Pandunia, a constructed globally sourced international auxiliary language.

It parses input sentences in Pandunia to identify parts of speech and phrase structure,
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

class pandunia_parser:
    cls_determiners = ['un', 'du', 'tri', 'car', 'ye', 'vo', 'la', 'si']
    cls_TAM_markers = ['sta', 'ha', 'fu']
    cls_auxiliary_and_modal_verbs = ['sta', 'fu', 'ha', 'pote', 'voli', 'debe', 'sabe', 'cing', 'ples']
    cls_personal_pronouns = ['mi', 'tu', 'ho', 'mimen', 'tumen', 'homen']
    def __init__(self):
        self.subject_found = False
        self.phrases = []
        self.phrase_pattern = ''

    def word_tokenize(self, text):
        # Simple tokenization based on whitespace.
        tokens = text.split()
        return tokens

    def begins_DP(self, token):
        clean_token = token.lower().translate(str.maketrans('', '', string.punctuation))
        return clean_token in self.cls_determiners

    def begins_PRP(self, token):
        clean_token = token.lower().translate(str.maketrans('', '', string.punctuation))
        return clean_token in self.cls_personal_pronouns

    def begins_NP(self, token):
        return self.begins_DP(token) or self.begins_PRP(token)

    def begins_VP(self, token):
        clean_token = token.lower().translate(str.maketrans('', '', string.punctuation))
        return clean_token in self.cls_TAM_markers

    def begins_new_phrase(self, token):
        return self.begins_NP(token) or self.begins_VP(token)

    def tag_DP(self, tokens):
        """Tag a determiner phrase (DP) starting with a determiner.
        For example, "la doste" would be tagged as "(DP (D la) (N doste))".
        """
        noun_phrase = Phrase('NP')
        noun_phrase.pos_word_pairs.append(('D', tokens[0]))
        for i in range(1, len(tokens)):
            if self.begins_new_phrase(tokens[i]):
                break
            noun_phrase.pos_word_pairs.append(('N', tokens[i]))
        i += 1 if i+1 == len(tokens) else 0 # If we reached the end of the tokens, increment i to indicate that all tokens were consumed.
        self.phrases.append(noun_phrase)
        return i

    def tag_PRP(self, tokens):
        """Tag a personal pronoun (PRP) or a possessive pronoun phrase.
        For example, "mi" would be tagged as "(PRP mi)", while "mi su doste" would be tagged as "(NP (PRP$ mi su) (N doste))".
        """
        noun_phrase = Phrase('NP')
        if len(tokens) > 1:
            if tokens[1].lower() == 'su': # Possessive pronoun as a determiner, like "mi su doste" -> "my friend"
                noun_phrase.pos_word_pairs.append(('PRP$', tokens[0] + ' su'))
                for i in range(2, len(tokens)):
                    if self.begins_new_phrase(tokens[i]):
                        break
                    noun_phrase.pos_word_pairs.append(('N', tokens[i]))

                i += 1 if i+1 == len(tokens) else 0 # If we reached the end of the tokens, increment i to indicate that all tokens were consumed.
                self.phrases.append(noun_phrase)
                return i

        noun_phrase.pos_word_pairs.append(('PRP', tokens[0]))
        self.phrases.append(noun_phrase)
        return 1

    def tag_NP(self, tokens):
        """Tag a noun phrase (NP) starting with a determiner or a personal pronoun."""
        leap = 0
        subject_found_this_time = False

        if self.begins_DP(tokens[0]):
            leap = self.tag_DP(tokens)
            if self.subject_found == False:
                self.subject_found = True
                subject_found_this_time = True
        elif self.begins_PRP(tokens[0]):
            leap = self.tag_PRP(tokens)
            if self.subject_found == False:
                self.subject_found = True
                subject_found_this_time = True
        else:
            print(f"Warning: Unrecognized token '{tokens[0]}' in NP")

        if len(tokens) > leap:
            if subject_found_this_time:
                self.tag_VP(tokens[leap:])
            else:
                self.tag_VP(tokens[leap:])

    def tag_VP(self, tokens):
        """Tag a verb phrase (VP). VP is the first phrase in the clause or it starts with an auxiliary verb."""
        if len(tokens) == 0:
            return ''

        if self.begins_NP(tokens[0]):
            return  self.tag_NP(tokens)

        next = 1
        verb_phrase = Phrase('VP')
        verb_phrase.pos_word_pairs.append(('V', tokens[0]))
        if self.begins_VP(tokens[0]):
            # Insert TAM and verb as a pair.
            verb_phrase.pos_word_pairs.append(('V', tokens[1]))
            next = 2
        self.phrases.append(verb_phrase)

        if next < len(tokens):
            if self.begins_NP(tokens[next]):
                self.tag_NP(tokens[next:])
            else:
                self.tag_VP(tokens[next:])

    def determine_phrase_pattern(self):
        """Determine the phrase pattern of the sentence based on the identified phrases and their types.
           The function may also reclassify final VPs as NPs if they likely contain a noun due to
           lack of clear marking and the fact that there are not enough noun phrases in the sentence."""
        number_of_noun_phrases = sum(1 for phrase in self.phrases if phrase.phrase_type == 'NP')
        number_of_consecutive_verbs = 0
        number_of_auxiliary_verbs = 0
        object_noun_phrase = None

        for phrase in self.phrases:
            if phrase.phrase_type == 'NP':
                self.phrase_pattern += 'N'
            elif phrase.phrase_type == 'VP':
                number_of_consecutive_verbs += 1
                word = phrase.pos_word_pairs[0][1].lower()
                if word in self.cls_auxiliary_and_modal_verbs:
                    self.phrase_pattern += 'V'
                    number_of_auxiliary_verbs += 1
                elif number_of_consecutive_verbs - number_of_auxiliary_verbs == 1:
                    self.phrase_pattern += 'V' # First main verb in the VP
                elif number_of_noun_phrases >= 2:
                    self.phrase_pattern += 'V' # Exceptionally long series of verbs.
                else:
                    # Reclassify this VP as an NP, as it is likely an unmarked object NP.
                    self.phrase_pattern += 'N'
                    if object_noun_phrase is None:
                        object_noun_phrase = phrase
                        object_noun_phrase.phrase_type = 'NP'
                        object_noun_phrase.pos_word_pairs.pop(0)
                        object_noun_phrase.pos_word_pairs.insert(0, ('N', word)) # Insert the verb as a noun after the first noun in the phrase.
                    else:
                        # Insert other misclassified verbs as noun in the object NP.
                        object_noun_phrase.pos_word_pairs.append(('N', word))
                        phrase.phrase_type = 'Deleted VP'
            else:
                self.phrase_pattern += 'X' # Unrecognized phrase type for word order determination

        # Remove any phrases that have been reclassified from the list.
        self.phrases = [phrase for phrase in self.phrases if not phrase.phrase_type == 'Deleted VP']

    def determine_constituent_order(self):
        """Determine the order of constintuents (subject, verb and object) in the sentence based on the phrase pattern."""
        self.determine_phrase_pattern()

        if re.match('NVV*N', self.phrase_pattern):
            constituent_order = 'SVO' #Transitive SVO clause
        elif re.match('NNVV*', self.phrase_pattern):
            constituent_order = 'SOV' #Transitive SOV clause
        elif re.match('VV*N', self.phrase_pattern):
            constituent_order = 'VO' #Imperative clause with object
        elif re.match('NVV*', self.phrase_pattern):
            constituent_order = 'SV' #Intransitive clause
        elif re.match('VV*', self.phrase_pattern):
            constituent_order = 'V' #Imperative clause without object
        else:
            constituent_order = None #Unrecognized word order

        print(f"Determined constituent order {constituent_order} for phrase pattern {self.phrase_pattern}")
        return constituent_order

    def build_syntax_tree(self):
        """Build NLTK tree format string for the identified phrases and their types, based on the determined constituent order."""
        constituent_order = self.determine_constituent_order()
        syntax_tree = '(S'

        VPs_to_close = 0
        if constituent_order == 'SOV':
            beginning_of_VP = 1 # The VP begins between S and O.
            for i in range(len(self.phrases)):
                phrase = self.phrases[i]

                if i == beginning_of_VP:
                    syntax_tree += ' (VP'
                    VPs_to_close += 1

                if phrase.phrase_type == 'VP':
                    syntax_tree += phrase.print_pos_word_pairs()
                else:
                    syntax_tree += ' (' + phrase.phrase_type + phrase.print_pos_word_pairs() + ')'
        else:
            for i in range(len(self.phrases)):
                phrase = self.phrases[i]
                syntax_tree += ' (' + phrase.phrase_type + phrase.print_pos_word_pairs()
                if phrase.phrase_type == 'VP':
                    VPs_to_close += 1
                else:
                    syntax_tree += ')'

        for _ in range(VPs_to_close):
            syntax_tree += ')'
        syntax_tree += ')'
        return syntax_tree

    def parse_into_syntax_tree(self, tokens):
        """Parse the input tokens in Pandunia into a syntax tree in NLTK format."""
        if self.begins_NP(tokens[0]):
            self.tag_NP(tokens)
        else:
            self.tag_VP(tokens)
        print(tokens)
        return self.build_syntax_tree()
