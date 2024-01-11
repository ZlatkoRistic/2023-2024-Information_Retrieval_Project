import json
from datasets import load_dataset
from tqdm import tqdm

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


def verification():
    import json
    from datasets import load_dataset


    # filter out the evidence


    correct = 0
    incorrect = 0
    total = 0
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    fact_checking_model = GPT2LMHeadModel.from_pretrained('fractalego/fact-checking')
    fact = OurFactChecker(fact_checking_model, tokenizer)
    sample_size = 1000
    with open("pre_processed", "r") as f:
        line = f.readline()
        pbar = tqdm(total=sample_size)
        while line:
            json_obj = json.loads(line)
            label = json_obj["label"]
            evidence = json_obj["evidence"]
            claim = json_obj["claim"]
            result = fact.validate(evidence, claim)
            if result and label == "SUPPORTS":
                correct += 1
            elif result and label == "REFUTES":
                correct += 1
            else:
                incorrect += 1
            total += 1
            pbar.update(1)
    f.close()
    print("Correct: " + str(correct))
    print("Incorrect: " + str(incorrect))
    print("Total: " + str(total))
    return correct, incorrect, total


def pre_processing():
    ds = load_dataset('fever', 'wiki_pages')
    ds = ds['wikipedia_pages']
    ds = ds.remove_columns('lines')
    df = ds.to_pandas(500, batched=False)
    df.set_index('id', inplace=True)
    sample_size = 1000
    with open("pre_processed", 'w') as r:
        with open("train.jsonl", "r") as f:
            line = f.readline()
            counter = 0
            pbar = tqdm(total=sample_size)
            while line:
                json_obj = json.loads(line)
                label = json_obj["label"]
                if label == "NOT ENOUGH INFO":
                    line = f.readline()
                    continue
                evidence = ''
                for i in range(len(json_obj["evidence"][0])):
                    evidence_page = json_obj["evidence"][0][i][2]
                    temp = df.loc[df.index == evidence_page]
                    if temp.empty:
                        continue
                    evidence += df.loc[df.index == evidence_page].iloc[0]['text'] + ' '
                claim_txt = json_obj["claim"]
                if evidence == '':
                    line = f.readline()
                    continue
                dict = {"claim": claim_txt, "evidence": evidence, "label": label}
                json.dump(dict, r)
                r.write('\n')
                pbar.update(1)
                line = f.readline()
                counter += 1
                if counter == sample_size:
                    f.close()
                    r.close()
                    return dict
    f.close()
    r.close()
    return dict



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
    verification()
    # print(pre_processing())