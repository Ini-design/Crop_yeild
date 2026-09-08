import pandas as pd
import joblib
from math import sqrt
from pathlib import Path

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR


# load the dataset
data_path = Path(__file__).with_name("crop_yeild.xlsx")
df = pd.read_excel(data_path)

# data exploration
print(df.head())   
features = [
    "Rain Fall (mm)",
    "Fertilizer",
    "Temperatue",
    "Nitrogen (N)",
    "Phosphorus (P)",
    "Potassium (K)",
   
]

# Convert spreadsheet values to numbers. Invalid placeholders such as ':' become
# missing values and are removed before model training.
required_columns = features + ["Yeild (Q/acre)"]
missing_columns = [column for column in required_columns if column not in df.columns]
if missing_columns:
    raise KeyError(f"Missing required columns: {missing_columns}")

numeric_data = df[required_columns].apply(pd.to_numeric, errors="coerce")
clean_data = numeric_data.dropna()
if clean_data.empty:
    raise ValueError("The dataset has no rows with valid numeric feature and yield values.")

# Split into training and test data.
X = clean_data[features]
y = clean_data["Yeild (Q/acre)"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# model loading
models = {
    "linear_regression": LinearRegression(),
    "random_forest": RandomForestRegressor(random_state=42),
    "decision_tree": DecisionTreeRegressor(random_state=42),
    "svm": SVR()
}
# model evaluation and training
results = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    results[name] = {
        "mae": mean_absolute_error(y_test, y_pred),
        "r2": r2_score(y_test, y_pred),
        "rmse": sqrt(mean_squared_error(y_test, y_pred))
    }
    print(f"Model: {name}")
    print(f"MAE: {results[name]['mae']}")
    print(f"R2 Score: {results[name]['r2']}")
    print(f"RMSE: {results[name]['rmse']}")
    print()
results_df = pd.DataFrame(results).T.sort_values(by="rmse")

best_model_name = results_df.index[0]
best_model = models[best_model_name]

print(f"Best model: {best_model_name} with RMSE: {results_df.loc[best_model_name]['rmse']}")
model_path = Path(__file__).with_name("best_crop_yeild.pkl")
joblib.dump(best_model, model_path)
