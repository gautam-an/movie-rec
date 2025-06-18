import requests
import pandas as pd

df = pd.read_csv('data/movie.metadata.tsv', sep='\t', header=None)
df = df[[0, 2]]
df.columns = ['wiki_id', 'movie_name']

def get_plot_summary(wiki_id_to_find, filepath='data/plot_summaries.txt'):
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            wiki_id, plot = line.strip().split('\t', 1)
            if wiki_id == str(wiki_id_to_find):
                return plot
    return None

def get_name(wiki_id):
    url = f"https://en.wikipedia.org/w/api.php?action=query&pageids={wiki_id}&format=json"
    response = requests.get(url)
    data = response.json()
    movie_name = data['query']['pages'][str(wiki_id)]['title']
    return movie_name

def find_wiki_id_by_title(title):
    match = df[df['movie_name'].str.lower() == title.lower()]
    if not match.empty:
        return match.iloc[0]['wiki_id']
    return None

if __name__ == "__main__":
    title_input = input("Enter movie title: ").strip()
    wiki_id = find_wiki_id_by_title(title_input)

    if wiki_id is None:
        print(f"Movie '{title_input}' not found in metadata.")
    else:
        name = get_name(wiki_id)
        print(f"Wikipedia ID: {wiki_id}")
        print(f"Movie name: {name}")
        plot = get_plot_summary(wiki_id)
        if plot:
            print(f"Plot summary:\n{plot}")
        else:
            print("Plot summary not found.")
