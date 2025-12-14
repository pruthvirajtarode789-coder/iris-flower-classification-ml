import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle
import os

# Auto-detect CSV file
csv_file = None
for f in os.listdir():
    if f.lower().endswith(".csv"):
        csv_file = f
        break

if csv_file is None:
    raise FileNotFoundError("❌ No CSV file found")

print("Using dataset:", csv_file)

df = pd.read_csv(csv_file)
print("Columns:", df.columns)

# Remove ID column if present
if 'Id' in df.columns:
    df = df.drop('Id', axis=1)

# Detect target column automatically
for target_col in ['species', 'Species', 'variety', 'class', 'target']:
    if target_col in df.columns:
        y = df[target_col]
        X = df.drop(target_col, axis=1)
        break
else:
    raise Exception("❌ No target (species) column found")

# Train model
model = LogisticRegression(max_iter=200)
model.fit(X, y)

# Save model
pickle.dump(model, open("iris_model.pkl", "wb"))

print("✅ Iris model trained successfully")
