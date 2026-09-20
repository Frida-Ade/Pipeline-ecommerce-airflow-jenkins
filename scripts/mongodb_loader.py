import json
from datetime import datetime
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["ecommerce_analytics"]

collection = db["sales_metrics"]

with open(
    "data/processed/kpis.json",
    "r",
    encoding="utf-8"
) as f:
    kpis = json.load(f)

document = {
    "execution_date": datetime.now().isoformat(),
    "dag_id": "ecommerce_sales_pipeline",
    "dataset": "olist",
    "status": "success",
    "global_metrics": {
        "nb_commandes": kpis["nb_commandes"],
        "nb_clients": kpis["nb_clients"],
        "chiffre_affaires": kpis["chiffre_affaires"],
        "panier_moyen": kpis["panier_moyen"]
    },
    "top_products": kpis["top_products"],
    "ca_region": kpis["ca_region"],
    "ca_categorie": kpis["ca_categorie"]
}

collection.insert_one(document)

print("Insertion MongoDB réussie")