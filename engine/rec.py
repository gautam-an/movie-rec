import csv
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from utils.fetch import get_plot_summary, find_wiki_id_by_title

API_KEY = "YOUR_PINECONE_API_KEY" 
INDEX_NAME = "all-minilm-16-v2-384-dims"
NAMESPACE = "movies1"
CSV_PATH = "data/processed_movie_data.csv"

pc = Pinecone(api_key=API_KEY)
index = pc.Index(INDEX_NAME)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

movie_data = {}
with open(CSV_PATH, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        if len(row) < 3:
            continue
        wiki_id, title, plot = row
        movie_data[title.lower()] = plot

def recommend_by_title(title, top_k=5):
    plot = movie_data.get(title.lower())
    if not plot:
        return f"movie '{title}' not found in dataset."

    embedding = model.encode(plot).tolist()
    return query_pinecone(embedding, exclude_title=title, top_k=top_k)

def recommend_by_plot(custom_plot, top_k=5):
    embedding = model.encode(custom_plot).tolist()
    return query_pinecone(embedding, top_k=top_k)

def query_pinecone(embedding, exclude_title=None, top_k=5):
    response = index.query(
        vector=embedding,
        top_k=top_k + 1,
        namespace=NAMESPACE,
        include_metadata=True
    )

    results = []
    for match in response['matches']:
        title = match['metadata']['title']
        if exclude_title and title.lower() == exclude_title.lower():
            continue
        results.append((title, match['score']))
        if len(results) == top_k:
            break
    return results

if __name__ == "__main__":
    print("Movie Recommendation System:")
    mode = input("Choose mode — type 'title' or 'plot': ").strip().lower()

    if mode == "title":
        title = input("Enter the movie title: ")
        recs = recommend_by_title(title)
    elif mode == "plot":
        plot = input("Paste or write your movie plot: ")
        recs = recommend_by_plot(plot)
    else:
        print("invalid mode")
        exit()

    print("\nRecommendations:")
    if isinstance(recs, str):
        print(recs)
    else:
        for i, (title, score) in enumerate(recs, 1):
            print(f"{i}. {title} (Similarity: {score * 100:.2f}%)")
    
    print("\n")
    print("Would you like to see the plot summary of any of these movies? (y/n)")
    if input().strip().lower() == "y":
        print("Enter the number (1-5) of the movie:")
        choice = int(input().strip())
        chosen_title = recs[choice - 1][0]
        wiki_id = find_wiki_id_by_title(chosen_title)
        plot = get_plot_summary(wiki_id)
        print(f"Plot summary for '{chosen_title}':")
        print("\n")
        print(f"{plot}")
        print("\n")

    
