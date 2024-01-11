import argparse
import pathlib

from pathlib import Path
from wiki_extract import store_wiki_category_pages, soupify_wiki_category_pages

import sys
sys.path.append('../')

from src.vsm.vsm import VSM

if __name__ == "__main__":
    # Argument handling based on https://www.geeksforgeeks.org/command-line-arguments-in-python/

    this_file_path: str = pathlib.Path(__file__).parent.resolve().as_posix()

    cat_hierarchy_viz_path: str  = f"{this_file_path}/corpus/visualization.txt"
    wiki_raw_path: str           = f"{this_file_path}/corpus/raw-articles"
    wiki_processed_path: str     = f"{this_file_path}/corpus/processed-articles"
    vsm_index_dump_path: str     = f"{this_file_path}/corpus/index.dump"
    root_category: str = "Cats"

    # Setup parser
    parser = argparse.ArgumentParser(description="Functionality to generate the evidence corpus.")
    parser.add_argument("-d", "--download", required=False, type=int, choices=range(0, 10), help = "Download the wikipedia articles, based on the specified category recursion depth.")
    parser.add_argument("-v", "--visualization", action='store_true', help = "When downloading the wikipedia articles, generate a visualization of the category hierarchy.")
    parser.add_argument("-p", "--process", action='store_true', help = "Process the downloaded wikipedia articles.")
    parser.add_argument("-i", "--index", action='store_true', help = "Construct an index from the processed wikipedia articles.")
    args = parser.parse_args()

    # Do corpus generation
    if args.download is not None:
        cat_recursion_depth: int = args.download
        cat_hierarchy_path = cat_hierarchy_viz_path if args.visualization else None
        store_wiki_category_pages(root_category, cat_recursion_depth, wiki_raw_path, cat_hierarchy_path)
    if args.process:
        soupify_wiki_category_pages(wiki_raw_path, wiki_processed_path)
    if args.index:
        vsm: VSM = VSM()
        files = Path(wiki_processed_path).glob('*.txt')
        for file in files:
            print(file.name, type(file.name))
            exit()
            with open(file, "r", encoding="utf8") as processed_file:
                vsm.add_document(processed_file.read(), )

        with open(vsm_index_dump_path, "w") as index_file:
            index_file.write(vsm.dumps("\t"))
