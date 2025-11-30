# src/main.py

import pandas as pd
from cleaning import clean_movies_dataset
from analysis import create_features
from plotting import (
    plot_budget_vs_revenue,
    plot_avg_profit_year,
    plot_genre_revenue,
    plot_vote_vs_revenue,
    plot_correlation_heatmap,
    plot_roi_distribution,
    plot_top20_movies,
)

#  Load dataset

movies = pd.read_csv("data/movies_metadata.csv", low_memory=False)
print("Dataset loaded:", movies.shape)

#  Clean data

movies = clean_movies_dataset(movies)
print("Dataset cleaned:", movies.shape)


#  Creating Features

movies = create_features(movies)
print("Features created.")


#  Visualizations

plot_budget_vs_revenue(movies)
plot_avg_profit_year(movies)
plot_genre_revenue(movies)
plot_vote_vs_revenue(movies)
plot_correlation_heatmap(movies)
plot_roi_distribution(movies)
plot_top20_movies(movies)

# Save final dataset

movies.to_csv("data/movies_clean.csv", index=False)
print("Saved cleaned dataset at data/movies_clean.csv")
