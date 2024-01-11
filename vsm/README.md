# Vector Space Model (VSM)

A VSM for information retrieval represents queries and documents as vectors, where each axis of the space is a term in the vocabulary of the collection of documents that are managed by the VSM.

By calculating a similarity score between a given query and the documents of the VSM, we can disciminate relevant documents from irrelevant documents. Relevant documents can then be retrieved as results for a query through the VSM.

To speed up these calculations, we shall make use of an inverted document index.

## Pre-Processing

The performance of a VSM generally improves through the application of some **pre-processing steps** for both the query and documents.

The documents are pre-processed to **normalize their contents**, and to limit the dimensionality of the resulting vocabulary and inverted document index. If the query is then pre-processed using the exact same steps as were used for the documents, then **fewer terms need to be evaluated** to produce the similarity scores and thus the top-k ranking relevant documents.

## Query & Document Pre-Processing



Pre-processing happens within the [VSMTokenizer](/vsm/vsm_tokenizer.py) class. After we detail the pre-processing steps, we make some [concluding observations](#concluding-observations). It consists of the following steps:

* Normalizing accented (unicode) characters
* Converting Case
* [Converting numbers to their word form](#numbers-to-words)
* [Expand contractions](#expand-contractions)
* Removing special characters
* [Stemming](#stemming)
* [Removing stopwords](#removing-stopwords)

But first, we provide a short explanation on the use of true tokenizers within the VSMTokenizer.

### True Tokenizers

Calling our class VSMTokenizer is perhaps somewhat misguided. Because what is often referred to as a tokenizer, only splits input strings, natural language sentences in our use-case, into its constituent tokens, such as words and punctuation symbols. Our VSMTokenizer also performs pre-processing, and makes use of an actual tokenizer to do the tokenization of sentences. To avoid confusion, we will refer to such methods as _true tokenizers_ in this section.

We may refer to token-based pre-processing as text-based pre-processing as well (see [challenges](#challenges)). These are processing steps that apply transformations on a token-by-token level of granularity.

There are many tokenizer implementations to choose from. To keep things simple, we will restrict
our search to the [nltk tokenize module](https://www.nltk.org/api/nltk.tokenize.html).

### Tokenizer choice

As an initial attempt at tokenization, we simply used python's built-in `str.split()` method. This is incredibly fast, but treats punctuation very naïvely. This results in tokens that simply have punctuation symbols attached to them.

We then tried the [ToktokTokenizer](https://www.nltk.org/api/nltk.tokenize.toktok.html). This tokenizer is reasonably fast, but we disliked the way it treated constraction by splitting them, such as `y'all` into `y`, `'` and `all`.

We **settled on** using the `nltk.tokenize.word_tokenize` tokenizer. This is a somewhat slower tokenizer, but it handles contractions and punctuation as we wanted.

### Expand Contractions

After some initial research, two options presented themselves:
- Naïve contraction expansion, by following [this article](https://www.kdnuggets.com/2018/08/practitioners-guide-processing-understanding-text-2.html)
- Smart contraction expansion, by using [the pycontractions module](https://pypi.org/project/pycontractions/)

The naïve approach make use of simple substitutions, mapping each contraction to exactly one expanded form. This ensures a more speedy, though naïve expansion process.

The smart approach applies a three pass approach, that possibly considers multiple viable expanded strings for every single contraction. This provides a more correct result, at the cost of speed.

For the initial implementation of the pre-processing, and until we specify otherwise, **we will make use of the naïve method**. We have several reasons for this.
+ Many other steps must be performed for a single fact-check, so **processing speed** is important.
+ Many of the words produced by expanding contractions **are stopwords**, which will be removed in a following pre-processing step.
+ Many of the words produced by expanding contractions **are common words**, so their impact on the final score is relatively low.

For these reasons, less accurate expansions are acceptable.

### Numbers to Words

We want to minimize the impact of numbers on the **dimensionality of the vocabulary**. This is because numbers represent an explosion of possible terms. To reduce them to a normalized form, we **convert them from numeric representation to word representation**. For example:

number | words
-- | -
102 | one hundred two
-1.3 | minus one point three
1.4433 | one point four four three three
.1 | point one
-.1 | minus zero point one
1\. | one point
-1. | minus one point

'102' converts to 'one hundred two', '-1.3' converts to 'minus one point three'.

We utilize the [inflect module](https://pypi.org/project/inflect/) to enable this conversion step. We take some liberties during this conversion:
+ All connectors between the converted words are removed
  - NOT "twenty-three", BUT "twenty three"
  - NOT "one thousand, two hundred and two", but "one thousand two hundred two"
  - So '-', ',' and 'and' are pruned from the output words

### Stemming

Stemming is a very impactful step of the normalization proces. Stemming is the proces of mapping a word to its word stem, by following some stemming algorithm. For example, using the PorterStemmer from nltk, the words "eat", "eating" and "eaten" all get mapped to the stem "eat". However, stemming does not necessarily result in words that are found in the dictionary: "hundred" becomes "hundr".

Another option to achieve similar results is lemmatization. Lemmatization does always result in words found in the dictionary. However, it is slower. So with performance in mind, **we prefer stemming over lemmatization**.

### Removing Stopwords

Stop words are words that contribute relatively less to the meaning of a sentence. But some of them are very common words, such as "the", "and", etc.

Removing them **lowers the dimensionality** of the vocabulary of the VSM. Additionally, because some of those words are extremely common, such as "the", pruning them from the vocabulary may considerably reduce length of some queries and documents.  The computational cost of removing these stopwords will somewhat be recovered due to two sped up steps:
* faster top-k document retrieval, because less unique query terms need to be processed
* faster inverted document index generation, because less document terms need to be processed

Query processing will also be sped up because extremely common words such as "the" would have had very long posting lists, if they were not removed. This also spares us from having to maintain posting lists for those terms.

### Concluding Observations

This section details some observations about the text pre-processing. It aims to provide more insight into its challenges and contributions to the VSM model.

#### Challenges

**Balancing** between **text-based** and **regex-based** pre-processing steps took some trial and error. For example, the contraction replacement was ill suited to `re.sub` type replacements. Implementing it by applying substitutions token by token was a fair bit faster. These kinds of considerations were tested individually for each of the applicable pre-processing steps.

The **ordering** of **removing (replacing) special characters** in the set of pre-processing steps had to be carefully considered. Because two steps depend on special characters:
* Numbers to words conversion: depends on hyphons, e.g. "twenty-three"
* Contraction expansion: depends on single quotes, e.g. "i'd"

So we perform special character removal after both of these steps have concluded. Another option would be to consider the special characters the other steps depend on in separate, specialised special character removel steps.

**The choice of stemmer** affects the quality/dimensionality of the output tokens. We make use of stemmers part of the `nltk` module.\
Suppose the query string contains "one". Then the `PorterStemmer` will produce "one", while the `LancasterStemmer` will produce "on". This is important, because we consider "on" to be a stopword, so the `VSMTokenizer` will never output any stemmed form of "1" or "one". If a query contains either of these, then they will not be reflected in the output tokens.\
A more subtle case is the query "1000". The number to words conversion will map this to "one thousand", the stemmer reduce this to "on thousand", and stopword removal finally produces "thousand". So the order of the pre-processing steps and use of a particular stemmer may somewhat negatively impact the quality and or dimensionality of the output tokens.

