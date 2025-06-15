import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

file_path = Path(__file__).resolve().parent.parent.parent.parent
df = pd.read_csv(file_path / "src" / "data_aggregation" / "flood_dataset_full.csv")

# Substitui valores inválidos (ex: -9999, -1000, etc.) por NaN
df["PRECTOTCORR_SUM"] = df["PRECTOTCORR_SUM"].replace([-999, -9999, -1000], np.nan)

# Remove linhas com dados climáticos ausentes
df = df.dropna(subset=["PRECTOTCORR_SUM"])

sns.scatterplot(data=df, x="hand", y="PRECTOTCORR_SUM")
plt.title("Dispersão HAND vs Chuva")
plt.show()

