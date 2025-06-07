# AI_Ethical_Price_Prediction
  An Ethical Pricing Prediction Model that uses machine learning to determine fair and sustainable product prices, considering factors like production costs, fair wages, and environmental impact.<br>

## Ethical Pricing Prediction Model
  This repository houses the code and data for an Ethical Pricing Prediction Model, designed to determine fair and sustainable prices for various products. The project leverages machine learning to integrate crucial ethical considerations such as production costs, fair wages, environmental sustainability, and local market dynamics into pricing strategies.

**Project Overview**
  The primary goal of this project is to create a robust model that can suggest an ethical price range and a specific ethical price for products. This is achieved by training a * *RandomForestRegressor* * on a synthetic dataset that simulates real-world pricing factors. The model aims to help businesses establish prices that are not only competitive but also socially responsible and environmentally conscious.

**Key Features**
  *Ethical Price Prediction*: Generates a recommended ethical price and an acceptable price range for a given product, category, and city.

  *Multi-factor Analysis*: Incorporates a wide array of factors including:

    production_cost
    fair_wage_multiplier
    sustainability_score
    local_demand_index
    market_avg_price_city
    profit_margin_standard
    regulatory_adjustment

  *Machine Learning Powered*: Utilizes a RandomForestRegressor for its ability to handle complex relationships and provide accurate predictions.

  *Comprehensive Dataset*: Built upon ethical_pricing_mock_dataset_extended.csv, a detailed mock dataset containing diverse product entries, categories, and geographical locations.

  *Model Persistence*: The trained model and label encoders are saved, allowing for easy deployment and future use without retraining.<br>
**Files in this Repository**
    *Project 1 (1).ipynb*: The main Jupyter Notebook that contains the complete workflow of the project. This includes:
                          Data loading and initial exploration.
                          Feature engineering and data preprocessing (e.g., LabelEncoder for categorical features).
                          Model training (RandomForestRegressor).
                          Model evaluation.
                          A custom function predict_ethical_price to demonstrate how to get predictions for new product inputs.
                          Saving the trained model and label encoders.

    *ethical_pricing_mock_dataset_extended.csv*: The synthetic dataset used to train and test the ethical pricing model. Each row represents a unique product-location combination with various pricing and ethical attributes.

    *ethical_price_model.pkl*: A serialized (pickled) file containing the trained RandomForestRegressor model. This allows for direct loading and use of the model without needing to retrain it.

    *label_encoders.pkl*: A serialized (pickled) file containing the LabelEncoder objects used for transforming categorical features (item_category, city, marketplace) into numerical representations during training. These are essential for consistent preprocessing when making new predictions.
