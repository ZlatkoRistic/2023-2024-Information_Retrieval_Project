from transformers import GPT2LMHeadModel, GPT2Tokenizer
from fact_checking import FactChecker

def fact_check(claim, evidence):
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    fact_checking_model = GPT2LMHeadModel.from_pretrained('fractalego/fact-checking')
    fact_checker = FactChecker(fact_checking_model, tokenizer)
    is_claim_true = fact_checker.validate(evidence, claim)
    return is_claim_true

# TODO: See if this is useful (Co-Pilot generated)
class Ranked_retrieval():
    def __init__(self):
        self.index = {}
        self.documents = {}
        self.document_frequency = {}
        self.total_documents = 0

    def add_document(self, document_name, document_text):
        self.documents[document_name] = document_text
        self.total_documents += 1
        for token in document_text.split():
            if token not in self.index.keys():
                self.index[token] = {document_name: 1}
            else:
                if document_name not in self.index[token].keys():
                    self.index[token][document_name] = 1
                else:
                    self.index[token][document_name] += 1

    def compute_document_frequency(self):
        for token in self.index.keys():
            self.document_frequency[token] = len(self.index[token])

    def compute_tf_idf(self, query):
        query_tokens = query.split()
        query_weights = {}
        for key in self.index.keys():
            if key in query_tokens:
                pass
                # query_weights[key] = query_tokens.count(key) * self.index[key][document_name]
            else:
                query_weights[key] = 0

        for token in query_weights.keys():
            query_weights[token] *= self.document_frequency[token] / self.total_documents

        return query_weights

    def get_relevant_documents(self, query):
        query_weights = self.compute_tf_idf(query)
        query_weights = sorted(query_weights.items(), key=lambda x: x[1], reverse=True)
        return query_weights


if __name__ == '__main__':
    claim = "The Earth is flat"
    Ranked_retrieval = Ranked_retrieval()


    relevant_doc = Ranked_retrieval.get_relevant_documents(claim)
    evidence = relevant_doc
    result = fact_check(claim, evidence)
    print("Evidence: " + evidence)
    print("Claim: " + claim)
    print("Result: " + str(result))
