# src/plotting.py

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

sns.set(style="whitegrid")


def plot_budget_vs_revenue(df):
    plt.figure(figsize=(10,6))
    sns.scatterplot(data=df, x="budget", y="revenue", alpha=0.5)
    plt.xscale("log")
    plt.yscale("log")
    plt.title("Budget vs Revenue (log-log scale)")
    plt.savefig("outputs/figures/budget_vs_revenue.png")
    plt.show()


def plot_avg_profit_year(df):
    profit_year = df.groupby("release_year")["profit"].mean()
    plt.figure(figsize=(12,6))
    profit_year.plot()
    plt.title("Average Profit per Year")
    plt.xlabel("Year")
    plt.ylabel("Avg Profit")
    plt.savefig("outputs/figures/profit_per_year.png")
    plt.show()


def plot_genre_revenue(df):
    genres = df.explode("genre_names")
    top = genres.groupby("genre_names")["revenue"].mean().sort_values(ascending=False).head(10)

    plt.figure(figsize=(12,6))
    sns.barplot(y=top.index, x=top.values)
    plt.xlabel("Average Revenue")
    plt.ylabel("Genre")
    plt.title("Top 10 Genres by Average Revenue")
    plt.savefig("outputs/figures/top_genre_revenue.png")
    plt.show()


def plot_vote_vs_revenue(df):
    plt.figure(figsize=(10,6))
    sns.scatterplot(data=df, x="vote_average", y="revenue", alpha=0.5)
    plt.yscale("log")
    plt.title("Vote Average vs Revenue")
    plt.savefig("outputs/figures/vote_vs_revenue.png")
    plt.show()


def plot_correlation_heatmap(df):
    corr = df[["budget", "revenue", "profit", "roi", "vote_average", "vote_count", "popularity"]].corr()
    plt.figure(figsize=(12,8))
    sns.heatmap(corr, annot=True, cmap="coolwarm")
    plt.title("Correlation Heatmap")
    plt.savefig("outputs/figures/correlation_heatmap.png")
    plt.show()


def plot_roi_distribution(df):
    plt.figure(figsize=(10,6))

    # Cap ROI at the 95th percentile (for better visualisation)
    cap = np.percentile(df["roi"], 95)
    capped_roi = df["roi"].clip(upper=cap)

    sns.histplot(capped_roi, bins=50)
    plt.title("ROI Distribution (Capped at 95th percentile)")
    plt.xlabel("ROI")
    plt.savefig("outputs/figures/roi_distribution.png")
    plt.show()


def plot_top20_movies(df):
    top = df.sort_values("revenue", ascending=False).head(20)
    plt.figure(figsize=(12,8))
    sns.barplot(y=top["title"], x=top["revenue"])
    plt.title("Top 20 Highest Grossing Movies")
    plt.savefig("outputs/figures/top20_movies.png")
    plt.show()
