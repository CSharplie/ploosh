import pandas as pd

# Charger le fichier CSV dans un DataFrame
csv_file = "/home/bilel/workspace/ploosh/tests/.data/sales.csv"
df = pd.read_csv(csv_file)

# Convertir le DataFrame en JSON
json_data = df.to_json(orient="records", lines=False)

# (Optionnel) Sauvegarder le JSON dans un fichier
json_file = "/home/bilel/workspace/ploosh/tests/.env/json/sales-ISO-8859-1.json"
with open(json_file, "w", encoding='ISO-8859-1') as f:
    f.write(json_data)

print("Fichier JSON créé avec succès !")
