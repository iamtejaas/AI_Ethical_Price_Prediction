from flask import Flask, render_template, request
from model_updated import assess_price
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# In-memory prediction history
history = []

# Load dropdown options from CSV
try:
    df = pd.read_csv("ethical_pricing_mock_dataset_extended.csv")
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)

    category_items = df.groupby("item_category")["item_name"].unique().apply(list).to_dict()
    sorted_categories = sorted(category_items.keys())
    unique_cities = sorted(df["city"].unique().tolist())
except Exception as e:
    print("Error loading dropdown data:", e)
    category_items = {}
    sorted_categories = []
    unique_cities = []

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    selected_category = ""
    selected_item = ""
    selected_city = ""

    if request.method == "POST":
        selected_category = request.form.get("item_category")
        selected_item = request.form.get("item_name")
        selected_city = request.form.get("city")

        if selected_category and selected_item and selected_city:
            result = assess_price(selected_category, selected_item, selected_city)

            # Save result to history
            history.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "category": selected_category,
                "item": selected_item,
                "city": selected_city,
                "predicted_price": result.get("predicted_price"),
                "fair_label": result.get("fair_label")
            })

    # Clear values on page refresh
    if request.method == "GET":
        selected_category = ""
        selected_item = ""
        selected_city = ""

    return render_template("index.html",
                           categories=sorted_categories,
                           category_items=category_items,
                           cities=unique_cities,
                           category=selected_category,
                           item_name=selected_item,
                           city=selected_city,
                           result=result)


@app.route("/get_items_for_category", methods=["POST"])
def get_items_for_category():
    category = request.form.get("category")
    if category and category in category_items:
        return category_items[category]
    return []

@app.route("/history")
def view_history():
    return render_template("history.html", history=history)

@app.route("/compare", methods=["POST"])
def compare_prices():
    try:
        category = request.form["comp_category"]
        item = request.form["comp_item"]
        city_a = request.form["city_a"]
        city_b = request.form["city_b"]

        df_filtered = df[
            (df["item_category"] == category) &
            (df["item_name"] == item) &
            (df["city"].isin([city_a, city_b]))
        ]

        if df_filtered.empty:
            return "No data available for comparison", 404

        comparison = df_filtered.groupby("city")["base_price"].agg(["min", "max", "mean"]).reset_index()
        comparison_html = comparison.to_html(
            index=False,
            float_format="₹{:,.2f}".format,
            classes="stats-table"
        )

        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Price Comparison for {item}</title>
            <style>
                body {{
                    margin: 0;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(to right top,  #00c9ff, #92fe9d);
                    min-height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: flex-start;
                    padding: 40px 20px;
                }}

                .container {{
                    width: 100%;
                    max-width: 900px;
                    background: #ffffffcc;
                    padding: 30px;
                    border-radius: 12px;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                    animation: fadeIn 0.8s ease-in-out;
                }}

                h2 {{
                    text-align: center;
                    color: #01579b;
                    margin-bottom: 30px;
                }}

                .stats-table {{
                    width: 100%;
                    margin-top: 20px;
                    border-collapse: collapse;
                    border-radius: 12px;
                    overflow: hidden;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                    background: #ffffff;
                }}

                .stats-table th, .stats-table td {{
                    padding: 14px 18px;
                    text-align: center;
                    border-bottom: 1px solid #ddd;
                    font-size: 15px;
                }}

                .stats-table th {{
                    background-color: #0288d1;
                    color: #fff;
                    font-weight: bold;
                }}

                .stats-table tr:nth-child(even) {{
                    background-color: #f2f9fc;
                }}

                .stats-table tr:hover {{
                    background-color: #e1f5fe;
                }}

                @keyframes fadeIn {{
                    from {{
                        opacity: 0;
                        transform: translateY(20px);
                    }}
                    to {{
                        opacity: 1;
                        transform: translateY(0);
                    }}
                }}

                .back-button {{
                    margin-top: 30px;
                    display: inline-block;
                    background: #0288d1;
                    color: white;
                    padding: 10px 20px;
                    border-radius: 8px;
                    text-decoration: none;
                    font-weight: bold;
                    transition: background 0.3s ease;
                }}
                .back-button:hover {{
                    background: #026fa1;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Price Comparison for {item}</h2>
                {comparison_html}
                <div style="text-align: center;">
                    <a href="/" class="back-button">⬅ Back to Home</a>
                </div>
            </div>
        </body>
        </html>
        """
        return html

    except Exception as e:
        return f"Error during comparison: {str(e)}", 500


@app.route('/about')
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
