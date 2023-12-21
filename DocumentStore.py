from dataclasses import dataclass
from typing import Dict

from exceptions import UnknownDocument



@dataclass
class Document:
    contents: str



class DocumentStore:
    def __init__(self) -> None:
        # TODO Replace document_mapping by more appropriate structure?
        #   ==> Utilize document oriented DB?
        # The mapping of document ID to document.
        # This allows posting lists to refer to a document, and for the
        # document to be retrieved as a retrieval result.
        self.document_store: Dict[int, Document] = dict()

    @property
    def document_count(self) -> int:
        """The number of documents tracked by the document store."""
        return len(self.document_store)

    def persist_document(self, document: Document) -> int:
        """Persist the document to the document store as a new document.
        Even if this document was persisted before, this call will store
        it as a new entry.

        :param document: The document to persist in the document store
        :return: The unique ID assigned to the document
        """
        new_document_ID: int = len(self.document_store)
        self.document_store[new_document_ID] = document
        return new_document_ID

    def retrieve_document(self, document_ID: int) -> Document:
        """Retrieve the document corresponding to the given ID
        from the document store.

        :raise UnknownDocument: The given document ID is not in use
        :param document_ID: The ID corresponding to the retrieved document
        :return: The corresponding document
        """
        document: Document = self.document_store.get(document_ID)
        if document is None: raise UnknownDocument(document_ID)
        return document
