# Corpus

We need a sizeable corpus of documents for use in fact verification. Else we may not be able to provide the evidence required to validate a claim.

# Wikipedia

One option is to extract a number of pages from wikipedia, which may serve as evidence. Each wikipedia page has a unique, associated page id. For example, the page for cat has id $6678$. You can manually look up a page using its id as follows.

https://en.wikipedia.org/w/index.php?curid=PAGE_ID

Replace `PAGE_ID` by the id of the page itself. For the cats page, this becomes:

https://en.wikipedia.org/w/index.php?curid=6678

Notably, wikipedia also makes use of categories to organize its pages. One such category is `Cats`. The cat page falls under this category. So by making use of categories, we can construct a corpus around a specific topic.

Categories also have related subcategories. This means we can recursively query the subcategories of **one single main category** to great effect. Because wikipedia articles are organically organised under categories and subcategories, this will result in a useful corpus of enough levels subcategory of recursion are used, so that the corpus consists of many related pages.
