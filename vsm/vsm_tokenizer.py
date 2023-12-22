import re
import nltk
import inflect

from typing import Set, List, Dict, Union
from unidecode import unidecode
from contractions import CONTRACTION_MAP



class VSMTokenizer:
    def __init__(self) -> None:
        self._stemmer = nltk.porter.PorterStemmer()
        self._stopword_list: Set[str] = set()
        self._load_stopwords()
        self._tokenizer = nltk.tokenize.toktok.ToktokTokenizer()
        self._inflect_engine: inflect.engine = inflect.engine()
        self._contraction_mapping: Dict[str, str] = CONTRACTION_MAP

        # Regex patterns
        self._CONTRACTION_PATTERN = re.compile('({})'.format('|'.join(self._contraction_mapping.keys())),
                                               flags=re.IGNORECASE|re.DOTALL)

    def tokenize(self, text: str) -> List[str]:
        # String-based pre-processing
        text = self._remove_accents(text, strict=True)
        text = self._expand_contractions(text)
        # TODO "twenty-three" becomes "twentythree"
        #   ==> Replace special characters by whitespace instead?
        #   ==> Won't split() take care of the whitespace?
        text = self._remove_special_characters(text, replace_char='', remove_digits=False)
        text = text.lower()     # Change case should only be done if the following steps will not add wrong-case characters

        # Token-based pre-processing
        tokens: List[str] = self._tokenizer.tokenize(text)
        tokens = [token.strip() for token in tokens]    # Strip whitespace
        tokens = self._numbers_to_words(tokens)
        tokens = self._remove_stopwords(tokens)
        tokens = self._stem(tokens)

        return tokens

    def _remove_accents(self, text: str, strict: bool = True) -> str:
        """Remove accents from the *text* via transliteration --
        replace the accented characters to their closes non-
        accented ASCII counterpart.

        :raise UnidecodeError: The transliteration failed on some character
        :param text: The text to remove accents from
        :param strict: Whether to raise an exception transliteration fails
         on some character
        :return: The transliterated *text*
        """
        return unidecode(text, errors="strict" if strict else "ignore")

    def _expand_contractions(self, text: str):
        """Expand all contractions in the *text* using the VSMTokenizer's internal contraction map.
        
        This entire method was obtained from the following article:
            https://www.kdnuggets.com/2018/08/practitioners-guide-processing-understanding-text-2.html

        :param text: The text containing contractions, to expand
        :return: The *text* where all contractions have been expanded
        """
        def expand_match(contraction):
            match = contraction.group(0)
            first_char = match[0]
            expanded_contraction = self._contraction_mapping.get(match)\
                                    if self._contraction_mapping.get(match)\
                                    else self._contraction_mapping.get(match.lower())                       
            expanded_contraction = first_char+expanded_contraction[1:]
            return expanded_contraction
            
        expanded_text: str = self._CONTRACTION_PATTERN.sub(expand_match, text)
        expanded_text = expanded_text.replace("'", "")
        return expanded_text

    def _remove_special_characters(self, text: str, replace_char: str = '', remove_digits: bool = False):
        """Remove all non-alpha-numeric characters from the *text*.
        
        This entire method was obtained from the following article:
            https://www.kdnuggets.com/2018/08/practitioners-guide-processing-understanding-text-2.html

        :param text: The text to remove special characters from
        :param replace_char: The character to replace any special character by.
         Defaults to removing the character.
        :param remove_digits: Whether to also remove digits
        :return: The *text* where all special characters have been removed
        """
        pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
        text = re.sub(pattern, replace_char, text)
        return text

    def _numbers_to_words(self, tokens: List[str]) -> List[str]:
        """Replace all occurrences of arabic numerals by their
        full, word-based counterparts.

        Comma's and 'and' words to connect the numbers-words
        together are purposely removed, so that only the number
        words themselves remain. This is to avoid adding additional
        special characters and stop-words to the token list.

        e.g.
            >>> self._numbers_to_words(["123", 4])
            ["one thousand one hundred twenty-three", "four"]

        :param tokens: The text in which to replace all numerals by words, as a list of tokens
        :return: The converted text, as a pruned version of the input *tokens*
        """
        return [
            transformed_token
            for token in tokens
                for transformed_token in\
                (
                    self._inflect_engine.number_to_words(token, andword='').\
                        replace(',', '').\
                        replace('-', ' ').\
                        split()
                    if self._is_number(token) else [token]
                )
        ]

    def _stem(self, tokens: List[str]) -> List[str]:
        """Apply stemming to the *tokens*.
        
        This method was obtained from the following article and subsequently adapted:
            https://www.kdnuggets.com/2018/08/practitioners-guide-processing-understanding-text-2.html

        :param tokens: The text to stem, as a list of tokens
        :return: The stemmed text, as a pruned version of the input *tokens*
        """
        return [self._stemmer.stem(word) for word in tokens]

    def _remove_stopwords(self, tokens: List[str], is_lower_case: bool = False):
        """Strip the text of any instances of a stopword.
        
        This method was obtained from the following article and subsequently adapted:
            https://www.kdnuggets.com/2018/08/practitioners-guide-processing-understanding-text-2.html

        :param tokens: The text, as a list of *tokens*, to strip of stopwords
        :param is_lower_case: Whether the *tokens* are all already entirely in lower case
        :return: The *tokens* stripped (pruned) of (all) stopwords
        """
        filtered_tokens: List[str]
        if is_lower_case:
            filtered_tokens = [token for token in tokens if token not in self._stopword_list]
        else:
            filtered_tokens = [token for token in tokens if token.lower() not in self._stopword_list]

        return filtered_tokens

    def _load_stopwords(self) -> None:
        """Load the nltk english stopwords list.

        :raise LookupError: If the stopword list could not be located nor downloaded
        """
        try:
            self._stopword_list = set(nltk.corpus.stopwords.words("english"))
        except LookupError:
            nltk.download("stopwords")
            self._stopword_list = set(nltk.corpus.stopwords.words("english"))

    def _is_number(self, text: str):
        """Check whether the given *text* is a pure number string.
        This can be either a whole number, or a float.

        :param text: The string for which to check if it is number as a string
        :return: True if *text* contains only a number, else False
        """
        try:
            if text.isnumeric():
                return True
            float(text)
            return True
        except ValueError:
            return False


tokenizer: VSMTokenizer = VSMTokenizer()
text: str = """
Ëa&A 123
y'all can't expand contractions I'd think
Sómě Áccěntěd těxt
Tony hawk did 5 epic 360 backflips while eating -14214.5 icereams for $ 1.3
five ten five-ten hundred
"""
#print(tokenizer.tokenize(text))

print("\n"*2, "===========")

strings = [
    "Ëa&A 123",
    "y'all can't expand contractions I'd think",
    "Sómě Áccěntěd těxt",
    "Tony hawk did 5 epic 360 backflips while eating -14214.5 icereams for $ 1.3",
    "five ten five-ten hundred",
]
for s in strings:
    print(tokenizer.tokenize(s))

print(tokenizer._tokenizer.tokenize("3&abba"))
