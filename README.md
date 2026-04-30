# COMP3011 Coursework 2 – Search Engine Tool

## Overview

This project implements a simplified search engine in Python that demonstrates the fundamental components of information retrieval systems including web crawling, indexing and query processing.

The system crawls the website:

https://quotes.toscrape.com/

and allows users to search for quotes using a command-line interface. It includes an inverted index with statistical information and uses TF-IDF ranking to improve search result relevance.

---

## Features

- Web crawler with a 6-second politeness delay  
- HTML parsing using BeautifulSoup  
- Inverted index containing:
  - Word frequency
  - Word positions  
- Case-insensitive search  
- TF-IDF ranking for improved relevance  
- Command-line interface (CLI)  
- Comprehensive automated test suite (95% coverage)  

---

## System Architecture

The system follows a modular pipeline similar to real-world search engines:

Crawler → Parser → Indexer → Search Engine

---

### 1. Crawler (crawler.py)

- Sends HTTP requests using the Requests library  
- Extracts quotes and authors from HTML pages  
- Follows pagination links to crawl all pages  
- Enforces a 6-second delay between requests to respect server load  

---

### 2. Indexer (indexer.py)

- Tokenises text using case-insensitive processing  
- Builds an inverted index with the following structure:

    {
      "word": {
        "doc_id": {
          "frequency": int,
          "positions": [int, ...]
        }
      }
    }

- Stores document metadata (URL and content)  
- Saves and loads the index as a JSON file  

---

### 3. Search Engine (search.py)

- Processes user queries  
- Identifies documents containing all query terms  
- Ranks results using TF-IDF  

#### TF-IDF Formula

TF-IDF is calculated as:

TF-IDF = TF × log((N + 1) / (df + 1)) + 1

Where:
- TF is the term frequency in the document  
- df is the number of documents containing the term  
- N is the total number of documents  

This approach improves ranking by giving higher weight to rare and meaningful terms.

---

### 4. Command-Line Interface (main.py)

The CLI supports the following commands:

- build – Crawl the website and build the index  
- load – Load a previously saved index  
- print <word> – Display index entry for a word  
- find <query> – Search for documents  
- exit – Terminate the program  

---

## Installation and Setup

### Clone the repository

git clone https://github.com/1alpakkor0/web-services-coursework2.git  
cd repository-name

### Install dependencies

pip install -r requirements.txt  

---

## Running the Application

python src/main.py  

Example usage:

> build  
> load  
> print love  
> find good friends  
> exit  

---

## Testing

Run all tests:

python -m pytest  

Run with coverage:

python -m pytest --cov=src tests/  

### Test Coverage

- Total coverage: 95%  
- Includes:
  - Unit tests  
  - Integration tests  
  - Performance tests  

---

## Design Rationale

### Inverted Index

An inverted index was used because it allows efficient retrieval of documents based on words. It is a standard structure used in search engines and enables fast query processing.

---

### Tokenisation

Tokenisation is implemented using regular expressions and converts all text to lowercase. This ensures consistency and supports case-insensitive search.

---

### TF-IDF Ranking

The initial approach used simple term frequency. This was improved by implementing TF-IDF to better rank documents by considering both term frequency and term rarity across the dataset.

---

### Data Storage

The index is stored in JSON format. This makes it easy to inspect, debug and load for future searches. It is suitable for the scale of this coursework.

---

## Performance Considerations

- Efficient dictionary-based data structures are used for indexing  
- Query processing uses set intersection for fast filtering  
- Performance tests validate the system’s scalability on larger datasets  

---

## Use of Generative AI

This project was developed with assistance from generative AI tools.

### Usage

- Understanding BeautifulSoup and web scraping techniques  
- Debugging Python errors  
- Improving test coverage and structure  
- Learning and implementing TF-IDF ranking
- Assisted to create the structure of the README file

### Critical Evaluation

Some AI-generated suggestions were inefficient or incorrect particularly for data structures and query handling. These required manual debugging and refinement.

AI was useful for accelerating development but full understanding of all code was necessary to ensure correctness and reliability.

---

## References

- COMP3011 Lecture Notes  
- Requests Documentation: https://docs.python-requests.org/  
- BeautifulSoup Documentation: https://www.crummy.com/software/BeautifulSoup/  

---

## Author

Alp Akkor  
University of Leeds  
COMP3011 – Web Services and Web Data