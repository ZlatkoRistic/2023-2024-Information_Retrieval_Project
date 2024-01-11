import requests
from typing import List, Set, Tuple, Dict


# Constants, for easy editing
WIKI_LANG: str = "en"
WIKI_FORMAT: str = "json"

WIKI_CM_TYPE: str = "subcat%7Cfile%7Cpage"
WIKI_CM_LIMIT: str = "max"      # Should be an integer >= 0 OR the string 'max'

WIKI_PAGE_PROP: str = "text%7Ccategories%7Csections%7Cdisplaytitle%7Csubtitle"



def get_wiki_category_page_ids(wiki_category: str, depth: int = 0, output_path: str = None) -> Set[int]:
    """Get all wikipedia page ids that belong to the specified *wiki_category*
    wikipedia category. If *depth* is larger than zero, then recursively
    do the same for all subcategories of the *wiki_category* for *depth*
    levels of subcategories.

    :param wiki_category: The top-level category to retrieve all page ids for
    :param depth: The number of times to recurse on the subcategories
    :param dot_output_path: The output path of the visualization of the recursive
    hierarchy between the *wiki_category* and its pages and subcategories
    :return: The set of page ids belonging to all retrieved categories and subcategories
    """
    depth = max(0, depth)
    page_ids: Set[int] = set()
    seen_categories: Set[str] = set()
    curr_categories: Set[str] = {wiki_category}
    dot_dict: dict = dict()
    should_output: bool = output_path is not None

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
            if should_output: dot_dict[category] = (subcategories, cat_page_ids)

        # Store categories for next iteration
        curr_categories = new_categories

    if should_output:
        _to_category_tree(wiki_category, dot_dict, output_path)
        print("wrote output to:", output_path)

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

def _to_category_tree(init_category: str,
                            category_dict: Dict[str, Tuple[List[str], List[int]]],
                            output_path: str) -> None:
    """Convert a mapping from category to a tuple containing first a list
    of subcategories and then a list of page ids to a file tree style string
    and write it to file.

    :param init_category: The category that is the top-level category, of which
    all other categories are subcategories
    :param category_dict: A mapping from category to subcategories and page ids
    :param output_path: The ouput path for the file
    """
    out_str: str = _build_category_tree(init_category, category_dict)

    with open(output_path, "w") as of:
        of.write(out_str)

def _build_category_tree(category: str,
                     category_dict: dict,
                     cat_tree: str = "",
                     current_depth: int = 0,
                     simplify_whitespace: bool = False) -> str:
    """Recursively build a file tree style string for a mapping from category
    to a tuple containing first a list of subcategories and then a list of page ids.

    :param category: The current category to recurse on
    :param category_dict: The mapping containing all the category to subcategory and page ids info
    :param cat_tree: The category tree being built
    :param current_depth: The current recursion depth. This equals the current subcategory or file tree depth
    :param simplify_whitespace: Whether or not to use a '|' in the whitespace symbol
    :return: The recursively built category tree string
    """
    # Leaf node for subcategories
    if category not in category_dict:
        return cat_tree

    mid_symbol: str = "├──"
    end_symbol: str = "└──"
    ws_symbol: str  = (" " if simplify_whitespace else "|") + "   "
    ws_symbol *= current_depth
    subcats, page_ids = category_dict[category]
    no_subcats: bool = len(subcats) == 0

    # Add top-level category
    if current_depth == 0:
        cat_tree += category + "\n"

    # Add #pages
    cat_tree += ws_symbol + (end_symbol if no_subcats else mid_symbol) + " #pages: " + str(len(page_ids)) + "\n"
    # Recursively add subcategories
    for idx, subcat in enumerate(subcats):
        is_final_subcat: bool = idx == (len(subcats) - 1)
        cat_tree += ws_symbol + (end_symbol if is_final_subcat else mid_symbol) + " " + subcat + "\n"
        cat_tree = _build_category_tree(subcat, category_dict, cat_tree, current_depth + 1, simplify_whitespace=(current_depth == 0 and is_final_subcat))

    return cat_tree

def get_wiki_page(page_id: int) -> Tuple[str, str, str]:
    """Get the wikipedia page corresponding to the given *page_id*.
    Also retrieve the page title and subtitle for completeness' sake.
    The title is also present in the html contents, as a display title.

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

    display_title: str = data.get("displaytitle", "")
    title: str = data.get("title", "")
    subtitle: str = data.get("subtitle", "")
    text: str = data.get("text", "")

    return title, subtitle, display_title + text
