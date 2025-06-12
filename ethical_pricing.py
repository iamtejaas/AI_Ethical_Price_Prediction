import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("dataset_final.csv")
df.head()

df.drop_duplicates(inplace=True)
df.dropna(inplace=True)

Q1 = df['price'].quantile(0.25)
Q3 = df['price'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df = df[(df['price'] >= lower_bound) & (df['price'] <= upper_bound)]

label_encoders = {}
categorical_cols = ['item_category', 'item_name', 'city', 'market_place']
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

X = df[['item_category', 'item_name', 'city', 'year', 'month', 'date']]
y = df['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Model MAE: ₹{mae:.2f}")
print(f"Model R² Score: {r2:.2f}")

def assess_price(item_category, item_name, city_input):
    from datetime import datetime

    # Encode user inputs
    cat_id = label_encoders['item_category'].transform([item_category])[0]
    name_id = label_encoders['item_name'].transform([item_name])[0]
    if city_input not in label_encoders['city'].classes_:
        label_encoders['city'].classes_ = np.append(label_encoders['city'].classes_, city_input)

    city_id = label_encoders['city'].transform([city_input])[0]


    today = datetime.today()
    input_data = pd.DataFrame([{
        'item_category': cat_id,
        'item_name': name_id,
        'city': city_id,
        'year': today.year,
        'month': today.month,
        'date': today.day
    }])

    predicted_price = model.predict(input_data)[0]

    city_df = df[(df['item_category'] == cat_id) &
                 (df['item_name'] == name_id) &
                 (df['city'] == city_id)]

    min_price = city_df['price'].min()
    max_price = city_df['price'].max()

    if predicted_price < min_price:
        status = "Underpriced"
    elif predicted_price > max_price:
        status = "Overpriced"
    else:
        status = "Ethical"

    print(f"\nItem Category: {item_category}")
    print(f"Item Name: {item_name}")
    print(f"City: {city_input}")
    print(f"Predicted Ethical Price: ₹{predicted_price:.2f}")
    print(f"Ethical Price Range in {city_input}: ₹{min_price:.2f} - ₹{max_price:.2f}")
    print(f"Price Status: {status}")

    market_df = df[(df['item_category'] == cat_id) & (df['item_name'] == name_id)]
    avg_market_prices = market_df.groupby('market_place')['price'].mean().reset_index()
    avg_market_prices['market_place'] = label_encoders['market_place'].inverse_transform(avg_market_prices['market_place'])

    plt.figure(figsize=(8, 5))
    sns.barplot(data=avg_market_prices, x='market_place', y='price', palette='viridis')
    plt.axhline(predicted_price, color='red', linestyle='--', label='Predicted Price')
    plt.title('Price Comparison Across Marketplaces')
    plt.ylabel('Average Price')
    plt.legend()
    plt.tight_layout()
    plt.show()

    city_prices = df[(df['item_category'] == cat_id) &
                    (df['item_name'] == name_id)].groupby('city')['price'].mean().reset_index()
    city_prices['city'] = label_encoders['city'].inverse_transform(city_prices['city'])

    plt.figure(figsize=(10, 5))
    sns.lineplot(data=city_prices, x='city', y='price', marker='o', color='blue')
    plt.axhline(predicted_price, color='green', linestyle='--', label='Predicted Price')
    plt.title('Price Comparison Across Cities')
    plt.ylabel('Average Price')
    plt.xlabel('City')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()