import csv
import cProfile
from pathlib import Path

from src.vsm.vsm import VSM


# TODO parse and import FEVER evidence as documents into VSM
# import json
# with open("train.jsonl", "r") as f:
#     line = f.readline()
#     while line:
#         json_obj = json.loads(line)
#         claim_txt = json_obj["claim"]
#         vsm.add_document(claim_txt)

#         line = f.readline()

def extract_train_claims():
    import json
    claims = set()
    with open("results/train.jsonl", "r") as f:
        line = f.readline()
        while line:
            json_obj = json.loads(line)
            claim_txt = json_obj["claim"]
            claims.add(claim_txt)

            line = f.readline()

    import csv
    with open("train-claims.csv", "a") as _:
        pass
    with open("train-claims.csv", "w") as of:
        writer = csv.writer(of)
        writer.writerow(("document_ID", "claim"))
        for idx, claim_text in enumerate(claims):
            writer.writerow((idx, claim_text))


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


def write_documents(vsm: VSM):
    with open("train-claims-pre-processed.csv", "w") as of:
        writer = csv.writer(of, delimiter=',')
        writer.writerow(["document_ID", "pre-processed claim"])
        for ID, document in vsm.document_store.items():
            writer.writerow([ID, document.contents])


def print_top_k(vsm: VSM, query: str, k: int):
    top_k = vsm.get_top_k(query, k)

    print("\n" * 3)
    print("    k = ", k)
    print("query = ", query)
    print("top-k = ", top_k)
    print()
    for idx, res in enumerate(top_k):
        id, score = res
        print(f"{idx + 1})\tID={id}\tscore={score}\t", vsm.retrieve_document(id).contents)


def top_k_minimal():
    vsm = VSM()
    documents = [
        "introduc informa retrieval",
        "data mining concept technique",
        "introduc data mining",
        "modern informa retrieval",
        "data base system concept",
        "data warehous system",
        "modern data informa system data warehous data base data mining informa retrieval",
    ]

    for doc in documents:
        vsm.add_document(doc)

    print(vsm._vocabulary)
    print(vsm._document_norms)
    print(vsm._inverted_lists)

    query: str = "introduc modern informa"
    k: int = 3
    print_top_k(vsm, query, k)


def top_k_fever_small():
    vsm = VSM()

    load_train_claims(vsm, max_doc_count=-1)  # 10000)#1000)

    query: str = "introduction modern information"
    k: int = 3
    print_top_k(vsm, query, k)

    write_documents(vsm)


def verification(input_path: str = "./input/pre_processed.jsonl", output_path: str ="./output/results.json", sample_size: int = 1000):
    import json
    from transformers import GPT2Tokenizer, GPT2LMHeadModel
    from tqdm import tqdm
    from src.pfc.OurFactChecker import OurFactChecker
    """

    :param input_path: The validation set to be used for verification
    :param output_path: The output file to write the results to
    :param sample_size: The number of samples to be used for testing (this is not really neccessary, but it is used to estimate the eval time)
    :return: tuple of ints representing the number of correct, incorrect, and total results
    """
    # Variables to keep track of the number of correct, incorrect, and total results
    correct = 0
    incorrect = 0
    total = 0
    # Load the model and tokenizer
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    fact_checking_model = GPT2LMHeadModel.from_pretrained('fractalego/fact-checking')
    # Instantiate the fact checker
    fact = OurFactChecker(fact_checking_model, tokenizer)
    # Sample size to be used for testing
    sample_size = 1000

    print(input_path)
    print(output_path)
    input_path = Path('.') / input_path
    output_path = Path('.') / output_path
    print(input_path)
    print(output_path)


    # Open the validation set
    with open(input_path, "r") as f:
        # Read the first line
        line = f.readline()
        pbar = tqdm(total=sample_size)
        while line:
            # Load the json object
            json_obj = json.loads(line)
            label = json_obj["label"]
            evidence = json_obj["evidence"]
            claim = json_obj["claim"]
            # Fact check the claim against the evidence
            result = fact.validate(evidence, claim)
            # Update the correct, incorrect, and total results depending on the result
            if result and label == "SUPPORTS":
                correct += 1
            elif result and label == "REFUTES":
                correct += 1
            else:
                incorrect += 1
            total += 1
            # Update the progress bar
            pbar.update(1)
            # Read the next line
            line = f.readline()
    f.close()
    # Print the results
    print("Correct: " + str(correct))
    print("Incorrect: " + str(incorrect))
    print("Total: " + str(total))
    # Write the results to the output file
    with open(output_path, "w") as f:
        d = {"correct": correct, "incorrect": incorrect, "total": total}
        json.dump(d, f)
    f.close()
    return correct, incorrect, total


def precision(correct: int, total: int):
    """

    :param correct: int representing the number of correct results
    :param total: int representing the total number of results
    :return: the precision of the results
    """
    return correct / total


def pre_processing(input_path: str = "./input/train.jsonl", output_path: str = "./input/pre_processed.jsonl", sample_size: int = 1000):
    """

    :param input_path: str representing the path to the validation set
    :param output_path: str representing the path to the output file with the pre-processed data
    :param sample_size: str representing the number of samples to be used for pre-processing
    :return: the dict of all samples
    """
    import json
    from datasets import load_dataset
    from tqdm import tqdm
    # Load the dataset
    ds = load_dataset('fever', 'wiki_pages')
    ds = ds['wikipedia_pages']
    # Remove the lines column
    ds = ds.remove_columns('lines')
    # Put in pandas
    df = ds.to_pandas(500, batched=False)
    # Set the index to the id, this makes it faster
    df.set_index('id', inplace=True)
    with open(output_path, 'w') as r:
        with open(input_path, "r") as f:
            line = f.readline()
            # Counter to keep track of the number of samples and abort when the sample size is reached
            counter = 0
            # Time updates
            pbar = tqdm(total=sample_size)
            while line:
                json_obj = json.loads(line)
                label = json_obj["label"]
                # We filter out the entries where the label is "NOT ENOUGH INFO", these are irrelevant for our task
                if label == "NOT ENOUGH INFO":
                    line = f.readline()
                    continue
                evidence = ''
                for i in range(len(json_obj["evidence"][0])):
                    evidence_page = json_obj["evidence"][0][i][2]
                    temp = df.loc[df.index == evidence_page]
                    # If the is no evidence page, we skip it
                    if temp.empty:
                        continue
                    # Concatenate the evidence to eachother
                    evidence += df.loc[df.index == evidence_page].iloc[0]['text'] + ' '
                # If there is no evidence, we skip it
                if evidence == '':
                    line = f.readline()
                    continue
                claim_txt = json_obj["claim"]
                # Create the dict and write it to the output file
                dict = {"claim": claim_txt, "evidence": evidence, "label": label}
                json.dump(dict, r)
                r.write('\n')
                # Update the progress bar
                pbar.update(1)
                # Read the next line
                line = f.readline()
                # Update the counter
                counter += 1
                # If the counter is equal to the sample size, we stop
                if counter == sample_size:
                    f.close()
                    r.close()
                    return dict
    f.close()
    r.close()
    return dict


def dump_wiki():
    import json
    from datasets import load_dataset
    from tqdm import tqdm

    # Load the dataset
    ds = load_dataset('fever', 'wiki_pages')
    ds = ds['wikipedia_pages']
    # Remove the lines column
    ds = ds.remove_columns('lines')
    # Put in pandas
    df = ds.to_pandas(500, batched=False)
    # Set the index to the id, this makes it faster
    df.set_index('id', inplace=True)
    with open("output/wiki-pages.json", "w") as f:
        pb = tqdm(total=len(df))
        for index, row in df.iterrows():
            d = {"text": row['text']}
            json.dump(d, f)
            f.write("\n")
            pb.update(1)


if __name__ == "__main__":
    # top_k_minimal()
    cProfile.run('top_k_fever_small()', sort="cumulative")
    # extract_train_claims()
