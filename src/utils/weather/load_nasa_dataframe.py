import json
from pathlib import Path

import pandas as pd

file_path = Path(__file__).resolve().parent.parent.parent

# Load the JSON file
with open(
    file_path / "data" / "json_dados_2010_2025_POWER_Point_Monthly_20100101_20251231_012d25S_038d95W_UTC.json",
    "r",
) as f:
    data = json.load(f)

# Extract the "parameter" dict
params = data["properties"]["parameter"]

# Create a DataFrame for each parameter and merge them
df_list = []

for param_name, values in params.items():
    df_param = pd.DataFrame.from_dict(values, orient="index", columns=[param_name])
    df_param.index.name = "yyyymm"
    df_list.append(df_param)

# Merge all variables into one DataFrame
climate_df = pd.concat(df_list, axis=1).reset_index()

# Convert 'yyyymm' to datetime (handle 13-month anomalies by dropping them)
climate_df = climate_df[climate_df["yyyymm"].str[-2:] != "13"]  # Remove fake "month 13"
climate_df["date"] = pd.to_datetime(climate_df["yyyymm"], format="%Y%m")

# Reorder columns
climate_df = climate_df[["date"] + [col for col in climate_df.columns if col not in ["date", "yyyymm"]]]

# Show sample
print(climate_df.head())
