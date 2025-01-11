import pandas as pd

# Charger le fichier CSV
df = pd.read_csv('/home/bilel/workspace/ploosh/tests/.data/sales.csv')
df_filtered = df[df["sale_id"] > 10]
# Convertir le DataFrame en fichier Parquet

df =  pd.read_parquet("/home/bilel/workspace/ploosh/tests/.env/parquet/sales.parquet",
                             columns=None,
                             engine="auto",
                             filters=[("sale_id", ">", 10)])

df.to_parquet('/home/bilel/workspace/ploosh/tests/.env/parquet/votre_fichier.parquet')

df_filtered.to_csv('/home/bilel/workspace/ploosh/tests/.data/votre_fichier.csv', index= False)
