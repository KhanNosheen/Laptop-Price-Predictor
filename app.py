# Import Libraries
import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Package Configuration 
st.set_page_config(
    page_title="Smart PC Price Predictor",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="expanded",
)


# Load cleaned dataset with caching for fast performance
@st.cache_data
def load_data():
  return pd.read_csv("./data/cleaned_data.csv")


df_cleaned = load_data()

# Load model ONCE when the app starts up
model = joblib.load("laptop_price_predict_model.pkl")

# --- Sidebar Model Performance Section ---
st.sidebar.markdown(
    '<h2 style="color: #38bdf8; font-size: 1.3rem;">📊 Model Performance</h2>',
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    '<p style="color: #94a3b8; font-size: 0.85rem;">Evaluated on GridSearchCV'
    " tuned pipeline</p>",
    unsafe_allow_html=True,
)
st.sidebar.metric(label="R² Score", value="0.90")
st.sidebar.metric(label="Mean Absolute Error (MAE)", value="0.15")
st.sidebar.metric(label="Root Mean Squared Error (RMSE)", value="0.21")
st.sidebar.markdown("---")

# Project Summary
st.sidebar.subheader("About Project")
st.sidebar.markdown(
    "An interactive machine learning web application built to estimate "
    "laptop market values in real-time based on hardware specifications "
    "like RAM, CPU, GPU, and storage. \n\n"
    "The underlying prediction engine utilizes a robust regression model "
    "optimized and fine-tuned using **GridSearchCV** across a structured "
    "machine learning pipeline to achieve high predictive accuracy and "
    "minimize error."
)

# Centered Title and Subtitle with Inline Styles
st.markdown(
    '<h1 style="text-align: center; color: #38bdf8; font-size:'
    ' 2.3rem;">🚀 Smart PC Price Predictor</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p style="text-align: center; color: #94a3b8; margin-bottom: 30px;">Estimate'
    " the market value of your computer configuration instantly.</p>",
    unsafe_allow_html=True,
)

# Input Columns Layout
col1, col2 = st.columns(2)

with col1:
  company = st.selectbox("Company", df_cleaned["Company"].unique())
  type_name = st.selectbox("TypeName", df_cleaned["TypeName"].unique())
  inches = st.selectbox("Inches", sorted(df_cleaned["Inches"].unique()))
  ram = st.selectbox(
      "Ram (GB)",
      sorted(
          df_cleaned["Ram"]
          .astype(str)
          .str.replace("GB", "", regex=False)
          .astype(int)
          .unique()
      ),
      format_func=lambda x: f"{x} GB",
  )
  gpu = st.selectbox("Gpu", df_cleaned["Gpu"].unique())
  op_sys = st.selectbox("OpSys", df_cleaned["OpSys"].unique())
  hdd = st.selectbox("HDD (GB)", [0, 500, 1, 2, 32, 128, 10])

with col2:
  ssd = st.selectbox(
      "SSD (GB)", [0, 1, 8, 16, 32, 64, 128, 180, 240, 256, 512, 768, 1024]
  )
  weight = st.slider("Weight (kg)", min_value=0.8, max_value=4.7, value=1.8, step=0.05)
  x_res = st.number_input("X_res", 1024, 3840, 1920)
  y_res = st.number_input("Y_res", 768, 2160, 1080)
  ppi = st.number_input("ppi", 50.0, 300.0, 141.0)
  cpu_brand = st.selectbox(
      "Cpu brand", ["Intel Core i5", "Intel Core i7", "AMD Processor", "Intel Core i3"]
  )
  touchscreen_input = st.toggle("Touchscreen")
  ips_input = st.toggle("IPS Panel")

  # Convert True/False to 1 and 0 model
  touchscreen = 1 if touchscreen_input else 0
  ips = 1 if ips_input else 0

st.markdown("<br><br>", unsafe_allow_html=True)

# Custom CSS to make the button look stunning and distinct
st.markdown(
    """
    <style>
    .stButton > button {
        width: 100%;
        background-color: #0ea5e9;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6rem;
        border: none;
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.2);
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #0284c7;
        color: white;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Place the button cleanly at the bottom spanning full width
submitted = st.button("Predict Price 🚀")

# Handle prediction and render results & charts ONLY when the button is clicked
if submitted:
  with st.spinner("Analyzing computer specifications..."):

    input_data = pd.DataFrame({
        "Company": [company],
        "TypeName": [type_name],
        "Inches": [inches],
        "Ram": [ram],
        "Gpu": [gpu],
        "OpSys": [op_sys],
        "Weight": [weight],
        "HDD": [hdd],
        "SSD": [ssd],
        "Touchscreen": [touchscreen],
        "IPS": [ips],
        "X_res": [x_res],
        "Y_res": [y_res],
        "ppi": [ppi],
        "Cpu brand": [cpu_brand],
    })

    log_prediction = model.predict(input_data)[0]
    predicted_price = np.exp(log_prediction)

    # 1. Plotly Gauge Chart
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=predicted_price,
            title={"text": "Estimated Laptop Price (Rs.)"},
            gauge={
                "axis": {"range": [None, 150000]},
                "bar": {"color": "#636EFA"},
                "steps": [
                    {"range": [0, 50000], "color": "rgba(99, 110, 250, 0.1)"},
                    {"range": [50000, 100000], "color": "rgba(99, 110, 250, 0.3)"},
                    {
                        "range": [100000, 150000],
                        "color": "rgba(99, 110, 250, 0.5)",
                    },
                ],
            },
        )
    )
    fig.update_layout(
        template="plotly_dark", margin=dict(l=20, r=20, t=80, b=20), height=300
    )
    st.plotly_chart(fig, use_container_width=True)


        # Create three columns to act as margins (left, center, right)
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        
        # 4. Display the stylish prediction box with the real price
        st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
                padding: 18px 15px;
                border-radius: 12px;
                text-align: center;
                font-size: 1.4rem;
                font-weight: bold;
                color: #38bdf8;
                border: 2px solid #38bdf8;
            ">
                Estimated Price: Rs. {predicted_price:,.2f}
            </div>
        """, unsafe_allow_html=True)

    
