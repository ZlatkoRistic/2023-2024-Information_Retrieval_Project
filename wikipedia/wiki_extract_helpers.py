import requests
from typing import List, Set, Tuple


# Constants, for easy editing
WIKI_LANG: str = "en"
WIKI_FORMAT: str = "json"

WIKI_CM_TYPE: str = "subcat%7Cfile%7Cpage"
WIKI_CM_LIMIT: str = "max"      # Should be an integer >= 0 OR the string 'max'

WIKI_PAGE_PROP: str = "text%7Ccategories%7Csections%7Cdisplaytitle%7Csubtitle"



def get_wiki_category_page_ids(wiki_category: str, depth: int = 0) -> Set[int]:
    """Get all wikipedia page ids that belong to the specified *wiki_category*
    wikipedia category. If *depth* is larger than zero, then recursively
    do the same for all subcategories of the *wiki_category* for *depth*
    levels of subcategories.

    :param wiki_category: The top-level category to retrieve all page ids for
    :param depth: The number of times to recurse on the subcategories
    :return: The set of page ids belonging to all retrieved categories and subcategories
    """
    depth = max(0, depth)
    page_ids: Set[int] = set()
    seen_categories: Set[str] = set()
    curr_categories: Set[str] = {wiki_category}

    for _ in range(depth + 1):      # +1, first iteration retrieves the category's pages
        # Only process unseen categories
        curr_categories.difference_update(seen_categories)
        # Mark new categories as seen
        seen_categories.update(curr_categories)
        new_categories: Set[str] = set()
        for category in curr_categories:
            cat_page_ids, subcategories = _get_wiki_category_info(category)
            page_ids.update(cat_page_ids)
            new_categories.update(subcategories)
        # Store categories for next iteration
        curr_categories = new_categories

    return page_ids


def _get_wiki_category_info(category: str):
    """Get the page and subcategory information related to the specified *category*.

    This method will continue to query the wikipedia API until ALL the info/results
    for the category are retrieved.

    :param category: The category to find related info for
    :return: (
        The list of pages related to the category,
        The list of subcategories of the category
    )
    """
    wiki_subcat_query: str = f"https://en.wikipedia.org/w/api.php?action=query&format={WIKI_FORMAT}&uselang={WIKI_LANG}&list=categorymembers&formatversion=2&cmtitle=Category%3A{category}&cmtype={WIKI_CM_TYPE}&cmlimit={WIKI_CM_LIMIT}"
    response_contains_continue: bool = True
    cmcontinue_param: str = ""

    page_ids: List[int] = []
    subcategories: List[str] = []

    while response_contains_continue:
        # Get page ids and subcategories
        response: dict = requests.get(wiki_subcat_query + cmcontinue_param).\
            json()

        # If there are still pages and/or subcategories remaining, then continue querying.
        continue_section = response.get("continue", None)
        response_contains_continue = continue_section is not None
        if response_contains_continue:
            cmcontinue_param = "&cmcontinue=" + continue_section["cmcontinue"]
        else:
            cmcontinue_param = ""

        # Extract page ids and subcategories
        query_key: str = "query"
        catmem_key: str = "categorymembers"
        if query_key not in response:
            continue
        if catmem_key not in response[query_key]:
            continue

        for catmem in response[query_key][catmem_key]:
            title: str = catmem["title"]
            pageid: int = catmem["pageid"]

            if "category:" == title.lower()[:9]:
                subcategories.append(title[9:])
            else:
                page_ids.append(pageid)

    return page_ids, subcategories

def get_wiki_page(page_id: int) -> Tuple[str, str, str]:
    """Get the wikipedia page corresponding to the given *page_id*.
    Also retrieve the page title and subtitle for completeness' sake

    :param page_id: The page ID of the to retrieve page
    :return: (
        page title,
        page subtitle,
        page contents as an html string
    )
    """
    wiki_page_query: str = f"https://en.wikipedia.org/w/api.php?action=parse&format={WIKI_FORMAT}&pageid={page_id}&prop={WIKI_PAGE_PROP}&formatversion=2"
    response: dict = requests.get(wiki_page_query).\
        json()
    
    parse_key: str = "parse"
    if parse_key not in response:
        return ""
    data: dict = response[parse_key]

    title = data.get("title", "")
    subtitle = data.get("subtitle", "")
    text = data.get("text", "")

    return title, subtitle, text
