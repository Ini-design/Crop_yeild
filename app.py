from pathlib import Path

import joblib
import pandas as pd
import streamlit as st


st.set_page_config(
	page_title="Harvest | Crop yield estimator",
	page_icon="🌾",
	layout="wide",
	initial_sidebar_state="expanded",
)

FEATURES = [
	"Rain Fall (mm)",
	"Fertilizer",
	"Temperatue",
	"Nitrogen (N)",
	"Phosphorus (P)",
	"Potassium (K)",
]
TARGET = "Yeild (Q/acre)"
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "crop_yeild.xlsx"
MODEL_PATH = BASE_DIR / "best_crop_yeild.pkl"


def load_artifacts():
	if not DATA_PATH.exists():
		raise FileNotFoundError(f"Dataset not found: {DATA_PATH.name}")
	if not MODEL_PATH.exists():
		raise FileNotFoundError(f"Model not found: {MODEL_PATH.name}")

	raw_data = pd.read_excel(DATA_PATH)
	missing = [column for column in FEATURES + [TARGET] if column not in raw_data]
	if missing:
		raise ValueError(f"Dataset is missing required columns: {', '.join(missing)}")

	numeric_data = raw_data[FEATURES + [TARGET]].apply(pd.to_numeric, errors="coerce")
	clean_data = numeric_data.dropna()
	if clean_data.empty:
		raise ValueError("The dataset has no valid numeric rows.")
	return clean_data, joblib.load(MODEL_PATH)


@st.cache_data(show_spinner=False)
def get_data():
	return load_artifacts()[0]


@st.cache_resource(show_spinner=False)
def get_model():
	return load_artifacts()[1]


def inject_styles():
	st.markdown(
		"""
		<style>
		@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
		:root { --ink:#16251f; --muted:#60726b; --leaf:#19724c; --lime:#d9ef9f; --paper:#f5f7f1; --line:#dce5dc; }
		html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; color:var(--ink); }
		.stApp { background:var(--paper); }
		[data-testid="stSidebar"] { background:#173b2c; border-right:0; }
		[data-testid="stSidebar"] * { color:#edf5e9; }
		[data-testid="stSidebar"] .stCaption { color:#b8cfbf; }
		h1, h2, h3 { font-family:'Space Grotesk', sans-serif; letter-spacing:0; }
		h1 { font-size:clamp(2.2rem, 4vw, 4.3rem); line-height:1.02; margin-bottom:.4rem; }
		.hero { background:#d9ef9f; padding:2.2rem 2.5rem; border-radius:8px; margin-bottom:1.5rem; position:relative; overflow:hidden; }
		.hero:after { content:'FIELD / 01'; position:absolute; right:2rem; top:1.6rem; color:#48734d; font:600 12px 'Space Grotesk'; letter-spacing:2px; }
		.eyebrow { text-transform:uppercase; font-size:.72rem; font-weight:700; letter-spacing:2px; color:#397052; }
		.hero p { max-width:610px; color:#385342; font-size:1.05rem; margin:0; }
		.metric-card { background:#fff; border:1px solid var(--line); border-radius:8px; padding:1rem 1.2rem; min-height:105px; }
		.metric-label { color:var(--muted); font-size:.76rem; text-transform:uppercase; letter-spacing:1px; }
		.metric-value { font:700 1.65rem 'Space Grotesk'; margin-top:.35rem; }
		.stButton > button { background:#19724c; color:white; border:0; border-radius:5px; padding:.7rem 1rem; font-weight:700; }
		.stButton > button:hover { background:#0f5738; color:white; }
		div[data-testid="stForm"] { background:#fff; border:1px solid var(--line); border-radius:8px; padding:1.25rem; }
		.result { background:#173b2c; border-radius:8px; color:#f4f8eb; padding:1.6rem; min-height:190px; }
		.result .value { color:#d9ef9f; font:700 3rem 'Space Grotesk'; line-height:1; margin:.5rem 0; }
		.result small { color:#b8cfbf; }
		</style>
		""",
		unsafe_allow_html=True,
	)


inject_styles()

try:
	data = get_data()
	model = get_model()
except (FileNotFoundError, ValueError, OSError) as error:
	st.error(f"Unable to start the estimator: {error}")
	st.stop()

with st.sidebar:
	st.markdown("## HARVEST")
	st.caption("Crop yield intelligence")
	st.divider()
	st.markdown("### Model status")
	st.success("Ready for estimates")
	st.caption(f"Engine: {type(model).__name__}")
	st.caption(f"Training rows: {len(data):,}")
	st.divider()
	st.caption("Estimates are decision support, not a guarantee of field performance.")

st.markdown(
	'<div class="hero"><div class="eyebrow">Agricultural analytics</div><h1>Plan the next harvest<br>with more signal.</h1><p>Enter your field conditions to estimate expected crop yield per acre.</p></div>',
	unsafe_allow_html=True,
)

metric_columns = st.columns(4)
metric_values = [
	("Dataset rows", f"{len(data):,}"),
	("Average yield", f"{data[TARGET].mean():.1f}"),
	("Yield range", f"{data[TARGET].min():.1f} - {data[TARGET].max():.1f}"),
	("Input signals", str(len(FEATURES))),
]
for column, (label, value) in zip(metric_columns, metric_values):
	with column:
		st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>', unsafe_allow_html=True)

st.markdown("## Field estimate")
st.caption("Use measurements from the same field and growing season for the most useful estimate.")

with st.form("prediction_form"):
	input_columns = st.columns(3)
	inputs = {}
	labels = {
		"Rain Fall (mm)": "Rainfall (mm)",
		"Fertilizer": "Fertilizer",
		"Temperatue": "Temperature",
		"Nitrogen (N)": "Nitrogen (N)",
		"Phosphorus (P)": "Phosphorus (P)",
		"Potassium (K)": "Potassium (K)",
	}
	for index, feature in enumerate(FEATURES):
		series = data[feature]
		with input_columns[index % 3]:
			inputs[feature] = st.number_input(
				labels[feature],
				min_value=float(series.min()),
				max_value=float(series.max()),
				value=float(series.median()),
				step=0.1,
				help=f"Observed range: {series.min():.1f} to {series.max():.1f}",
			)
	submitted = st.form_submit_button("Estimate yield", use_container_width=True)

if submitted:
	prediction = float(model.predict(pd.DataFrame([inputs], columns=FEATURES))[0])
	st.markdown(
		f'<div class="result"><div class="eyebrow">Estimated output</div><div class="value">{prediction:,.1f}</div><div>quintals per acre</div><small>Based on the conditions entered above.</small></div>',
		unsafe_allow_html=True,
	)
else:
	st.info("Enter field conditions and select Estimate yield to generate a result.")

with st.expander("Explore the training data"):
	st.dataframe(data.rename(columns={TARGET: "Yield (Q/acre)", "Temperatue": "Temperature"}), use_container_width=True, hide_index=True)
