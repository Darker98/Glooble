# Glooble: A Revolutionary Article Search Engine

Welcome to **Glooble**, a revolutionary search engine designed for retrieving articles efficiently and effectively. This repository documents the architecture, implementation, and features of Glooble, which utilizes a dataset of over 190,000 Medium articles to provide fast and accurate search results.

## Table of Contents
- [Introduction](#introduction)
- [Languages Used and Reasoning](#languages-used-and-reasoning)
- [Dataset Used and Reasoning](#dataset-used-and-reasoning)
- [Data Structures Used](#data-structures-used)
  - [Lexicon](#lexicon)
  - [Forward Index](#forward-index)
  - [Inverted Index](#inverted-index)
  - [Barrels](#barrels)
- [Frontend](#frontend)
  - [Features](#features)
- [Backend](#backend)
  - [Preprocessing](#preprocessing)
  - [Inverted Index Lookup](#inverted-index-lookup)
  - [Content Mapper](#content-mapper)
  - [Ranking](#ranking)
- [Article Upload Backend](#article-upload-backend)
- [Frontend-Backend Integration](#frontend-backend-integration)
- [Other Optimizations and Features](#other-optimizations-and-features)

---

## Introduction
**GitHub Repository:** [Darker98/Glooble](https://github.com/Darker98/Glooble)

Glooble is a semi-large-scale article search engine that leverages advanced indexing techniques and ranking algorithms to provide users with relevant search results.

---

## Languages Used and Reasoning
### Frontend: React, TypeScript
- **Reasoning:**
  - Allows seamless integration with the Python backend using libraries like Flask.
  - Enables the creation of modern and visually appealing user interfaces.

### Backend: Python
- **Reasoning:**
  - Ease of development and extensive library support for rapid development.
  - Facilitates efficient I/O operations on disk.

---

## Dataset Used and Reasoning
- **Name:** 190k+ Medium Articles
- **Size:** Over 190,000 articles
- **Reasoning:**
  - Sufficient size to support the development of a semi-large-scale search engine.
  - Includes a URL field, simplifying the response structure for user queries.

---

## Data Structures Used
### Lexicon
- **Purpose:** Maps words to unique `wordID`s.
- **Format:**
  - `1 byte`: Length of the word
  - `N bytes`: Word
  - `4 bytes`: `wordID`

### Forward Index
- **Purpose:** Maps documents to `wordID`s and includes the context and frequency of each word.
- **Format:**
  - `8 bytes`: `docID`
  - `2 bytes`: Number of `wordID`s
  - For each `wordID`:
    - `4 bytes`: `wordID`
    - `1 byte`: Context flags (e.g., title, text, authors, tags)
    - `2 bytes`: Frequency in the document

### Inverted Index
- **Purpose:** Maps `wordID`s to the documents containing them, with context and frequency information.
- **Format:**
  - `4 bytes`: `wordID`
  - `4 bytes`: Number of `docID`s
  - For each `docID`:
    - `8 bytes`: `docID`
    - `1 byte`: Context flags
    - `2 bytes`: Frequency

### Barrels
- **Purpose:** Divide the inverted index into smaller chunks for efficient storage and retrieval.
- **Reasoning:** Average size of each barrel is ~10 MB for manageability.

---

## Frontend
### Features
- **Search Bar:** Input queries or upload files; results are dynamically displayed.
- **Search Results:** Each result includes title, snippet, tags, authors, and metadata.
- **Result Pagination:** Navigate through multiple pages of results.
- **File Upload:** Upload JSON files for processing; success/error messages are displayed.
- **Spelling Suggestions:** Query corrections with an option to use the original query.
- **Result Cards:** Visually styled cards displaying title, snippet, tags, authors, score, and publication date.

---

## Backend
### Preprocessing
- Converts queries into a searchable format.
- Steps:
  1. Tokenize using NLTK.
  2. Convert numbers to words; remove decimals.
  3. Split hyphenated words.
  4. Remove punctuation and capitalization.
  5. Normalize accented characters and remove non-ASCII characters.
  6. Lemmatize tokens using spaCy.
  7. Remove stop words using a custom list.
  8. Truncate words to 30 characters.

### Inverted Index Lookup
- **Optimization:** Constant-time lookup using an offsets file (`offsets.bin`).
- **Offset Format:**
  - `4 bytes`: `wordID`
  - `4 bytes`: Offset
- **Mechanism:** Hash table maps `wordID` to barrel offset, calculated as `wordID % number of barrels`.

### Content Mapper
- Maps `docID` to details like URL, title, authors, tags, and snippet.
- **Format:**
  - `2 bytes`: URL length
  - `N bytes`: URL
  - `2 bytes`: Title length
  - `N bytes`: Title
  - Additional bytes for tags, authors, and text.
- **Offsets File Format:**
  - `8 bytes`: `docID`
  - `8 bytes`: Offset

### Ranking
- **Purpose:** Sort documents by relevance to a query.
- **Formula:**
  
  ```
  TF(t, d) = f(t, d) / max(f(t', d))
  IDF(t) = log(N / (1 + df(t)))
  TF-IDFw(t, d) = TF(t, d) × IDF(t) × C(t, d)
  Score(q, d) = ∑ TF-IDFw(t, d)
  ```

- **Context Weights:**
  - Title + Tags: `C = 4`
  - Title: `C = 3`
  - Tags/Authors: `C = 2`
  - Text: `C = 1`

---

## Article Upload Backend
### Steps:
1. Extract data from JSON.
2. Preprocess and tokenize.
3. Calculate term frequencies and context flags.
4. Update lexicon and retrieve `wordID`.
5. Update barrels and offsets.
6. Add entries to the content mapper and frequency file.
7. Reflect changes in runtime variables.

---

## Frontend-Backend Integration
- **Framework:** Flask
- **Endpoints:**
  1. **Query Endpoint:** Accepts query, page number, and `use_original` flag; returns results.
  2. **Upload Article Endpoint:** Accepts JSON documents and updates the dataset.

---

## Other Optimizations and Features
- **Error Correction:** Uses TextBlob to suggest corrections for misspelled queries.
- **Pagination:** Fetches and returns only the relevant results for the requested page.
- **Threading:** Processes multi-word queries in parallel to improve response time.
- **Query Response Time:** Maintained under 30 ms for optimized performance.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contributing
Contributions are welcome! Please create an issue or submit a pull request.

---

## Acknowledgements
Special thanks to the creators of the libraries and frameworks used in this project, including React, Flask, NLTK, and spaCy.
