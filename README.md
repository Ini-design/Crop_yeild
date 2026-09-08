 # Crop Yield Estimator

Crop Yield Estimator is a Streamlit application that uses field conditions to estimate expected crop yield in quintals per acre. It also includes a training script that compares several regression models and saves the best-performing model for use by the app.

## Features

- Estimate yield from rainfall, fertilizer, temperature, and NPK measurements.
- Display summary statistics from the training data.
- Explore the cleaned training data in the Streamlit interface.
- Compare Linear Regression, Random Forest, Decision Tree, and Support Vector Regression models.
- Select the best model using test-set RMSE and save it with `joblib`.

## Project Files

| File | Description |
| --- | --- |
| `app.py` | Streamlit interface for making yield estimates. |
| `main.py` | Cleans the dataset, trains and evaluates regression models, and saves the best model. |
| `crop_yeild.xlsx` | Excel dataset used for training and predictions. |
| `best_crop_yeild.pkl` | Serialized model loaded by the Streamlit app. |
| `requirement.txt` | Python dependencies. |

## Requirements

- Python 3.9 or newer
- A virtual environment is recommended

Install the dependencies from this project directory:

```bash
python -m venv .venv
```

Activate the environment:

**Windows PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux**

```bash
source .venv/bin/activate
```

Then install the packages:

```bash
python -m pip install -r requirement.txt
```

## Run the Application

From the project directory, start Streamlit:

```bash
streamlit run app.py
```

Open the local URL shown in the terminal, usually `http://localhost:8501`.

The app loads the spreadsheet and model when it starts. Enter values within the observed ranges shown by the input controls, then select **Estimate yield**.

## Retrain the Model

Run the training script after updating `crop_yeild.xlsx` or changing the model-selection logic:

```bash
python main.py
```

The script:

1. Reads the Excel dataset.
2. Converts required columns to numeric values and removes invalid rows.
3. Splits the data into training and test sets using `random_state=42`.
4. Trains four regression models.
5. Reports MAE, R2, and RMSE for each model.
6. Saves the model with the lowest RMSE to `best_crop_yeild.pkl`.

## Dataset Columns

The Excel file must contain these columns:

- `Rain Fall (mm)`
- `Fertilizer`
- `Temperatue`
- `Nitrogen (N)`
- `Phosphorus (P)`
- `Potassium (K)`
- `Yeild (Q/acre)`

The `Temperatue`, `Yeild`, and `crop_yeild` spellings are retained because they are part of the existing dataset and model file interface.

## Troubleshooting

- **Dataset not found:** Run Streamlit from this directory and confirm that `crop_yeild.xlsx` exists beside `app.py`.
- **Model not found:** Run `python main.py` to generate `best_crop_yeild.pkl`.
- **Missing columns:** Check that the Excel headers exactly match the required column names above.
- **PowerShell activation blocked:** Run `Set-ExecutionPolicy -Scope Process Bypass` for the current terminal session, then activate the environment again.

## Disclaimer

Predictions are estimates for decision support. Actual yield can vary with crop variety, soil conditions, pests, irrigation, weather, and other factors that are not represented by the model.
