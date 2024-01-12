import csv
from src.vsm.vsm import VSM
from utils import verification, precision, pre_processing

def fact_check(claim, evidence):
    """
    :param claim: The claim to be fact checked
    :param evidence: The evidence to be fact checked against
    :return: Boolean value indicating whether the claim is true or false

    This is more used for testing purposes, as the fact we do not have to instantiate the model every time we want to fact check
    """
    from transformers import GPT2LMHeadModel, GPT2Tokenizer
    from src.pfc.OurFactChecker import OurFactChecker

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
    with open("train-claims.csv", "r", encoding="utf8") as ipf:
        reader = csv.reader(ipf, delimiter=',')
        next(reader)
        ctr: int = 0
        for _, claim in reader:
            if max_doc_count != -1 and ctr >= max_doc_count:
                return
            vsm.add_document(claim)  # ' '.join([claim] * 10))
            ctr += 1





if __name__ == '__main__':
    # claim = "The planet Earth is flat."
    # evidence = "The Earth is round."
    # k: int = 3
    #
    # vsm = VSM()
    # load_train_claims(vsm, max_doc_count=-1)
    # top_k = vsm.get_top_k(claim, k)
    # evidence_list = []
    #
    # print("Claim: " + claim)
    # print(f"top-{k} relevant Evidence: ")
    # for idx, res in enumerate(top_k):
    #     id, score = res
    #     evidence_doc = vsm.retrieve_document(id).contents
    #     evidence_list.append(evidence_doc)
    #
    #     print("     {:4}ID={:12}score={:30}     ".format(str(idx+1) + ')', "" + str(id), "" + str(score)), evidence_doc)
    #
    # evidence = '\n\n'.join(evidence_list)
    # result = fact_check(claim, evidence)
    # k: int = 3
    #
    # vsm = VSM()
    # load_train_claims(vsm, max_doc_count=-1)
    # top_k = vsm.get_top_k(claim, k)
    # evidence_list = []
    #
    # print("Claim: " + claim)
    # print(f"top-{k} relevant Evidence: ")
    # for idx, res in enumerate(top_k):
    #     id, score = res
    #     evidence_doc = vsm.retrieve_document(id).contents
    #     evidence_list.append(evidence_doc)
    #
    #     print("     {:4}ID={:12}score={:30}     ".format(str(idx+1) + ')', "" + str(id), "" + str(score)), evidence_doc)
    #
    # evidence = '\n\n'.join(evidence_list)
    # result = fact_check(claim, evidence)
    # print("Result: " + str(result))

    # TODO: MAKE SURE THAT THE SAMPLE SIZE IS NOT BIGGER THAN THE VALIDATION SET
    sample_size = 1000
    input_pre_processing_path = "./input/train.jsonl"
    output_pre_processing_path = "./input/pre_processed.jsonl"

    input_verification_path = "./input/pre_processed.jsonl"
    output_verification_path = "./output/results.json"

    pre_processing(input_path=input_pre_processing_path, output_path=output_pre_processing_path, sample_size=sample_size)
    # correct, incorrect, total = verification(input_path=input_verification_path, output_path=input_verification_path,
    #                                          sample_size=sample_size)
    # print("Correct: " + str(correct))
    # print("Incorrect: " + str(incorrect))
    # print("Total: " + str(total))
    # print("------------------")
    # print("Precision: " + str(precision(correct, total)))
