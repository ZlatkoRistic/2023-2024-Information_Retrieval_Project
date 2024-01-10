from transformers import GPT2LMHeadModel, GPT2Tokenizer
from pfc.OurFactChecker import OurFactChecker
import csv
from vsm import VSM


def fact_check(claim, evidence):
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    fact_checking_model = GPT2LMHeadModel.from_pretrained('fractalego/fact-checking')
    fact = OurFactChecker(fact_checking_model, tokenizer)
    test = fact.validate(evidence, claim)
    return test


def load_train_claims(vsm: VSM, max_doc_count: int = -1):
    """Load the list of claims extracted from the FEVER train.jsonl file,
    as if they were evidence documents.

    :param vsm: The VSM to load the claims into
    :param max_doc_count: The maximum amount of docs to load.
      This allows the loaded amount to be limited. Default value
      of -1 means unlimited
    
    """
    with open("train-claims.csv", "r") as ipf:
        reader = csv.reader(ipf, delimiter=',')
        next(reader)
        ctr: int = 0
        for _, claim in reader:
            if max_doc_count != -1 and ctr >= max_doc_count:
                return
            vsm.add_document(claim)  # ' '.join([claim] * 10))
            ctr += 1


if __name__ == '__main__':
    claim = "The planet Earth is flat."
    k: int = 3

    vsm = VSM()
    load_train_claims(vsm, max_doc_count=-1)
    top_k = vsm.get_top_k(claim, k)
    evidence_list = []

    print("Claim: " + claim)
    print(f"top-{k} relevant Evidence: ")
    for idx, res in enumerate(top_k):
        id, score = res
        evidence_doc = vsm.retrieve_document(id).contents
        evidence_list.append(evidence_doc)

        print("     {:4}ID={:12}score={:30}     ".format(str(idx+1) + ')', "" + str(id), "" + str(score)), evidence_doc)

    evidence = '\n\n'.join(evidence_list)
    result = fact_check(claim, evidence)
    k: int = 3

    vsm = VSM()
    load_train_claims(vsm, max_doc_count=-1)
    top_k = vsm.get_top_k(claim, k)
    evidence_list = []

    print("Claim: " + claim)
    print(f"top-{k} relevant Evidence: ")
    for idx, res in enumerate(top_k):
        id, score = res
        evidence_doc = vsm.retrieve_document(id).contents
        evidence_list.append(evidence_doc)

        print("     {:4}ID={:12}score={:30}     ".format(str(idx+1) + ')', "" + str(id), "" + str(score)), evidence_doc)

    evidence = '\n\n'.join(evidence_list)
    result = fact_check(claim, evidence)
    print("Result: " + str(result))

def verification():
    # db = FEVER
    pass
