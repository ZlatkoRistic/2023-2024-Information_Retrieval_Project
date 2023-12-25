from dataclasses import dataclass
from typing import List, Set, Dict, Tuple
from math import log, sqrt

from vsm.exceptions import UnknownDocument, UnknownTerm
from vsm.DocumentStore import DocumentStore, Document
from vsm.vsm_tokenizer import VSMTokenizer



@dataclass
class Posting:
    document_ID: int
    term_frequency: int

    def __str__(self) -> str:
        return f"(docID={self.document_ID},TF={self.term_frequency})"
    
    def __repr__(self) -> str:
        return self.__str__()

@dataclass
class InvertedTermData:
    document_frequency: int
    posting_list: List[Posting]

    def __str__(self) -> str:
        return f"<IDF={self.document_frequency}, {self.posting_list}>"

    def __repr__(self) -> str:
        return self.__str__()



class VSM(DocumentStore):
    """A Vector Space Model (VSM) that can be used to retrieve
    top-k documents for a specified query.
    
    The VSM provides an interface to register and persist documents
    for the VSM to make use of. It maintains a dynamic vocabulary
    the collection of stored documents, and builds and inverted
    document index to ensure reasonable calculation speed.
    
    Its implementation was based on the following sources:

    """
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

        # The tokenizer to pre-process & tokenize both queries and documents.
        self._tokenizer: VSMTokenizer = VSMTokenizer()

        # The collection of terms know by the VSM.
        # Can be used to check if a term is known in O(1).
        self._vocabulary: Set[str] = set()

        # Index statistics per document.
        # The following format is used:
        #   {
        #       document_ID : document_norm
        #   }
        # The document tf norm depends only on the terms in the document.
        # All other terms in the vocabulary contribute 0.0 to the norm.
        # So the norm does *not* need to be updated when the vocabulary is updated.
        #
        # If the document is updated, then this norm MUST be recalculated as well
        self._document_norms: Dict[int, float] = dict()

        # The inverted document index for every known term.
        self._inverted_lists: Dict[str, InvertedTermData] = dict()

    def get_top_k(self, query: str, k: int) -> List[Tuple[int, float]]:
        """Retrieve the top k documents for *query*.

        :param query: The query to do ranked retrieval for
        :param k: The amount of results to retrieve
        :return: The top k ranked documents for *query*, in
         the form of a list of `( document_ID, score )` pairs.
        """
        assert k >= 0, "Can not retrieve a negative number of top-k results."

        # Prevent wasted computation
        if k == 0:
            return []

        terms: List[str] = self._parse(query)

        # Compute accumulators
        # { document_ID : accumulator }
        accumulators: Dict[int, int] = dict()
        for term in terms:
            term_data: InvertedTermData = self._inverted_lists.get(term, None)
            if term_data is None: raise UnknownTerm(term)

            for posting in term_data.posting_list:
                document_ID: int = posting.document_ID
                tf_idf: float = self._tf_idf(term_data, posting)

                accumulator: float = accumulators.get(document_ID, 0.0)   # Default to 0.0 for docs that have no accumulator yet
                accumulators[document_ID] = accumulator + tf_idf

        # Generate scores for ALL related documents
        document_score_pairs: List[Tuple[int, float]] = []
        for document_ID, accumulator in accumulators.items():
            document_norm: float = self._document_norms.get(document_ID, None)
            if document_norm is None: raise UnknownDocument(document_ID)

            document_score_pairs.append((document_ID, accumulator / document_norm))

        # Produce top-k results
        document_score_pairs.sort(key=lambda pair: pair[1], reverse=True)
        return [(document_ID, score) for document_ID, score in document_score_pairs[:k]]

    def add_document(self, document: str) -> None:
        """Add a document to the VSM.

        Calling this method invalidates all existing query and
        document vectors if the document contains new terms that
        are not yet part of the VSM vocabulary.

        :param document: The document to add
        """
        # TODO Consider a "unknown term strategy" for queries that contain unknown terms?

        terms: List[str] = self._parse(document)
        unique_terms: Set[str] = set(terms)

        # Collect results
        self._vocabulary.update(unique_terms)
        new_document_ID: int = self.persist_document(Document(contents=document))
        new_document_tf_vector: List[float] = []

        for term in unique_terms:
            term_data: InvertedTermData = self._inverted_lists.get(term, None)

            if term_data is None:
                term_data = InvertedTermData(0, [])
                self._inverted_lists[term] = term_data

            # Generate new posting
            new_posting = Posting(
                document_ID    = new_document_ID,
                term_frequency = terms.count(term)
            )
            term_data.posting_list.append(new_posting)
            term_data.document_frequency += 1

            # Update running document norm
            new_document_tf_vector.append(new_posting.term_frequency)

        # Calculate document statistics
        self._document_norms[new_document_ID] = self._norm(new_document_tf_vector)

    def _tf(self, posting: Posting) -> float:
        """Calculate the logarithm weighted term frequency for some term
        in the document corresponding to the given posting.

        :param posting: A document posting of the term for which to determine the tf
        :return: The logarithm weighted tf of the term
        """
        assert posting is not None, "Can not determine TF for None-type posting"

        term_frequency: int = posting.term_frequency 
        
        if term_frequency == 0:
            return 0
        
        return 1 + log(term_frequency, 10)

    def _idf(self, term_data: InvertedTermData) -> float:
        """Calculate the inverse document frequency of the *term_data* in the
        collection of documents.

        :param term_data: The term for which to determine the idf
        :return: The idf of the term
        """

        assert term_data is not None, "Can not determine IDF for None-type term"

        document_count: int = self.document_count
        document_frequency: int = term_data.document_frequency
        # clamp document frequency, because division by zero = ERROR
        document_frequency = max(1, document_frequency)
        # clamp document count, because log(0) = ERROR
        document_count = max(1, document_count)
        return log(document_count / document_frequency, 10)

    def _tf_idf(self, term_data: InvertedTermData, posting: Posting) -> float:
        """Calculate the term frequency, inverse document frequency (tf-idf) weight
        of some term, given one of its document postings, in the collection of documents.

        :param term_data: The term data for which to determine the tf-idf
        :param posting: The document posting for which to determine the tf-idf
        :return: The tf-idf weight of the term
        """
        return self._tf(posting) * self._idf(term_data)

    def _norm(self, vector: List[float]):
        """Calculate the L2 (Euclidean) norm of the *vector*.

        :param vector: The vector to consider
        :return: The L2 norm of the vector
        """
        squared_vector: List[float] = [pow(x, 2) for x in vector]
        return sqrt(sum(squared_vector))

    def _parse(self, text: str) -> List[str]:
        """Parse input text and extract the sequential token sequence.
        
        :param text: The text to parse for tokens
        :return: The sequential token sequence
        """
        return self._tokenizer.tokenize(text)

