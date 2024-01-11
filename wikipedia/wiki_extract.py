"""The text from html extraction part of this script was based
on the following stack overflow answer:
    https://stackoverflow.com/a/24968429

"""

import os

from typing import List
from bs4 import BeautifulSoup
from wiki_extract_helpers import get_wiki_category_page_ids, get_wiki_page



def store_wiki_category_pages(category: str, depth: int, output_path: str) -> None:

    assert os.path.exists(output_path), f"Wiki page output path '{output_path}' does not exist!"

    page_ids: List[int] = get_wiki_category_page_ids(category, depth=depth)
    
    print(len(page_ids))
    print(page_ids)
    return

    for page_id in page_ids:
        page_plaintext: str = soupify_wiki_html_page(*get_wiki_page(page_id))
        with open(f"{output_path}/{page_id}.txt", "w") as of:
            of.write(page_plaintext)



def soupify_wiki_html_page(title: str, subtitle: str, html: str) -> str:
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

    text = title + "\n" + subtitle + "\n" + text

    return text#.encode('utf-8')

store_wiki_category_pages("Cats", 0, "corpus")
