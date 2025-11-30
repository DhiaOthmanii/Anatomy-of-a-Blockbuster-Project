# dashboard/app.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import ast
import base64

# PAGE CONFIG
st.set_page_config(page_title="Blockbuster Anatomy", layout="wide")

# BACKGROUND IMAGE 
bg_file = "rustic-gray-concrete-textured-background.jpg"
with open(bg_file, "rb") as f:
    encoded = base64.b64encode(f.read()).decode()

st.markdown(
    f"""
    <style>
    .stApp {{
        background: url(data:image/jpg;base64,{encoded});
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    /* Make headings white for contrast */
    h1, h2, h3 {{
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
    }}

    /* Plot containers for readability on background */
    .plot-box {{
        background-color: rgba(255,255,255,0.9);
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 8px;
    }}

    /* Bigger, more readable interpretation boxes */
    .note-box {{
        background-color: rgba(255,255,255,0.92);
        padding: 16px 18px;
        border-radius: 10px;
        margin-top: 8px;
        margin-bottom: 28px;
        font-size: 18px;     /* bigger paragraph text */
        line-height: 1.75;   /* more readable spacing */
        color: #111;         /* strong contrast */
    }}

    .interp-title {{
        font-size: 20px;     /* bigger title */
        font-weight: 800;    /* bold */
        margin-bottom: 6px;
        display: block;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Movies Success Dashboard")

#  LOAD DATA 
df = pd.read_csv("../data/movies_clean.csv")

# Fix stringified genre list after CSV reload
df["genre_names"] = df["genre_names"].apply(
    lambda x: ast.literal_eval(x) if isinstance(x, str) else x
)

# Defensive drops to avoid crashes
df = df.dropna(subset=["budget", "revenue", "roi", "profit", "release_year"])

#  SIDEBAR FILTERS
st.sidebar.title("Filters")

min_year = int(df["release_year"].min())
max_year = int(df["release_year"].max())

year_range = st.sidebar.slider(
    "Select Release Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

all_genres = sorted({g for lst in df["genre_names"] for g in lst})
selected_genres = st.sidebar.multiselect(
    "Select Genres",
    options=all_genres,
    default=[]
)

# APPLY FILTERS 
filtered_df = df[
    (df["release_year"] >= year_range[0]) &
    (df["release_year"] <= year_range[1])
].copy()

if selected_genres:
    filtered_df = filtered_df[
        filtered_df["genre_names"].apply(
            lambda genre_list: any(g in genre_list for g in selected_genres)
        )
    ]

sns.set_style("whitegrid")

# Helper to show interpretation text consistently
def interpretation(text: str):
    st.markdown(
        f"""
        <div class='note-box'>
            <span class='interp-title'>Interpretation</span>
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )

# PLOTS 

# 1) Budget vs Revenue
st.header("Budget vs Revenue")
st.markdown("<div class='plot-box'>", unsafe_allow_html=True)
fig, ax = plt.subplots(figsize=(7, 4.5))
sns.scatterplot(data=filtered_df, x="budget", y="revenue", alpha=0.45, ax=ax)
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("Budget")
ax.set_ylabel("Revenue")
ax.set_title("Budget vs Revenue")
st.pyplot(fig)
st.markdown("</div>", unsafe_allow_html=True)

interpretation(
    "This plot shows the relationship between a movie’s budget and its box office revenue. "
    "Using a log–log scale lets us compare films across huge ranges of money, from low-budget titles "
    "to billion-dollar blockbusters. The points form an overall upward trend, meaning higher budgets "
    "usually lead to higher revenues. However, the spread is wide: many expensive movies earn only "
    "moderate returns, and some low-budget films perform extremely well. So budget is an important "
    "driver of revenue, but it is not a guarantee of success on its own."
)

# 2) ROI Distribution
st.header("ROI Distribution")
st.markdown("<div class='plot-box'>", unsafe_allow_html=True)
fig, ax = plt.subplots(figsize=(7, 4.5))
cap = np.percentile(filtered_df["roi"], 95)
capped_roi = filtered_df["roi"].clip(upper=cap)
sns.histplot(capped_roi, bins=50, ax=ax)
ax.set_xlabel("ROI")
ax.set_ylabel("Count")
ax.set_title("ROI Distribution")
st.pyplot(fig)
st.markdown("</div>", unsafe_allow_html=True)

interpretation(
    "Most movies have low to moderate ROI, meaning they return only a small multiple of their budget. "
    "The distribution is strongly right-skewed, showing that filmmaking is high risk: many films barely "
    "break even, while a small minority achieve very large returns. The final spike on the right appears "
    "because ROI values above the 95th percentile were capped, so all extreme outliers are grouped into "
    "the same bin to keep the plot readable."
)

# 3) Average Profit per Year
st.header("Average Profit per Year")
st.markdown("<div class='plot-box'>", unsafe_allow_html=True)
profit_year = filtered_df.groupby("release_year")["profit"].mean()
fig, ax = plt.subplots(figsize=(7, 4.5))
profit_year.plot(ax=ax)
ax.set_xlabel("Year")
ax.set_ylabel("Average Profit")
ax.set_title("Average Profit per Year")
st.pyplot(fig)
st.markdown("</div>", unsafe_allow_html=True)

interpretation(
    "This plot shows how the average profit (revenue − budget) of movies changes over time. "
    "The early part of the curve (before about 1950) is very unstable, with sharp spikes and drops, "
    "because the dataset contains relatively few films from those years, so a single successful or "
    "failed movie can heavily affect the average. From the mid-1900s onward, the trend becomes more "
    "consistent and generally rises, indicating that films have become more profitable on average "
    "over the decades. This long-term increase likely reflects the expansion of global box office "
    "markets, bigger production scales, and higher ticket prices over time. Overall, the plot suggests "
    "profitability has grown, but early-year values should be interpreted cautiously due to small sample effects."
)

# 4) Top 10 Genres by Average Revenue
st.header("Top 10 Genres by Average Revenue")
st.markdown("<div class='plot-box'>", unsafe_allow_html=True)
genres_long = filtered_df.explode("genre_names")
top_genres = (
    genres_long.groupby("genre_names")["revenue"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)
fig, ax = plt.subplots(figsize=(7, 4.5))
sns.barplot(y=top_genres.index, x=top_genres.values, ax=ax)
ax.set_xlabel("Average Revenue")
ax.set_ylabel("Genre")
ax.set_title("Top 10 Genres by Average Revenue")
st.pyplot(fig)
st.markdown("</div>", unsafe_allow_html=True)

interpretation(
    "This bar chart ranks the ten genres with the highest average box office revenue in the dataset. "
    "Animation, Adventure, Fantasy, and Family lead the list, which makes sense because these genres "
    "usually have broad global appeal, are easier to market internationally, and are often tied to "
    "major franchises. Genres like Action and Science Fiction also perform strongly, reflecting demand "
    "for large-scale, spectacle-driven films. On the other hand, Comedy, Thriller, War, and Mystery "
    "appear lower in the top ten, suggesting they can still succeed but typically generate less revenue "
    "on average than the big blockbuster categories. Overall, the plot shows that genre choice influences "
    "earning potential, with event-style genres dominating revenue performance."
)

# 5) Ratings vs Revenue
st.header("Ratings vs Revenue")
st.markdown("<div class='plot-box'>", unsafe_allow_html=True)
fig, ax = plt.subplots(figsize=(7, 4.5))
sns.scatterplot(data=filtered_df, x="vote_average", y="revenue", alpha=0.45, ax=ax)
ax.set_yscale("log")
ax.set_xlabel("Ratings")
ax.set_ylabel("Revenue")
ax.set_title("Ratings vs Revenue")
st.pyplot(fig)
st.markdown("</div>", unsafe_allow_html=True)

interpretation(
    "This scatterplot compares a movie’s average audience/critic score with its box office revenue "
    "(log scale). The points form a wide cloud rather than a clear upward line, which means higher "
    "ratings do not reliably lead to higher revenue. Many films rated around 6–8 earn anywhere from "
    "low to extremely high revenue, and some low-rated movies still become big financial successes. "
    "The main takeaway is that revenue is influenced more by factors like budget, marketing, franchise "
    "power, and release timing than by rating alone."
)

# 6) Correlation Heatmap
st.header("Correlation Heatmap")
st.markdown("<div class='plot-box'>", unsafe_allow_html=True)
subset = filtered_df[["budget", "revenue", "profit", "roi", "vote_average", "vote_count", "popularity"]]
fig, ax = plt.subplots(figsize=(7, 4.5))
sns.heatmap(subset.corr(), annot=True, cmap="coolwarm", ax=ax)
ax.set_title("Correlation Heatmap")
st.pyplot(fig)
st.markdown("</div>", unsafe_allow_html=True)

interpretation(
    "This correlation heatmap summarizes how the main variables move together. The strongest relationship "
    "is between revenue and profit (0.98), which is expected because profit is directly derived from revenue. "
    "Budget is strongly correlated with revenue (0.73) and moderately with profit (0.58), showing that higher "
    "spending generally increases earning potential, but not perfectly. Vote average has only weak correlation "
    "with revenue (0.17) and profit (0.20), meaning better-rated films do not consistently earn more. Vote count "
    "and popularity correlate moderately with revenue (0.77 and 0.44), suggesting that visibility and audience "
    "reach matter more for box office success than rating quality alone. Overall, financial success is driven mainly "
    "by scale and exposure, while ratings play a secondary role."
)

# 7) Top 20 Highest Grossing Movies
st.header("Top 20 Highest Grossing Movies")
st.markdown("<div class='plot-box'>", unsafe_allow_html=True)
top20 = filtered_df.sort_values("revenue", ascending=False).head(20)
fig, ax = plt.subplots(figsize=(7, 4.5))
sns.barplot(y=top20["title"], x=top20["revenue"], ax=ax)
ax.set_xlabel("Revenue")
ax.set_ylabel("Movie Title")
ax.set_title("Top 20 Highest Grossing Movies")
st.pyplot(fig)
st.markdown("</div>", unsafe_allow_html=True)

interpretation(
    "This bar chart lists the highest-grossing movies by total revenue within the current filter selection. "
    "The titles are dominated by global franchises and event films, showing that the biggest box-office wins "
    "usually come from large-scale releases with strong brand recognition and worldwide appeal. It reinforces "
    "the idea that blockbuster revenue is concentrated in a small set of high-visibility, high-budget films "
    "rather than spread evenly across the industry."
)
