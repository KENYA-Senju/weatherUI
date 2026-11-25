import zipfile
import pandas as pd
from utils import haversine
from config import config


def state_security(state):
    if not state:
        return False
    return state in config.US_LIST.values


def load_data():
    with zipfile.ZipFile(config.us_file) as z:
        with z.open("US.txt") as f:
            return pd.read_csv(f, sep="\t", header=None)


def filter_data(df):
    state = config.secure.get().lower()

    if not state_security(state):
        return df[(df[6] == "P") & (df[14] > 5000)]

    match = config.US_LIST[
        (config.US_LIST["state"].str.lower() == state) |
        (config.US_LIST["abbreviation"].str.lower() == state)
    ]

    if match.empty:
        return df[(df[6] == "P") & (df[14] > 50)]

    abb = match.iloc[0]["abbreviation"]

    return df[
        (df[6] == "P") &
        (df[14] > 50) &
        (df[10].str.lower() == abb.lower())
    ]


def knearest(city, k=5):
    df = load_data()
    filtered = filter_data(df)

    result = filtered[[1, 4, 5]].copy()
    result.columns = ["name", "lat", "lon"]

    match = result[result["name"].str.lower() == city.lower()]
    if match.empty:
        raise ValueError("City not found")

    ref = match.iloc[0]

    distances = []
    for _, row in result.iterrows():
        if row["name"].lower() != city.lower():
            d = haversine(row["lat"], row["lon"], ref["lat"], ref["lon"])
            distances.append((d, row["name"]))

    distances.sort()
    return distances[:k]