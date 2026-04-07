"""Parser for Pandunia, a constructed globally international auxiliary language.

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
    cls_personal_pronouns = ['mi', 'tu', 'ho', 'mimen', 'tumen', 'homen']
    def __init__(self):
        self.subject_found = False
        self.phrases = []
        self.word_order = ''

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
        self.word_order += 'N'
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

        self.word_order += 'V'

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

    def determine_constituent_order(self):
        if re.match('NVV*N', self.word_order):
            return 'SVO' #Transitive SVO clause
        elif re.match('NNVV*', self.word_order):
            return 'SOV' #Transitive SOV clause
        elif re.match('VV*N', self.word_order):
            return 'VO' #Imperative clause
        elif re.match('NVV*', self.word_order):
            return 'OV' #Intranstive clause
        else:
            return None #Unrecognized word order

    def print_sentence_structure(self):
        constituent_order = self.determine_constituent_order()
        sentence = '(S'

        VPs_to_close = 0
        if constituent_order == 'SOV':
            beginning_of_VP = 1 # The VP begins between S and O.
            for i in range(len(self.phrases)):
                phrase = self.phrases[i]

                if i == beginning_of_VP:
                    sentence += ' (VP'
                    VPs_to_close += 1

                if phrase.phrase_type == 'VP':
                    sentence += phrase.print_pos_word_pairs()
                else:
                    sentence += ' (' + phrase.phrase_type + phrase.print_pos_word_pairs() + ')'
        else:
            for i in range(len(self.phrases)):
                phrase = self.phrases[i]
                sentence += ' (' + phrase.phrase_type + phrase.print_pos_word_pairs()
                if phrase.phrase_type == 'VP':
                    VPs_to_close += 1
                else:
                    sentence += ')'

        for _ in range(VPs_to_close):
            sentence += ')'
        sentence += ')'
        return sentence

    def tag_sentence(self, tokens):
        if self.begins_NP(tokens[0]):
            self.tag_NP(tokens)
        else:
            self.tag_VP(tokens)
        print(tokens)
        return self.print_sentence_structure()
