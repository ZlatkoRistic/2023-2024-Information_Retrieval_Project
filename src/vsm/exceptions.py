class UnknownTerm(Exception):
    def __init__(self, term: str, *args: object) -> None:
        super().__init__(*args)
        self.term = term

    def __str__(self) -> str:
        return f"'{self.term}'"

class UnknownDocument(Exception):
    def __init__(self, document_ID: int, *args: object) -> None:
        super().__init__(*args)
        self.document_ID = document_ID

    def __str__(self) -> str:
        return f"document ID = {self.document_ID}"

class DuplicateDocument(Exception):
    def __init__(self, document_ID: int, *args: object) -> None:
        super().__init__(*args)
        self.document_ID = document_ID

    def __str__(self) -> str:
        return f"document ID = {self.document_ID}"
