import pandas as pd
import json
from pathlib import Path

DATASET = Path("data/processed/dataset.csv")

df = pd.read_csv(DATASET)

nb_commandes = df["order_id"].nunique()

nb_clients = df["customer"].nunique()

chiffre_affaires = round(df["amount"].sum(), 2)

panier_moyen = round(
    chiffre_affaires / nb_commandes,
    2
)

top_products = (
    df.groupby("product_id")["amount"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

ca_region = (
    df.groupby("region")["amount"]
      .sum()
      .to_dict()
)

ca_categorie = (
    df.groupby("category")["amount"]
      .sum()
      .to_dict()
)

kpis = {
    "nb_commandes": int(nb_commandes),
    "nb_clients": int(nb_clients),
    "chiffre_affaires": chiffre_affaires,
    "panier_moyen": panier_moyen,
    "top_products": top_products.to_dict(),
    "ca_region": ca_region,
    "ca_categorie": ca_categorie
}

with open(
    "data/processed/kpis.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        kpis,
        f,
        indent=4
    )

print("KPI générés avec succès")