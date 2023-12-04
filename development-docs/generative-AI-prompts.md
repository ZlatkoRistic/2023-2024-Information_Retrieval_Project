# Introduction

This document details prompts that were submitted to generative AI models, to gather information and do research on the fact checking topic within information retrieval.

Table of models:
- [Phind section](#phind), its [url](https://www.phind.com/)
- [ChatGPT 3.5 section](#chatgpt-35), its [url](https://chat.openai.com/)


## Phind

The phind model was tailored to answer technical (IT) and scientific questions.

- [Q1: Multiple Textual Evidence](#q1-multiple-textual-evidence)
- [Q2: Viable Approach](#q2-viable-approach)
- [Q3: Quality Evaluation](#q3-quality-evaluation)
- [Q4: Course Topics](#q4-course-topics)
- [Q5: Ranked Retrieval functions](#q5-ranked-retrieval-functions)


## And a table of contents

### Q1: Multiple Textual Evidence

```
"The system should verify a claim using multiple textual evidence from a corpora eg. Google news corpora or Wikipedia."

In the above statement, in the context of a automated fact verification system, what does "multiple textual evidence" mean?
```

In the context of an automated fact verification system, "multiple textual evidence" refers to multiple pieces of information or data that are used to verify the truthfulness of a claim. This information is usually sourced from a corpus, such as Google News or Wikipedia, and is presented in the form of text.

The system uses Natural Language Processing (NLP) techniques to extract relevant information from these textual sources and use it as evidence to verify the claim. The evidence can come in various forms, such as direct quotes, paraphrased statements, or factual assertions that are related to the claim [Source 1](https://www.mdpi.com/2076-3417/13/23/12608).

For instance, if the claim is "The Earth revolves around the Sun", the system might find multiple pieces of evidence in the form of text from various sources that confirm this fact. These pieces of evidence could include scientific articles, educational content, or reliable news reports that discuss the heliocentric model of the solar system.

The process of extracting and using this evidence is often complex and involves several steps:

1. **Information Retrieval**: The system first needs to retrieve relevant pieces of evidence from the corpus. This can be done using various techniques, such as keyword matching, semantic search, or more advanced methods like machine learning models [Source 1](https://www.mdpi.com/2076-3417/13/23/12608).

2. **Fact Extraction**: Once the relevant documents are retrieved, the system needs to extract the specific pieces of evidence that are relevant to the claim. This can be done using techniques like Named Entity Recognition (NER), Relation Extraction, or other NLP techniques [Source 1](https://www.mdpi.com/2076-3417/13/23/12608).

3. **Evidence Verification**: After the evidence is extracted, the system needs to determine whether the evidence supports, refutes, or provides insufficient information about the claim. This can be done using various methods, such as pattern matching, machine learning models, or even more advanced techniques like logical reasoning [Source 1](https://www.mdpi.com/2076-3417/13/23/12608).

In conclusion, "multiple textual evidence" in the context of an automated fact verification system refers to multiple pieces of information or data that are used to verify the truthfulness of a claim. This process involves complex steps like information retrieval, fact extraction, and evidence verification.

### Q2: Viable Approach

```
What kind of approach to a fact verification system using multiple textual evidence is able to yield not only the truth/falsehood verdict, but also the documents or evidence that supports this verdict from the multiple corpora?
```

A fact verification system that can yield not only the truth/falsehood verdict but also the supporting documents or evidence from multiple corpora typically employs a combination of Information Retrieval (IR), Natural Language Processing (NLP), and Machine Learning (ML) techniques. Here's a step-by-step approach:

1. **Information Retrieval (IR)**: The system first retrieves relevant documents or passages from the corpora (like Google News or Wikipedia) that might contain evidence related to the claim. This can be done using techniques like Boolean model, Probabilistic model, or more advanced methods like BM25 or PageRank [Source 1](https://www.sciencedirect.com/science/article/pii/S1877050919301593).

2. **Fact Extraction**: After retrieving the relevant documents, the system extracts the specific pieces of evidence that are relevant to the claim. This can be done using Named Entity Recognition (NER), Relation Extraction, or other NLP techniques. The extracted pieces of evidence are then associated with the retrieved documents [Source 2](https://www.mdpi.com/2076-3417/13/23/12608).

3. **Claim Verification**: The system then uses Machine Learning models to determine whether the extracted evidence supports, refutes, or provides insufficient information about the claim. This involves training a model on a dataset of claims and their verdicts, and then using this trained model to predict the verdict for new claims [Source 3](https://www.sciencedirect.com/science/article/pii/S1877050919301593).

4. **Evidence Presentation**: After determining the verdict, the system presents the supporting documents or evidence that led to this verdict. This involves keeping track of which pieces of evidence were associated with which documents during the fact extraction step, and then retrieving these documents when presenting the verdict [Source 2](https://www.mdpi.com/2076-3417/13/23/12608).

This approach allows the system to not only determine the truth or falsehood of a claim, but also to provide the user with the evidence that led to this verdict. It's important to note that the effectiveness of this approach largely depends on the quality of the IR and NLP techniques used, as well as the training of the Machine Learning model.

## Q3: Quality Evaluation

```
How do you measure the quality of the IR and NLP techniques used in a fact verification system?
```

The quality of Information Retrieval (IR) and Natural Language Processing (NLP) techniques used in a fact verification system can be evaluated using several metrics:

1. **Precision**: Precision measures the proportion of retrieved documents that are relevant to the user's query. In the context of a fact verification system, this could be the proportion of retrieved documents that contain evidence supporting the claim [Source 0](https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-in-information-retrieval-1.html).

2. **Recall**: Recall measures the proportion of relevant documents that were retrieved. In the context of a fact verification system, this could be the proportion of documents that contain evidence supporting the claim that were actually retrieved by the system [Source 0](https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-in-information-retrieval-1.html).

3. **F1 Score**: The F1 score is the harmonic mean of precision and recall. It provides a single metric that balances the need for precision and recall, making it a useful measure for evaluating the performance of a fact verification system [Source 0](https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-in-information-retrieval-1.html).

4. **User Satisfaction**: User satisfaction is another important metric for evaluating the quality of a fact verification system. This can be measured by asking users to rate the quality of the retrieved evidence and the overall user experience. It's important to note that user satisfaction can be influenced by factors other than the quality of the retrieved evidence, such as the speed of response and the layout of the user interface [Source 0](https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-in-information-retrieval-1.html).

5. **Benchmarking**: Benchmarking against established datasets and models can also be a useful way to evaluate the quality of an IR or NLP technique. For example, the KILT benchmark can be used to evaluate the performance of a fact verification system [Source 1](https://paperswithcode.com/task/fact-verification).

It's important to note that the choice of evaluation metric depends on the specific goals and constraints of the fact verification system. Different metrics may be more or less appropriate depending on the context. For example, if the goal is to maximize user satisfaction, then user satisfaction might be the most important metric. On the other hand, if the goal is to maximize the proportion of relevant documents that are retrieved, then recall might be the most important metric.


### Q4: Course Topics

```
In the context of the previous queries, what are the definitions and the significance/uses of the following techniques?
* Boolean search
* Ranked retrieval models
* Feedback Expansion and Evaluation
* Dimensionality reduction
```

1. **Boolean Search**: Boolean search is a technique used in information retrieval to find documents that match a certain query. It uses Boolean logic (AND, OR, NOT) to combine search terms and operators to find relevant documents. Boolean search is simple and efficient, and it's easy for users to understand why a particular document matches or doesn't match a query. However, it can be less effective than ranked retrieval in ad hoc retrieval because it doesn't consider the relevance of the documents. In the context of a fact verification system, Boolean search can be used to quickly narrow down the search space and retrieve a list of potential documents that might contain evidence supporting the claim [Source 1](https://bmcmedinformdecismak.biomedcentral.com/articles/10.1186/1472-6947-10-58).

2. **Ranked Retrieval Models**: Ranked retrieval models are techniques used in information retrieval to order the documents that match a query based on their relevance. They are more complex than Boolean search, but they can provide a more relevant and useful result set. Ranked retrieval models use various ranking functions to calculate a score for each document, and then sort the documents based on these scores. In the context of a fact verification system, ranked retrieval models can be used to order the potential documents based on their relevance to the claim [Source 1](https://bmcmedinformdecismak.biomedcentral.com/articles/10.1186/1472-6947-10-58).

3. **Feedback Expansion and Evaluation**: Feedback expansion is a technique used in information retrieval to refine the search space based on user feedback. It involves expanding the search space to include documents that are similar to the documents that were retrieved by the initial query. Feedback expansion can help to improve the relevance of the retrieved documents and reduce the number of non-relevant documents that need to be examined. In the context of a fact verification system, feedback expansion can be used to refine the search space based on the feedback from the users or the system's own evaluation of the retrieved documents [Source 1](https://bmcmedinformdecismak.biomedcentral.com/articles/10.1186/1472-6947-10-58).

4. **Dimensionality Reduction**: Dimensionality reduction is a technique used in data analysis to reduce the number of features in a dataset while preserving the essential information. In the context of a fact verification system, dimensionality reduction can be used to reduce the number of features in the data (e.g., the number of words in a document) while preserving the essential information (e.g., the relevance of the document to the claim). This can make the data easier to process and can help to improve the performance of the fact verification system. Dimensionality reduction techniques include Principal Component Analysis (PCA), t-distributed Stochastic Neighbor Embedding (t-SNE), and Singular Value Decomposition (SVD) [Source 1](https://bmcmedinformdecismak.biomedcentral.com/articles/10.1186/1472-6947-10-58).

### Q5: Ranked Retrieval functions

```
What are some common ranking functions used in ranked retrieval models?
```

Ranked retrieval models use various ranking functions to order the documents that match a query based on their relevance. Here are some common ranking functions used in these models:

1. **Vector Space Model**: This model represents documents and queries as vectors in a high-dimensional space. The similarity between a document and a query is calculated using a measure such as cosine similarity. Documents are then ranked based on their similarity scores. The Vector Space Model uses techniques like Term Frequency-Inverse Document Frequency (TF-IDF) to assign weights to terms in the documents and queries [Source 0](https://en.wikipedia.org/wiki/Ranking_(information_retrieval)).

2. **PageRank Algorithm**: The PageRank algorithm is a link analysis algorithm that assigns a numerical weighting to each element of a hyperlinked set of documents, such as the World Wide Web, with the purpose of "measuring" its relative importance within the set. It is a key part of Google’s method of ranking web pages in search results. The PageRank value for a page is dependent on the PageRank values for each page contained in the set of pages linking to it, divided by the amount of links from each page [Source 0](https://en.wikipedia.org/wiki/Ranking_(information_retrieval)).

3. **HITS Algorithm**: Similar to PageRank, HITS uses Link Analysis for analyzing the relevance of the pages but only works on small sets of subgraph (rather than the entire web graph) and is query dependent. The subgraphs are ranked according to weights in hubs and authorities where pages that rank highest are fetched and displayed [Source 0](https://en.wikipedia.org/wiki/Ranking_(information_retrieval)).

4. **Learning to Rank**: This is a machine learning approach to the ranking problem. It involves training a model on a dataset of queries and their associated documents, and then using this model to predict the ranking of a new query. Learning to rank models can be very effective, but they require a large amount of data and computational resources to train [Source 0](https://en.wikipedia.org/wiki/Ranking_(information_retrieval)).

These ranking functions are evaluated by a variety of means; one of the simplest is determining the precision of the first k top-ranked results for some fixed k; for example, the proportion of the top 10 results that are relevant, on average over many queries [Source 0](https://en.wikipedia.org/wiki/Ranking_(information_retrieval)).



## ChatGPT 3.5

ChatGPT is a more general generative model.

- [Q1: Multiple Textual Evidence](#q1-multiple-textual-evidence-1)


### Q1: Multiple Textual Evidence

```
"The system should verify a claim using multiple textual evidence from a corpora eg. Google news corpora or Wikipedia."

In the above statement, in the context of a automated fact verification system, what does "multiple textual evidence" mean?
```

In the context of an automated fact verification system, "multiple textual evidence" refers to the use of more than one source or piece of text to support or refute a particular claim. Instead of relying on a single source, the system is designed to gather and analyze information from various texts within a corpus (such as Google News or Wikipedia) to cross-reference and validate the accuracy of a given claim.

This approach aims to enhance the reliability of the fact-checking process by considering information from diverse perspectives and sources. By using multiple textual evidence, the system can potentially identify inconsistencies, contradictions, or patterns across different documents, leading to a more comprehensive and accurate evaluation of the claim in question.



