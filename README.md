# Pipeline E-commerce — Airflow, Jenkins & MongoDB

Projet réalisé dans le cadre du Master Data Engineering, visant à industrialiser un pipeline de traitement de données e-commerce, de l'ingestion à la production d'indicateurs décisionnels.

## Contexte

Une entreprise de vente de produits informatiques traitait ses données de ventes manuellement à partir de fichiers CSV, entraînant lenteur, risques d'erreurs et absence de traçabilité. Ce projet automatise l'ensemble de la chaîne : collecte, transformation, calcul des indicateurs et stockage.

## Architecture

Git → Jenkins (tests, validation, déploiement, déclenchement)
→ Apache Airflow (orchestration ETL + calcul des KPI)
→ MongoDB (stockage des indicateurs)

Tous les services sont conteneurisés avec Docker Compose (Jenkins, Airflow, MongoDB, PostgreSQL pour les métadonnées Airflow).

## Dataset

[Olist Brazilian E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) — plus de 100 000 commandes réelles (clients, commandes, produits, catégories, paiements).

## Structure du projet

```text
airflow-ecommerce-project/
├── dags/
│ └── ecommerce_sales_pipeline.py (DAG principal)
├── data/
│ ├── raw/ (données brutes)
│ └── processed/ (données transformées)
├── scripts/
│ ├── process_data.py
│ ├── calculate_kpis.py
│ ├── mongodb_loader.py
│ └── check_mongodb.py
├── tests/
│ └── test_pipeline.py
├── Jenkinsfile
├── docker-compose.yml
└── requirements.txt
```

## Pipeline ETL & DAG Airflow

Le DAG `ecommerce_sales_pipeline` réalise notamment :
- détection et validation du fichier source (FileSensor)
- contrôle qualité des données : montant positif, quantité positive, séparation des lignes valides/invalides
- choix dynamique du chemin d'exécution (BranchPythonOperator)
- calcul des indicateurs par catégorie (tâches dynamiques)
- transmission des métriques entre tâches (XComs)
- gestion des erreurs (TriggerRule.ALL_DONE)
- génération d'un rapport final et stockage MongoDB

## Intégration continue avec Jenkins

Pipeline CI/CD : Checkout → Install dependencies → Run tests (Pytest) → Validate DAG → Deploy DAG → Trigger DAG → Verify MongoDB.

**Résultat : SUCCESS**

## Tests

4 tests réalisés avec Pytest, tous réussis :
- existence du dataset
- validité des montants
- validité des quantités
- validation des commandes

## Exécution du projet

```bash
docker compose up -d
```

- Airflow : http://localhost:8080
- Jenkins : http://localhost:8081
- Lancer les tests : `pytest tests/`

## Résultats obtenus

- 98 666 commandes traitées, 95 420 clients
- Chiffre d'affaires total calculé : 15 843 553,24 €
- Panier moyen : 160,58 €
- 112 650 lignes valides, 0 ligne rejetée
- Historisation complète des indicateurs dans MongoDB

## Stack technique

Python, Apache Airflow, Jenkins, MongoDB, PostgreSQL, Docker & Docker Compose, Git, Pytest
