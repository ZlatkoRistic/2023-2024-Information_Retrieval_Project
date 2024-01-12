import argparse
import pathlib
import sys

from pathlib import Path
from wiki_extract import store_wiki_category_pages, soupify_wiki_category_pages

this_file_path: str = pathlib.Path(__file__).parent.resolve().as_posix()
sys.path.append(this_file_path + '/../../')

from src.vsm.vsm import VSM



if __name__ == "__main__":
    # Argument handling based on https://www.geeksforgeeks.org/command-line-arguments-in-python/


    cat_hierarchy_viz_path: str  = f"{this_file_path}/corpus/visualization.txt"
    wiki_raw_path: str           = f"{this_file_path}/corpus/raw-articles"
    wiki_processed_path: str     = f"{this_file_path}/corpus/processed-articles"
    vsm_index_dump_path: str     = f"{this_file_path}/corpus/index.dump"
    root_category: str = "Cats"

    # Setup parser
    parser = argparse.ArgumentParser(description="Functionality to generate the evidence corpus. Can be used to generate a VSM index from the processed corpus. Can be run from any location; the used output paths are bound relatively to the path of this script.")
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
        file_extension: str = ".txt"
        files = Path(wiki_processed_path).glob('*' + file_extension)
        for file in files:
            ID: int = int(file.name[:-len(file_extension)])
            with open(file, "r", encoding="utf8") as processed_file:
                vsm.add_document(processed_file.read(), ID)

        with open(vsm_index_dump_path, "w") as index_file:
            index_file.write(vsm.dumps("\t"))
