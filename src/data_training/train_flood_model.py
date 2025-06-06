import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
from pathlib import Path


file_path = Path(__file__).resolve(strict=True).parent.parent.parent

# === 1. Carrega os dados ===
df = pd.read_csv(file_path / "data" / "flood_dataset_full.csv")

# === 2. Substitui valores inválidos por NaN ===
flags = [-999, -9999, -1000]
for col in ["PRECTOTCORR_SUM", "RH2M", "GWETROOT", "GWETTOP"]:  # adicione mais se necessário
    if col in df.columns:
        df[col] = df[col].replace(flags, np.nan)

# === 3. Remove linhas com NaN em variáveis importantes ===
df = df.dropna(subset=["PRECTOTCORR_SUM", "RH2M", "GWETROOT", "GWETTOP", "hand"])

# === 4. Gera a variável flood_occurred (rótulo) com regra simples ===
# Ajuste os limites se necessário
df["flood_occurred"] = ((df["hand"] < 2.0) & (df["PRECTOTCORR_SUM"] > 80)).astype(int)

# === 5. Prepara features e target ===
features = ["hand", "PRECTOTCORR_SUM", "RH2M", "GWETROOT", "GWETTOP"]
X = df[features]
y = df["flood_occurred"]

# === 6. Divide em treino e teste ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# === 7. Treina o modelo ===
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# === 8. Avalia o modelo ===
y_pred = model.predict(X_test)
print("✅ Avaliação do modelo:\n")
print(classification_report(y_test, y_pred))

# === 9. Salva o modelo ===
joblib.dump(model, "modelo_flood_rf.pkl")
print("\n📦 Modelo salvo como 'modelo_flood_rf.pkl'")
