import csv
import time
import hashlib
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

API_KEY = "pcsk_vajkE_973hVdKMVwgN5XU83ZBZvr8SUGGTmhW8qk9Ew3zGozSkNfiM2r4tssfaFD6L8Ka"  
INDEX_NAME = "all-minilm-16-v2-384-dims"
NAMESPACE = 'movies1'

pc = Pinecone(api_key=API_KEY)
index = pc.Index(INDEX_NAME)
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

csv_path = "data/processed_movie_data.csv"

with open(csv_path, newline='', encoding='utf-8') as kb_file:
    csvreader = csv.reader(kb_file)
    header = next(csvreader)  
    print("CSV Header:", header)    

    for row in csvreader:
        if len(row) < 3: # missing data
            continue  

        wiki_id = row[0]
        title = row[1]
        plot_summary = row[2]

        print(f"Processing: {title}")
        embedding = model.encode(plot_summary).tolist()
        vector_id = hashlib.sha1(wiki_id.encode('utf-8')).hexdigest()

        index.upsert(
            vectors=[
                {
                    "id": vector_id,
                    "values": embedding,
                    "metadata": {
                        "title": title,
                        "description": plot_summary,
                        "created_at": int(time.time())
                    }
                }
            ],
            namespace=NAMESPACE
        )
