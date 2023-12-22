# Vector Space Model (VSM)

A VSM for information retrieval represents queries and documents as vectors, where each axis of the space is a term in the vocabulary of the collection of documents that are managed by the VSM.

Documents can be retrieved for a query through the VSM. By calculating a similarity score between a given query and the documents of the VSM, we can disciminate relevant documents from irrelevant documents.

To speed up these calculations, we shall make use of an inverted document index.

## Pre-Processing

The performance of a VSM generally improves through the application of some **pre-processing steps** for both the query and documents.

The documents are pre-processed to **normalize their contents**, and to limit the dimensionality of the resulting vocabulary and inverted document index. If the query is then pre-processed using the exact same steps as were used for the documents, then **fewer terms need to be evaluated** to produce the similarity scores and thus the top-k ranking relevant documents.

## Query & Document Pre-Processing



Pre-processing happens within the [VSMTokenizer](/vsm/vsm_tokenizer.py) class. It consists of the following steps:

+ Normalize accented (unicode) characters
+ [Expand contractions](#expand-contractions)
+ ...
+ Convert case

### Expand Contractions

After some initial research, two options presented themselves:
- Naïve contraction expansion, by following [this article](https://www.kdnuggets.com/2018/08/practitioners-guide-processing-understanding-text-2.html)
- Smart contraction expansion, by using [the pycontractions module](https://pypi.org/project/pycontractions/)

The naïve approach make use of simple regex substitutions, mapping each contraction to exactly one expanded form. This ensures a more speedy, though naïve expansion process.

The smart approach applies a three pass approach, that possibly considers multiple viable expanded strings for every single contraction. This provides a more correct result, at the cost of speed.

For the initial implementation of the pre-processing, and until we specify otherwise, w**e will make use of the naïve method**. We have several reasons for this.
+ Many other steps must be performed for a single fact-check, so processing speed is important.
+ Many of the words produced by expanding contractions are stopwords, which will be removed in a following pre-processing step.
+ Many of the words produced by expanding contractions are common words, so their impact on the final score is relatively low.
For these reasons, less accurate expansions are acceptable.

### Numbers to Words

We want to minimize the impact of numbers on the dimensionality of the vocabulary. This is because numbers represent an explosion of possible terms. To reduce them to a normalized for, we convert them from numeric representation to word representation. For example, '102' gets converted to 'one hundred two'.

We apply the [inflect module](https://pypi.org/project/inflect/) to enable this conversion step.

We take some liberties during this conversion:
+ All connectors between the converted words are removed
  - NOT "twenty-three", BUT "twenty three"
  - NOT "one thousand, two hundred and two", but "one thousand two hundred two"
  - So '-', ',' and 'and' are pruned from the output words