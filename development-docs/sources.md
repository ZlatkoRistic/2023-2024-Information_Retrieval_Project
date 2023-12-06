# Introduction

This document pertains to useful sources to develop the project.

# Sources

This section mentions a list of useful sources.

## Online Sources

Many online sources provide useful information, though care needs to be taken to avoid incorrect information.

* Automated fact-checking: ["Fully Automated Fact-checking" presentation](https://youtu.be/7sH1tWlpiWA?t=496)
* Semi-automated fact-checking: ["Automated Fact Checking Talk @ Global Fact 7" presentation](https://youtu.be/lD4tKm8qsLs?t=1859)


## Course ppts

The powerpoint presentations provided for this course are also useful. This section wil contain brief summaries of important topics found in them.

### 01 Boolean Search

Summary:

* **slide 3**: Term-document incidence matrix
  * Too much redundant information --> need a more sparse solution
* **slide 4**: Resolving Boolean Query
* **slide 5**: Inverted term index
* **slide 7**: Resolving Boolean Query v2
* **slides 10 - 12**: Phrase Queries
  * k-grams *(rarely used)*
  * positional index: *(fairly powerful)*
* **slides 13 - 19**: Wildcard queries
  * permuterm index: *(only 1 wildcard per word + large space requirements)*
  * k-gram index
* **slide 20 - 25**: Spell Correction
  * Two principal uses
    * Correcting documents being indexed
    * Correcting user queries
  * Two methods
    * Isolated word spelling correction
    * Context-sensitive spelling correction

### 02 Ranked Retrieval

**The Document Ranking Problem**: Ranked retrieval setup: given a collection of documents, the user
issues a query, and an ordered list of documents is returned

**Important keywords**: Boolean Retrieval, Ranked Retrieval, Term Frequency (**tf**), Document Frequency (**df**), Log frequency weighting, Inverse Document Frequency weighting (**idf**), **tf-idf** weighting, Cosine Similarity, Ad-hoc Vector-Space Model (**VSM**), Theory-based probabilistic model, Binary Independence Model (**BIM**), Retrieval Status Value (**RSV**, $RSV_d$), **Okapi BM25**: A Nonbinary Model, Language-based models, Mixture Model: document vs collection frequencies and smoothing plus balancing $\lambda$

* (**TF**) $tf_{t,d}$ is the **term frequency** of term $t$ in document $d$
* $\bold{w_{t,d}}$ is the (log frequency) weight of term $t$ in document $d$
* (**IDF**) $d_t$ is the document frequency, the amount of documents $d$ a term $t$ appears in == inverse measure of informativeness of term $t$ &rarr; greater $d_t$ == greater informativeness

Summary:

* **slides 2 - 4**: Boolean Retrieval/Search == Feast or Famine
  * Ranked Retrieval displays most relevant results first
* **slide 5**: Ranked Retrieval
 * high term frequency in document == more relevant document (+ normalize freq. because large docs naturally contain higher freqs)
 * terms found in few docs are important (low global freq)
* **slide 6**: three **Ranked Retrieval** approaches
  * Ad-hoc Vector-Space Model
  * Theory-based probabilistic model
    * Boolean Independence Model BM-25
  * Language-based models
* **slides 7 - 9**: term frequenct (**tf**)
* **slides 10 - 20**: weighting functions
  * Document relevance does not increase proportionally with term frequency.
  * **log frequency weighting**
    * Given query $q$ consisting of terms $t$ and a document $d$
    * $\text{tf-matching-score}(q, d) = \sum_{t \in q ∩ d} (1 + \log \text{tf}_{t,d} )$
  * **$idf_t$ weight**: informativeness document frequency for term $t$ weight? **Inverse Document Frequency weighting**
    * Given $df_t$ and $N$ the number of documents in the collection
    * $idf_t = \log_{10} \dfrac{N}{df_t}$
    * $P(e)$ == probability that event $e$ occurs
      * if $P(t)$, the prob. that term $t$ occurs in a document, is small, then the event is meaningful &rarr; rare terms are meaningful/informative
    * **tf-idf weighting**: Combines tf and idf to give a general weighting for a term $t$ within a collection of documents $d$
    * $w_{t,d} = (1 + \log_{10} tf_{t, d}) \cdot \log \dfrac{N}{df_t} = \text{tf-weight} \cdot \text{idf-weight}$
    * <span style='color:red'>slide 16 - 17</span>: normalization/generalization of of terms $t$ in a collection
      * {Information, information, informations} ==> {informa}
      * reduced complexity
      * better hit-rate (recall?)?
* **slides 21 - 22**: **Documents and Queries as vectors of (tf-idf) weights**
* **slides 23 - 28**: Comparing docs vs queries using **Cosine Similarity**
* **slides 29 - 34**: Example and final **tf-idf Weighting and Scoring** ==> **SMART**
* **slides 35 - 38**: Vector Space Models (VSM) -- <span style="color:red">Query processing and Take-Aways<span>
* **slides 39 - 41**: **Probabilistic Ranked Retrieval Models**
  * **binary notion of relevance**: $R_{d,q}$ is a random dichotomous variable, such that
    * $R_{d,q} = 1$ if document $d$ is relevant w.r.t query $q$
    * $R_{d,q} = 0$ otherwise
  * Probabilistic ranking orders documents decreasingly by their
* **slides 41 - 50**: **Probabilistic Ranked Retrieval Models**
estimated probability of relevance w.r.t. query $q$: $P(R = 1|d, q)$
  * **Binary Independence Model (BIM)**
    * **Binary**: docs and queries == binary incidence (membership) vectors
      * $d$ represented by vector $x = (x_1, x_2, \dots, x_M)$ where $x_t = 1$ if term $t$ occurs in $d$, else $x_t = 0$
    * **Independence**
      * no association between terms (not true, but practically works - ‘naive’ assumption of Naive Bayes models)
    * $P(R|d,q)$ is modelled using term incidence vectors as $P(R | \overset{\rightarrow}{x}, \overset{\rightarrow}{q})$ where $\overset{\rightarrow}{x}$ is the document term incidence vector and $\overset{\rightarrow}{q}$ the query term incidence vector
    * <span style='color:red'>slide 44</span> **Conditional Independence Assumption**
      * presence or absence of a word in a doc is independent of the presence or absence of any other word (given the query)
    * **slide 45**: shorthands
      * $p_t = P(x_t = 1 | R = 1, \overset{\rightarrow}{q})$ == prob that term $t$ is present in a relevant document $d$, given the query vector
      * $u_t = P(x_t = 1 | R = 0, \overset{\rightarrow}{q})$ == prob that term $t$ is present in a *non*-relevant document $d$, given the query vector
    * <span style='color:red'>slide 46</span> second simplifying assumption for $q_t = 0, p_t=u_t$
      * Presence/absence of term does not matter if term not in query
      * **use of inverted indices IMPOSSIBLE** for BIM
    * calculates **Retrieval Status Value** (RSV)
    * Still need to **estimate** $u_t$ and $p_t$
* **slide 51**: VSM vs BIM
  * Large similarities: you build an information retrieval scheme in the exact same way
  * Major difference: scoring method at the end: cosine sim. + tf-idf in vector space VS probability
* **slides 52 - 53**: Okapi BM25: A Nonbinary Model
* **slides 55 - 57**: **Language-based models**
  * Our basic model: each document was generated by a different
deterministic finite state automaton (**DFSA**) except that these automata are probabilistic
* **slide 58**: **Using language models in IR**
  * Each document is treated as (the basis for) a language model
  * Rank (**score function**??) documents based on: $P(d | q) = \dfrac{P(d | q) P(d)}{P(q)}$
  * Ranking by $P(d|q)$ or $P(q|d)$ is equivalent
* **slide 59**: compute $P(q|d)$
  * Computation makes use of **Multinomial model** (omitting constant factor)
  * Uses the probabilistic model $M_d$ for document $d$
* **slide 60**: Parameter Estimation &rarr; determine $P(t, M_d)$ for term $t$ and model $M_d$ of doc $d$
  * max likelihood estimation: $\hat{P}(t | M_d) = \dfrac{tf_{t,d}}{|d|}$ where $|d|$ is the length of doc $d$ (nr of tokens/terms??)
  * <span style="color:red">Edge case</span>: $P(t | M_d) = 0$ would bring product to $0$
* **slide 61**: **Smoothing** &rarr; avoid prev edge case
  * $M_c$ is the collection language model
  * $cf_t$ is the collection term frequency of term $t$ (total nr of appearances of $t$ in collection of docs $d$)
  * $T = \sum_t cf_t$ is the total number of tokens/terms in the **collection**
  * **$\hat{P}(t | M_c) = \dfrac{cf_t}{T}$ smooths $P(t | d)$ away from $0$**
* **slides 62 - 66**: Mixture model, includes $M_d$ and $M_c$, with a scaling factor $\lambda$ to balance the two sides
* **slides 67 - 68** **LM vs VSM**
  * LMs vs. vector space model: *commonalities*
    * Term frequency (**tf**) is directly in the model.
    * Probabilities are inherently “**length-normalized**” (similar to cosine similarity).
    * Mixing document and collection frequencies has an effect similar to **idf**.
  * LMs vs. vector space model: *differences*
    * LMs: based on probability theory
    * Vector space: based on similarity, a geometric/ linear algebra notion
    * **Collection frequency vs. document frequency**
    * **Details** of term frequency, length normalization etc.
* **slide 69**: Language models for IR: Assumptions
* **slide 70**: Summary
  * 3 ways of **scoring query-document pairs**
    * Vector space model
    * Probabilistic models
    * Language-based models
  * Many commonalities between the models
    * Term frequency, document frequency, and length normalization
  * Often many choices to make and **parameters to tune**
    * Can use **grid search, machine learning to optimize parameters given test collection**