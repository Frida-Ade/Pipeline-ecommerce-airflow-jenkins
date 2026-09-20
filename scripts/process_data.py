import pandas as pd
from pathlib import Path

# Dossiers
RAW_DATA_PATH = Path("data/raw")
PROCESSED_DATA_PATH = Path("data/processed")

# Création du dossier processed si nécessaire
PROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)

print("Chargement des datasets...")

customers = pd.read_csv(
    RAW_DATA_PATH / "olist_customers_dataset.csv"
)

orders = pd.read_csv(
    RAW_DATA_PATH / "olist_orders_dataset.csv"
)

items = pd.read_csv(
    RAW_DATA_PATH / "olist_order_items_dataset.csv"
)

products = pd.read_csv(
    RAW_DATA_PATH / "olist_products_dataset.csv"
)

translations = pd.read_csv(
    RAW_DATA_PATH / "product_category_name_translation.csv"
)

print("Datasets chargés")

print("Fusion des données...")

df = items.merge(
    products,
    on="product_id",
    how="left"
)

df = df.merge(
    translations,
    on="product_category_name",
    how="left"
)

df = df.merge(
    orders,
    on="order_id",
    how="left"
)

df = df.merge(
    customers,
    on="customer_id",
    how="left"
)

print("Fusion terminée")

# Création des colonnes métier

df["quantity"] = 1

df["amount"] = (
    df["price"] +
    df["freight_value"]
)

# Renommage

df.rename(
    columns={
        "order_purchase_timestamp": "date",
        "customer_unique_id": "customer",
        "customer_state": "region",
        "product_category_name_english": "category"
    },
    inplace=True
)

# Contrôles qualité

invalid_rows = df[
    (df["quantity"] <= 0)
    |
    (df["amount"] <= 0)
]

valid_rows = df[
    (df["quantity"] > 0)
    &
    (df["amount"] > 0)
]

# Sauvegarde erreurs

invalid_rows.to_csv(
    PROCESSED_DATA_PATH / "errors.csv",
    index=False
)

# Dataset final

valid_rows.to_csv(
    PROCESSED_DATA_PATH / "dataset.csv",
    index=False
)

print("Dataset généré")
print(f"Lignes valides : {len(valid_rows)}")
print(f"Lignes rejetées : {len(invalid_rows)}")