# src/analysis.py

def create_features(df):

    # Profit
    df["profit"] = df["revenue"] - df["budget"]

    # ROI
    df["roi"] = df["profit"] / df["budget"]

    # Release year
    df["release_year"] = df["release_date"].dt.year

    # Extract genre names
    df["genre_names"] = df["genres"].apply(
        lambda x: [d["name"] for d in x] if isinstance(x, list) else []
    )

    return df
