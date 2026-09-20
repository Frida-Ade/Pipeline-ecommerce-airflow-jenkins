# Pipeline E-commerce — Airflow, Jenkins & MongoDB

Projet réalisé dans le cadre du Master Data Engineering, visant à industrialiser un pipeline de traitement de données e-commerce, de l'ingestion à la production d'indicateurs décisionnels.

## Contexte

Une entreprise de vente de produits informatiques traitait ses données de ventes manuellement à partir de fichiers CSV, entraînant lenteur, risques d'erreurs et absence de traçabilité. Ce projet automatise l'ensemble de la chaîne : collecte, transformation, calcul des indicateurs et stockage.

## Architecture

Tous les services sont conteneurisés avec Docker Compose (Jenkins, Airflow, MongoDB, PostgreSQL).

## Dataset

[Olist Brazilian E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) — plus de 100 000 commandes réelles (clients, commandes, produits, catégories, paiements).

## Pipeline ETL & DAG Airflow

Le DAG `ecommerce_sales_pipeline` réalise notamment :
- détection et validation du fichier source (FileSensor)
- contrôle qualité des données (montants, quantités, doublons)
- choix dynamique du chemin d'exécution (BranchPythonOperator)
- calcul des indicateurs par catégorie (tâches dynamiques)
- transmission des métriques entre tâches (XComs)
- gestion des erreurs (Trigger Rules)
- génération d'un rapport final et stockage MongoDB

## Intégration continue avec Jenkins

Pipeline CI/CD : Checkout → Install dependencies → Run tests (Pytest) → Validate DAG → Deploy DAG → Trigger DAG → Verify MongoDB.

## Résultats obtenus

- 98 666 commandes traitées, 95 420 clients
- Chiffre d'affaires total calculé : 15 843 553,24 €
- Panier moyen : 160,58 €
- 112 650 lignes valides, 0 ligne rejetée
- Historisation complète des indicateurs dans MongoDB

## Stack technique

Python, Apache Airflow, Jenkins, MongoDB, Docker & Docker Compose, Git, Pytest
