# Corpus

We need a sizeable corpus of documents for use in fact verification. Else we may not be able to provide the evidence required to validate a claim.

# Running

For generating our corpus, we provide a [separate script](/wikipedia/generate_corpus.py). To get started, you best display its help info. **Note that it MUST be called from the same directory it is located at!**

```bash
python3 generate_corpus.py -h
```

We recommend running the script in two steps. **First**, download the html articles to store them on disk. Is is required to specify the category recursion depth as its value. It is also best to generate the visualization, as it provides insight into how many subcategories were used. Note that the visualization is generated *before* any of the html documents are downloaded.

```bash
python3 generate_corpus.py --download 0 --visualization
```

The process all the downloaded html files to strip their html tags. The corpus can be used to construct the VSM index.

```bash
python3 generate_corpus.py --process
```


# Wikipedia

One option is to extract a number of pages from wikipedia, which may serve as evidence. Each wikipedia page has a unique, associated page id. For example, the [page for cat](https://en.wikipedia.org/wiki/Cat) has id $6678$. You can manually look up a page using its id as follows.

https://en.wikipedia.org/w/index.php?curid=PAGE_ID

Replace `PAGE_ID` by the id of the page itself. For the cat page, this becomes:

https://en.wikipedia.org/w/index.php?curid=6678

Notably, wikipedia also makes use of categories to organize its pages. One such category is `Cats`. The cat page falls under this category. So by making use of categories, we can construct a corpus around a specific topic.

Categories also have related subcategories. This means we can recursively query the subcategories of **one single main category** to great effect. Because wikipedia articles are organically organised under categories and subcategories, this will result in a useful corpus when enough levels subcategory of recursion are used. Because then the corpus consists of many related pages.

## Wikipedia API

We considered the use of the [PetScan tool](https://petscan.wmflabs.org/) to retrieve the pages for this task, but we could not get it to work. So we turned to the Wikipedia API instead.

The Wikipedia API has two endpoints we can use:
* [the query action with the categorymembers list](https://en.wikipedia.org/w/api.php?action=help&modules=query%2Bcategorymembers)
* [the parse action](https://en.wikipedia.org/w/api.php?action=help&modules=parse)

The **query action** with the category members list lets us query all pages by id and all subcategories for a specified category. So we can manually send "recursive" requests for the depth of subcategory recursion we desire. This way, we may collect a list of page ids related to the chosen category and subsequent subcategories.

The **parse action** allows us to retrieve the content of individual pages by page id. We can fetch the html content of all pages for which we have collected the page ids using the recursive category search.

## Pre-processing

Since html is not very useful for fact verification, we should strip all the html tags from each of the retrieved wikipedia articles. We can do this using [beautiful soup](https://pypi.org/project/beautifulsoup4/).
