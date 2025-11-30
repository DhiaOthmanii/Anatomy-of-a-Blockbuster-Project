# src/cleaning.py

import pandas as pd
import ast

json_cols = [
    'belongs_to_collection', 'genres', 'production_companies',
    'production_countries', 'spoken_languages'
]

numeric_cols = ['budget', 'revenue', 'vote_average', 'vote_count', 'popularity']


def parse_json_field(val):
    if pd.isna(val):
        return []
    try:
        return ast.literal_eval(val)
    except:
        return []


def clean_movies_dataset(df):

    # Convert JSON-like fields
    for col in json_cols:
        df[col] = df[col].apply(parse_json_field)

    # Convert numeric fields
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Parse dates
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")

    # Remove impossible values
    df = df[(df["budget"] > 1000) & (df["revenue"] > 1000)]

    # Drop duplicates
    df = df.drop_duplicates(subset="id")

    return df
