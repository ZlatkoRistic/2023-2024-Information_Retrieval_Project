import csv
import cProfile

from vsm import VSM


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
    with open("train.jsonl", "r") as f:
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


if __name__ == "__main__":
    # top_k_minimal()
    cProfile.run('top_k_fever_small()', sort="cumulative")
    # extract_train_claims()