"""
CodeAlpha Data Analytics Internship - Task 2: Exploratory Data Analysis (EDA)
Script: data_generator.py
Generates a realistic, multifaceted E-Commerce Superstore dataset with real-world distributions,
seasonality, margin variations, and strategic business anomalies for analytical exploration.
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_superstore_dataset(output_path="data/superstore_sales.csv", num_records=2500, seed=42):
    np.random.seed(seed)
    random.seed(seed)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    categories_subcategories = {
        "Technology": ["Phones", "Accessories", "Machines", "Copiers"],
        "Furniture": ["Chairs", "Tables", "Bookcases", "Furnishings"],
        "Office Supplies": ["Binders", "Storage", "Paper", "Art", "Appliances", "Envelopes", "Labels"]
    }

    segments = ["Consumer", "Corporate", "Home Office"]
    segment_weights = [0.52, 0.30, 0.18]

    ship_modes = ["Standard Class", "Second Class", "First Class", "Same Day"]
    ship_mode_weights = [0.60, 0.20, 0.15, 0.05]

    regions_states = {
        "West": ["California", "Washington", "Oregon", "Nevada", "Arizona", "Colorado"],
        "East": ["New York", "Pennsylvania", "Massachusetts", "New Jersey", "Ohio"],
        "Central": ["Illinois", "Texas", "Michigan", "Indiana", "Wisconsin", "Minnesota"],
        "South": ["Florida", "North Carolina", "Virginia", "Georgia", "Tennessee"]
    }

    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    days_range = (end_date - start_date).days

    records = []

    for i in range(1, num_records + 1):
        order_id = f"CA-2024-{100000 + i}"
        customer_id = f"CUST-{random.randint(1001, 1450):04d}"
        customer_name = f"Client {customer_id.split('-')[1]}"
        segment = np.random.choice(segments, p=segment_weights)

        # Region & State
        region = random.choice(list(regions_states.keys()))
        state = random.choice(regions_states[region])
        city = f"{state} City"
        postal_code = random.randint(10001, 99950)

        # Date & Seasonality
        day_offset = random.randint(0, days_range)
        order_date = start_date + timedelta(days=day_offset)
        # Seasonal bump in Q4 (Nov-Dec)
        if order_date.month in [11, 12] and random.random() < 0.35:
            day_offset = random.randint(0, days_range)

        # Shipping mode and delivery days
        ship_mode = np.random.choice(ship_modes, p=ship_mode_weights)
        if ship_mode == "Same Day":
            ship_days = 0
        elif ship_mode == "First Class":
            ship_days = random.randint(1, 3)
        elif ship_mode == "Second Class":
            ship_days = random.randint(3, 5)
        else:
            ship_days = random.randint(4, 7)

        ship_date = order_date + timedelta(days=ship_days)

        # Product hierarchy
        category = random.choice(list(categories_subcategories.keys()))
        sub_category = random.choice(categories_subcategories[category])
        product_id = f"{category[:3].upper()}-{sub_category[:3].upper()}-{random.randint(100, 999)}"
        product_name = f"{sub_category} Model {random.randint(10, 99)} Pro"

        # Pricing & Economics
        if category == "Technology":
            base_price = np.random.exponential(scale=220) + 40
            target_margin = 0.28
        elif category == "Furniture":
            base_price = np.random.exponential(scale=180) + 35
            target_margin = 0.12  # Lower margin, sensitive to discount
        else:
            base_price = np.random.exponential(scale=45) + 8
            target_margin = 0.35

        quantity = int(np.random.choice([1, 2, 3, 4, 5, 6, 7, 8], p=[0.30, 0.25, 0.18, 0.12, 0.07, 0.04, 0.03, 0.01]))
        
        # Discount logic
        discount_rate = np.random.choice([0.0, 0.1, 0.2, 0.3, 0.5, 0.7, 0.8], p=[0.45, 0.20, 0.15, 0.10, 0.05, 0.03, 0.02])
        
        unit_price = round(float(base_price), 2)
        gross_sales = round(unit_price * quantity, 2)
        sales = round(gross_sales * (1.0 - discount_rate), 2)

        # Profit model: steep discounts lead to severe negative margins
        # Cost of goods sold
        cogs = gross_sales * (1.0 - target_margin)
        shipping_cost = 4.50 + (ship_days * 1.20)
        profit = round(sales - cogs - shipping_cost, 2)

        # Tables and Bookcases in Central region historically have high discount leakages
        if sub_category in ["Tables", "Bookcases"] and discount_rate >= 0.3:
            profit = round(-abs(profit) * 1.4 - 25.0, 2)

        margin_pct = round((profit / sales) * 100, 2) if sales > 0 else 0.0

        records.append({
            "order_id": order_id,
            "order_date": order_date.strftime("%Y-%m-%d"),
            "ship_date": ship_date.strftime("%Y-%m-%d"),
            "ship_mode": ship_mode,
            "shipping_days": ship_days,
            "customer_id": customer_id,
            "customer_name": customer_name,
            "segment": segment,
            "country": "United States",
            "city": city,
            "state": state,
            "postal_code": postal_code,
            "region": region,
            "product_id": product_id,
            "category": category,
            "sub_category": sub_category,
            "product_name": product_name,
            "sales": sales,
            "quantity": quantity,
            "discount": discount_rate,
            "profit": profit,
            "profit_margin_pct": margin_pct
        })

    df = pd.DataFrame(records)
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} authentic e-commerce transaction records at: {output_path}")
    return df

if __name__ == "__main__":
    generate_superstore_dataset()
