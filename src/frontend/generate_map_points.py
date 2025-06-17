import pandas as pd

df = pd.read_csv("flood_features_3.csv")
unique_points = df.groupby(["lat", "lon"]).size().reset_index()[["lat", "lon"]]
unique_points.to_json("map_points.json", orient="records")
