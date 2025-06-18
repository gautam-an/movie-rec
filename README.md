# Movie Recommendation Engine

This is a lightweight movie recommendation system that uses **Pinecone vector search** and **sentence-transformers** to suggest similar movies based on either a movie title or a plot summary.

## Dataset

This project is built on the [CMU Movie Summary Corpus](https://www.cs.cmu.edu/~ark/personas/), a dataset compiled by researchers at the Language Technologies Institute and Machine Learning Department at Carnegie Mellon University.

The dataset contains over **42,000** movie plot summaries extracted from Wikipedia, along with structured metadata from Freebase, including:

- Movie genres, box office revenue, release dates, runtime, and language
- Character names, actor identities, actor age at release, gender, and height
- Optional: Preprocessed plot summaries with Stanford CoreNLP (NER, coref, parsing, etc.)

All data is released under a Creative Commons Attribution-ShareAlike License.

## Key Files

- ## engine/seed.py
This script reads the `processed_movie_data.csv` file and creates vector embeddings for each movie plot using the sentence-transformers/all-MiniLM-L6-v2 model. Each embedding is stored in Pinecone under the index `all-minilm-16-v2-384-dims` and namespace `movies1`.
> link for the embedding model: [huggingface.co](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)

- ## `engine/rec.py`
The main interaction file. Users can input a movie title or a custom plot and receive top 5 recommendations based on cosine similarity in vector space. Includes an option to view plot summaries of recommended movies.

- ## `utils/fetch.py`
  This utility script retrieves plot summaries and Wikipedia-based metadata for movies using their internal wiki ID. It performs simple title-to-ID lookup and can request movie names    via Wikipedia's public API.

## Limitations

- This system includes movies from all time periods. There is currently no filter by decade, language, or genre.
- The system can be slow on first execution due to the size of the dataset (~42,000 movies).
- You must have a valid Pinecone API key and access to the correct index to use this. Without that, vector search will fail.
- Some titles in the dataset may be duplicated or differently formatted, and not all user-input queries may yield results if the match is imprecise.
- The system does not deduplicate very similar entries in Pinecone, so near-duplicates may appear in recommendations.
