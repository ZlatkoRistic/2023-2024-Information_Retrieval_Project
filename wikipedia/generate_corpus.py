import argparse

from wiki_extract import store_wiki_category_pages, soupify_wiki_category_pages



if __name__ == "__main__":
    # Argument handling based on https://www.geeksforgeeks.org/command-line-arguments-in-python/

    cat_hierarchy_viz_path: str  = "corpus/visualization.txt"
    wiki_raw_path: str       = "corpus/raw-articles"
    wiki_processed_path: str = "corpus/processed-articles"
    root_category: str       = "Cats"

    # Setup parser
    parser = argparse.ArgumentParser(description="Functionality to generate the evidence corpus.")
    parser.add_argument("-d", "--download", required=False, type=int, choices=range(0, 10), help = "Download the wikipedia articles, based on the specified category recursion depth.")
    parser.add_argument("-v", "--visualization", action='store_true', help = "When downloading the wikipedia articles, generate a visualization of the category hierarchy.")
    parser.add_argument("-p", "--process", action='store_true', help = "Process the downloaded wikipedia articles.")
    args = parser.parse_args()

    # Do corpus generation
    if args.download is not None:
        cat_recursion_depth: int = args.download
        cat_hierarchy_path = cat_hierarchy_viz_path if args.visualization else None
        store_wiki_category_pages(root_category, cat_recursion_depth, wiki_raw_path, cat_hierarchy_path)
    elif args.process:
        soupify_wiki_category_pages(wiki_raw_path, wiki_processed_path)
