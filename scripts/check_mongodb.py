from pymongo import MongoClient

client = MongoClient(
    "mongodb://localhost:27017"
)

db = client["ecommerce_analytics"]

collection = db["sales_metrics"]

count = collection.count_documents({})

print(
    f"Documents trouvés : {count}"
)

if count > 0:
    print("MongoDB vérifié avec succès")
else:
    print("Aucune donnée trouvée")