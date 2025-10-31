# ml_model.py
# -------------------------------------------------
# Simple Linear Regression Model for Demand Prediction
# -------------------------------------------------
# This module uses scikit-learn to predict whether demand
# for a product will increase or decrease based on
# its price per unit and current monthly sales.

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# -------------------------------------------------
# Core Predictive Function
# -------------------------------------------------
def predict_demand(products_df):
    """
    Predicts demand trend (Increasing/Decreasing) based on
    'Price (per unit)' and 'Monthly Sales'.

    Args:
        products_df (pd.DataFrame): A dataframe containing at least:
            ['Name', 'Price (per unit)', 'Monthly Sales']

    Returns:
        pd.DataFrame: Original dataframe with new columns:
            ['Predicted Sales', 'Demand', 'Trend Color']
    """

    # Ensure required columns exist
    required_cols = ["Name", "Price (per unit)", "Monthly Sales"]
    for col in required_cols:
        if col not in products_df.columns:
            raise ValueError(f"Missing column: {col}")

    # Prepare data
    X = products_df[["Price (per unit)"]].values
    y = products_df["Monthly Sales"].values

    # Simple linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Predict sales if price changes slightly (-5% to +5%)
    price_variation = X * 1.05
    y_pred = model.predict(price_variation)

    # Compute trend
    demand_trend = []
    predicted_sales = []

    for actual, predicted in zip(y, y_pred):
        predicted_sales.append(round(predicted, 2))
        if predicted > actual:
            demand_trend.append("Increasing")
        else:
            demand_trend.append("Decreasing")

    # Construct result dataframe
    products_df["Predicted Sales"] = predicted_sales
    products_df["Demand"] = demand_trend
    products_df["Trend Color"] = products_df["Demand"].apply(
        lambda x: "green" if x == "Increasing" else "red"
    )

    return products_df


# -------------------------------------------------
# Summary Generator
# -------------------------------------------------
def generate_summary(predicted_df):
    """
    Generates a brief text summary of demand prediction results.

    Args:
        predicted_df (pd.DataFrame): DataFrame from predict_demand()

    Returns:
        str: Summary paragraph
    """
    inc = (predicted_df["Demand"] == "Increasing").sum()
    dec = (predicted_df["Demand"] == "Decreasing").sum()
    total = len(predicted_df)

    summary = (
        f"Out of {total} products analyzed, {inc} show an increasing demand trend "
        f"while {dec} are expected to experience a decline. "
        "This analysis considers the relationship between product pricing and recent "
        "sales data using a linear regression model. Products with an increasing trend "
        "may benefit from proactive stock replenishment and promotion, while those "
        "with decreasing trends may require pricing review or marketing adjustments. "
        "Continuous monitoring of demand allows the supply chain to remain adaptive "
        "and responsive to market shifts, ensuring operational efficiency and optimal "
        "resource allocation."
    )

    return summary


# -------------------------------------------------
# Test Stub (Standalone Run)
# -------------------------------------------------
if __name__ == "__main__":
    # Example dataset
    data = {
        "Name": ["Widget A", "Widget B", "Widget C", "Widget D"],
        "Price (per unit)": [10, 20, 15, 30],
        "Monthly Sales": [100, 50, 75, 30]
    }

    df = pd.DataFrame(data)
    result = predict_demand(df)
    print(result[["Name", "Price (per unit)", "Monthly Sales", "Predicted Sales", "Demand"]])
    print("\nSummary:\n", generate_summary(result))
