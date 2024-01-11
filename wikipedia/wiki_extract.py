"""The text from html extraction part of this script was based
on the following stack overflow answer:
    https://stackoverflow.com/a/24968429

"""

import os

from pathlib import Path
from typing import List
from bs4 import BeautifulSoup
from wiki_extract_helpers import get_wiki_category_page_ids, get_wiki_page



def store_wiki_category_pages(category: str, depth: int, output_path: str, visualization_output_path: str = None) -> None:
    """Store the raw wiki page content for the category and all subcategories recursively,
    up until the specified depth.

    :param category: The Wikipedia category to recursively retrieve pages for
    :param depth: The subcategory recursion depth
    :param output_path: The path to the directory where to store the page content
    :param visualization_output_path: The path to store the visualization of the
    category hierarchy for the retrieved categories and files
    """

    assert os.path.exists(output_path), f"Wiki page output path '{output_path}' does not exist!"

    page_ids: List[int] = get_wiki_category_page_ids(category, depth=depth, output_path=visualization_output_path)
    
    for page_id in page_ids:
        _, _, page_content_html = get_wiki_page(page_id)
        with open(f"{output_path}/{page_id}.html", "w") as of:
            of.write(page_content_html)


def soupify_wiki_category_pages(input_path: str, output_path: str):
    """Process using BeatifulSoup the raw wiki pages located at the *input_path*
    and store them at the *output_path*
    """

    assert os.path.exists(input_path), f"Raw Wiki page input path '{input_path}' does not exist!"
    assert os.path.exists(output_path), f"Processed Wiki page output path '{output_path}' does not exist!"

    input_path += ('' if input_path[-1] == '/' else '/')
    output_path += ('' if output_path[-1] == '/' else '/')

    files = Path(input_path).glob('*.html')
    for file in files:
        with open(file, "r") as inp_file:
            output_file_path: str = f"{output_path}{file.name}"
            output_file_path = output_file_path[:-4] + "txt"      # Replace extension: html -> txt
            with open(output_file_path, "w") as out_file:
                out_file.write(_soupify_wiki_html_page(inp_file.read()))


def _soupify_wiki_html_page(html: str) -> str:
    """Process the given *html* using BeatifulSoup.

    :param html: The html sting to process
    :return: The processed string
    """
    soup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text
