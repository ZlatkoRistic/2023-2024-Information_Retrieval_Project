# Corpus

We need a sizeable corpus of documents for use in fact verification. Else we may not be able to provide the evidence required to validate a claim.

The primary goal of this corpus, is to serve as an evidence base for the fact checker. For that, we should be able to select relevant evidence from the corpus to fact check with. For this, we need to construct a [VSM](/src/vsm/README.md) index. This index will help us do ranked retrieval, to select the evidence to feed to the fact checker.

Since python is used, the size of the index may be fairly sizeable.

# Running

For generating our corpus, we provide a [separate script](./generate_corpus.py). To get started, you best display its help info. Note that this script can be called from anywhere; the output directory paths are bound relatively to the location of the scipt itself.

```bash
python3 generate_corpus.py -h
```

We first showcase a full command, that will generate an entire corpus and index. Then we will explain each component.

```bash
python3 generate_corpus.py -d 0 -v -p -i
```

The above command will trigger multiple steps in the script. **First**, download the html articles to store them on disk. This matches the `-d` or `--download` options. It is required to specify the category recursion depth as its value. This depth is how many subcategories deep the downloading should recurse, to search for related Wikipeda pages. It is also best to generate the visualization, as it provides insight into how many and *which* subcategories were used. This matches the `-v` or `--visualization` options. Note that the visualization is generated *before* any of the html documents are downloaded.

If you simply want to see this script run for the fun of it, then using a depth of $0$ is recommended. At the time of writing, this will result in a download of $25$ articles, in under a minute.

The raw articles will be downloaded to the [corpus/raw-articles/](./corpus/raw-articles/) directory and the visualization to the [corpus/](./corpus/) directory.

```bash
python3 generate_corpus.py --download 0 --visualization
```

Processing strips all the downloaded html files of their html tags. This matches the `-p` or `--process` options. This provides semi-natural language corpus. We say semi, because stripping the html essentially means concatenating sentences or words that may not have been intended to form a "sentence" together.

The processed articles will be output to the [corpus/processed-articles/](./corpus/processed-articles/) directory.

```bash
python3 generate_corpus.py --process
```

From this "natural language" corpus, we can construct a VSM index. This matches the `-i` or `--index` options.

The index will appear in the [corpus/](./corpus/) directory, likely (because we may change this detail) as `index.dump`.

```bash
python3 generate_corpus.py --index
```

In conclusion, all the previous steps can be chained together to construct an index from downloaded and subsequently processed wikipedia articles.

At the time of running, if a download recursion depth of $0$ is used, then the full command using all options -- `-d 0`, `-v`, `-p` and `-i` -- runs for around a minute. Using the same options and depth $1$ clocked in at around $7$ minutes.

Note that chaining these steps is possible due to their execution order. They run in the following order:
+ download & visualization
+ process
+ index

with all of them being optional steps. So each step can be run individually. This allows local processing on already or pre-installed articles and index re-construction, without needing to (re-)download.

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

The **parse action** allows us to retrieve the content of individual pages by page id. We can fetch the html content of all pages for which we have collected the page ids using the recursive category search. We must then individually fetch them using the wikipedia parse action API.

## Pre-processing

Since html is not very useful for fact verification, we should strip all the html tags from each of the retrieved wikipedia articles. We can do this using [beautiful soup](https://pypi.org/project/beautifulsoup4/).
