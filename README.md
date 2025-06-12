
# AI Ethical Price Prediction

An Ethical Pricing Prediction Model that uses machine learning to determine fair and sustainable product prices, considering factors like production costs, fair wages, and environmental impact.

---

## Ethical Pricing Prediction Model

This repository houses the code and web app for an Ethical Pricing Prediction Model, designed to determine fair and sustainable prices for various products. The project leverages machine learning to integrate crucial ethical considerations such as production costs, fair wages, environmental sustainability, and local market dynamics into pricing strategies.

---

## Project Overview

The primary goal of this project is to create a robust model that can suggest an ethical price range and a specific ethical price for products. This is achieved by training a **RandomForestRegressor** on a synthetic dataset that simulates real-world pricing factors. The model helps businesses establish prices that are not only competitive but also socially responsible and environmentally conscious.

---

## Key Features

- **Ethical Price Prediction**: Generates a recommended ethical price and an acceptable price range for a given product, category, and city.

- **Multi-factor Analysis**: Incorporates a wide array of factors including:
  - `production_cost`
  - `fair_wage_multiplier`
  - `sustainability_score`
  - `local_demand_index`
  - `market_avg_price_city`
  - `profit_margin_standard`
  - `regulatory_adjustment`

- **Machine Learning Powered**: Utilizes a RandomForestRegressor for its ability to handle complex relationships and provide accurate predictions.

- **Comprehensive Dataset**: Built upon `ethical_pricing_mock_dataset_extended.csv`, a detailed mock dataset containing diverse product entries, categories, and geographical locations.

- **Web Interface**: A Flask-based web application where users can input product details and get predictions, comparisons, and history.

- **Model Graphs**: Automatic generation of:
  - Price distribution plots
  - Marketplace comparisons
  - City-level trends

---

## Files in this Repository

```
├── app.py                   # Flask backend with routing and form handling
├── model_updated.py        # Prediction model using fairness metrics
├── ethical_pricing.py      # Initial EDA, training and visualization
├── templates/
│   ├── index.html          # User interface
│   ├── history.html        # View prediction history
│   └── about.html          # Project description
├── ethical_pricing_mock_dataset_extended.csv # Dataset
├── README.md               # Project overview
```

---

## Routes

- `/` - Main Prediction Interface
- `/compare` - Compare a product’s price between two cities
- `/history` - View historical prediction records
- `/about` - Learn more about the purpose of the tool

---

## Model Details

- **Model**: RandomForestRegressor
- **Preprocessing**: Label Encoding for `item_category`, `item_name`, `city`
- **Target Variable**: `base_price`
- **Evaluation Metrics**:
  - Price MSE
  - Ethical Classification Accuracy
- **Persistence**: Notebooks save trained models and encoders for reuse
