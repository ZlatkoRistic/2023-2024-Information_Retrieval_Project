import re
import nltk
import inflect

from typing import Set, List, Dict
from unidecode import unidecode

from src.vsm.contractions import CONTRACTION_MAP



class VSMTokenizer:
    """A pre-processor class to normalize text for use in a VSM.
    This pre-processor performs the following steps, not necessarily in this order:
    - replace accented characters   (êË => eE)
    - convert text to lower case    (eE => ee)
    - convert numbers to their word form (12 => twelve)
    - expand contractions   (i'd => i would)
    - remove special characters (any char not in [a-zA-Z0-9\s] where [0-9] is optional)
    - stemming              (optional, eat => eat, eating => eat, eaten => eat)
    - remove stopwords      (remove {i, you, and, the, ...})
    """
    def __init__(self) -> None:
        # Text processors
        self._tokenizer_method = nltk.tokenize.word_tokenize                # ToktokTokenizer is slower than str.split(), but better results? But ToktokTokenizer only considers final punctuation symbol, so use default ntlk word tokenizer instead
        self._stemmer: nltk.LancasterStemmer = nltk.LancasterStemmer()      # PorterStemmer is faster than the LancasterStemmer, but better results?
        self._inflect_engine: inflect.engine = inflect.engine()

        # Reference data
        self._stopword_list: Set[str] = self._load_stopwords()
        self._contraction_mapping: Dict[str, str] = CONTRACTION_MAP

        # Regex patterns
        self._NUMBER_PATTERN: re.Pattern       = re.compile(r'[+-]?(\d+([.]\d*)?|[.]\d+)')    # Matches whole numbers and floats of the form 'x.', '.y', 'x.y'
        self._NORMAL_ALNUM_PATTERN: re.Pattern = re.compile(r'[^a-zA-z0-9\s]')
        self._NORMAL_ALPHA_PATTERN: re.Pattern = re.compile(r'[^a-zA-z\s]')

    def tokenize(self, text: str, do_stemming: bool = True) -> List[str]:
        # String-based pre-processing
        text = self._remove_accents(text, strict=True)
        text = text.lower()     # Change case should only be done if the following steps will not add wrong-case characters
        text = self._numbers_to_words(text)

        # Token-based pre-processing
        tokens: List[str] = self._tokenizer_method(text) # text.split()
        tokens = self._expand_contractions(tokens)      # regex-based contraction expansion is slow?
        tokens = self._remove_special_characters(tokens, replace_char=' ', remove_digits=False)
        if do_stemming: tokens = self._stem(tokens)
        tokens = self._remove_stopwords(tokens, is_lower_case=True)

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

    def _expand_contractions(self, tokens: List[str]) -> List[str]:
        """Expand all contractions in the *tokens* using the VSMTokenizer's internal contraction map.
        
        This method was obtained from the following article and subsequently adapted:
            https://www.kdnuggets.com/2018/08/practitioners-guide-processing-understanding-text-2.html

        :param tokens: The tokens list containing contractions, to expand
        :return: The *tokens* where all contractions have been expanded
        """
        return [
            self._contraction_mapping.get(token, token)
            for token in tokens
        ]

    def _remove_special_characters(self, tokens: List[str], replace_char: str = '', remove_digits: bool = False) -> List[str]:
        """Remove all non-alpha-numeric characters from the *tokens*.
        
        This method was obtained from the following article and subsequently adapted:
            https://www.kdnuggets.com/2018/08/practitioners-guide-processing-understanding-text-2.html

        :param tokens: The set of tokens to remove special characters from
        :param replace_char: The character to replace every special character by.
         Defaults to removing the character.
        :param remove_digits: Whether to also remove digits
        :return: The *tokens* where all special characters have been removed
        """
        pattern = self._NORMAL_ALNUM_PATTERN if not remove_digits else self._NORMAL_ALPHA_PATTERN
        return pattern.sub(replace_char, ' '.join(tokens)).split()

    def _numbers_to_words(self, text: str) -> str:
        """Replace all occurrences of numbers by their full, word-based counterparts.
        This includes whole numbers and real point numbers, with an optional '+' or '-' prefix.

        Comma's, 'and' words and hyphons ('-' symbols) to connect the
        number words together are purposely excluded from the output,
        so that only the number words themselves remain. This prevents
        adding additional special characters and stop-words to the output.

        e.g.

            >>> vsm = VSMTokenizer()
        
            >>> vsm._numbers_to_words("1123")
            "one thousand one hundred twenty three"

            >>> vsm._numbers_to_words("-1 2")
            "minus one two"

            >>> vsm._numbers_to_words("PI UP TO FOUR DIGITS IS 3.1415")
            "PI UP TO FOUR DIGITS IS three point one four one five"

            >>> vsm._numbers_to_words("-1.4&+2")
            "minus one point four&plus two"

        :param text: The text in which to replace all numbers by words
        :return: The modified text
        """
        def transform_match(number: re.Match) -> str:
            """Map each number match to its word form."""
            number_text: str = number.group(0)
            return self._inflect_engine.number_to_words(number_text, andword='').\
                replace(',', '').\
                replace('-', ' ')

        expanded_text: str = self._NUMBER_PATTERN.sub(transform_match, text)
        return expanded_text


    def _stem(self, tokens: List[str]) -> List[str]:
        """Apply stemming to the *tokens*.
        
        This method was obtained from the following article and subsequently adapted:
            https://www.kdnuggets.com/2018/08/practitioners-guide-processing-understanding-text-2.html

        :param tokens: The text to stem, as a list of tokens
        :return: The stemmed text, as a pruned version of the input *tokens*
        """
        return [self._stemmer.stem(word) for word in tokens]

    def _remove_stopwords(self, tokens: List[str], is_lower_case: bool = False) -> List[str]:
        """Strip the *tokens* list of any instances of a stopword.
        
        This method was obtained from the following article and subsequently adapted:
            https://www.kdnuggets.com/2018/08/practitioners-guide-processing-understanding-text-2.html

        :param tokens: The text, as a list of *tokens*, to filter of stopwords
        :param is_lower_case: Whether the *tokens* are all already entirely in lower case
        :return: The *tokens* stripped (pruned) of (all) stopwords
        """
        filtered_tokens: List[str]
        if is_lower_case:
            filtered_tokens = [token for token in tokens if token not in self._stopword_list]
        else:
            filtered_tokens = [token for token in tokens if token.lower() not in self._stopword_list]

        return filtered_tokens

    def _load_stopwords(self) -> Set[str]:
        """Load the nltk english stopwords list.

        :raise LookupError: If the stopword list could not be located nor downloaded
        """
        try:
            return set(nltk.corpus.stopwords.words("english"))
        except LookupError:
            nltk.download("stopwords")
            return set(nltk.corpus.stopwords.words("english"))
