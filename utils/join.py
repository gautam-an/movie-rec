import pandas as pd

metadata = pd.read_csv('data/movie.metadata.tsv', sep='\t', header=None, usecols=[0, 2], names=['wiki_id', 'movie_name'])

metadata['wiki_id'] = metadata['wiki_id'].astype(str)

plot_dict = {}
with open('data/plot_summaries.txt', 'r', encoding='utf-8') as f:
    for line in f:
        wiki_id, plot = line.strip().split('\t', 1)
        plot_dict[wiki_id] = plot
        
plot_df = pd.DataFrame(list(plot_dict.items()), columns=['wiki_id', 'plot_summary'])

df = pd.merge(metadata, plot_df, on='wiki_id', how='inner')
df.to_csv('data/processed_movie_data.csv', index=False)

print(df.head())
