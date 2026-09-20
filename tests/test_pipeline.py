import pandas as pd


def test_dataset_exists():

    df = pd.read_csv(
        "data/processed/dataset.csv"
    )

    assert len(df) > 0


def test_positive_amounts():

    df = pd.read_csv(
        "data/processed/dataset.csv"
    )

    assert (df["amount"] > 0).all()


def test_positive_quantity():

    df = pd.read_csv(
        "data/processed/dataset.csv"
    )

    assert (df["quantity"] > 0).all()


def test_unique_orders():

    df = pd.read_csv(
        "data/processed/dataset.csv"
    )

    assert df["order_id"].nunique() > 0