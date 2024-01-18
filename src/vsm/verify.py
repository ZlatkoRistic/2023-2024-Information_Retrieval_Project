import argparse
import pathlib
import sys
import time

this_file_path: str = pathlib.Path(__file__).parent.resolve().as_posix()
sys.path.append(this_file_path + '/../../')

import ir_datasets

from typing import Dict
from src.vsm.vsm import VSM



# Setup parser
parser = argparse.ArgumentParser(description="Functionality to verify the VSM implementation. Can be used to generate a VSM index from the cranfield dataset. Can be run from any location; the used output paths are bound relatively to the path of this script.")
parser.add_argument("-i", "--index", action='store_true', help = "Construct an index from the cranfield dataset.")
parser.add_argument("-r", "--run-verification", action='store_true', help = "Do the verification of the VSM implementation using the stored index dump.")
parser.add_argument("-v", "--verbose", action='store_true', help = "Print a verbose verification output.")
args = parser.parse_args()



class Relevance:
    NO: int       = -1
    MIN: int      =  1
    USEFUL: int   =  2
    RELEVANT: int =  3
    COMPLETE: int =  4



if __name__ == "__main__":
    """This verification process will make use of the cranfield dataset.
    This dataset defines several relevance levels of documents compared to
    queries:
        -1 References of no interest.
         1 References of minimum interest, for example, those that have been included from an historical viewpoint.
         2 References which were useful, either as general background to the work or as suggesting methods of tackling certain aspects of the work.
         3 References of a high degree of relevance, the lack of which either would have made the research impracticable or would have resulted in a considerable amount of extra work.
         4 References which are a complete answer to the question.
    """


    # Based on the snippets at: https://ir-datasets.com/cranfield.html
    index_file_name: str = "vsm-verification-index.dump"
    index_output_path: str = f"{this_file_path}/output/{index_file_name}"
    dataset = ir_datasets.load("cranfield")
    prefix: str = "[FC]"


    if args.index:
        vsm: VSM = VSM()

        # Load docs into VSM
        print(prefix, "Starting index construction ...")
        start_time = time.time()
        for doc in dataset.docs_iter():
            vsm.add_document(doc.text, int(doc.doc_id))

        # Dump index file
        with open(index_output_path, "w", encoding="utf8") as index_file:
            index_file.write(vsm.dumps("\t"))
        print(prefix, "Finished index construction in {:.2f}s!".format(time.time() - start_time))
        print(prefix, "Dumped index at", index_output_path)

    if args.run_verification:
        vsm = VSM()
        qrels_dict = dataset.qrels_dict()
        avg_precision: float = 0.0
        avg_recall: float = 0.0
        processed_queries_nr: int = 0
        k: int = 3

        # Load index dump
        print(prefix, "Loading index from", index_output_path)
        with open(index_output_path, "r", encoding="utf8") as index_file:
            vsm.loads(index_file.read())

        # Do verification
        print(prefix, "Starting VSM verification ...\n")
        start_time: float = time.time()
        # Get all documents from the dataset for the query for which relevancy is stored
        for query in dataset.queries_iter():
            query_id: str = query.query_id
            docs_relevancy: Dict[str, int] = qrels_dict.get(query_id, None)

            # If no relevance info is available for the query, then skip
            if docs_relevancy is None:
                continue

            # Do ranked retrieval
            ranked_docs = vsm.get_top_k(query.text, k)

            # Update verification scores
            relevancy_cutoff: int = Relevance.RELEVANT
            relevant_retrieved: int = 0
            total_relevant: int = len([1 for relevancy in docs_relevancy.values() if relevancy >= relevancy_cutoff])
            for doc_id, _ in ranked_docs:
                relevancy_score = docs_relevancy.get(str(doc_id), -1)
                relevant_retrieved += relevancy_score >= relevancy_cutoff

            precision: float = relevant_retrieved / k
            recall: float = (relevant_retrieved / total_relevant) if total_relevant > 0 else 0.0


            avg_precision += precision
            avg_recall += recall
            processed_queries_nr += 1

            if args.verbose and (precision > 0.0 or recall > 0.0):
                print("== queryID=", query_id)
                print(f"ranked {k} results: ", [(did, dsc) for did, dsc in docs_relevancy.items()])
                print("relevant docs: ", sorted({(int(did), int(dsc)) for did, dsc in docs_relevancy.items()}))
                print("retrieved docs: ", sorted({d[0] for d in ranked_docs}))
                print("precision:", precision)
                print("recall:", recall)
                print()

        avg_precision /= float(processed_queries_nr) if processed_queries_nr > 0 else 1.0
        avg_recall    /= float(processed_queries_nr) if processed_queries_nr > 0 else 1.0

        print(prefix, "Finished VSM verification in {:.2f}s!".format(time.time() - start_time), f"""
    avg_precision: {avg_precision}
    avg_recall:    {avg_recall}
""")
