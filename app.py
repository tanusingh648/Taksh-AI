import io
import requests
import pandas as pd
import streamlit as st
import plotly.express as px

# =========================================================
# CONFIG
# =========================================================

API = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="TAKSH AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>



@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Orbitron:wght@500;600;700;800&display=swap');

/* =====================================================
   GLOBAL
===================================================== */

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(79,70,229,0.18), transparent 30%),
        radial-gradient(circle at 90% 15%, rgba(6,182,212,0.12), transparent 30%),
        radial-gradient(circle at 50% 90%, rgba(168,85,247,0.10), transparent 35%),
        #050816;

    color: #e5e7eb;
}

/* =====================================================
   STREAMLIT HEADER
===================================================== */

[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stDecoration"] {
    background: transparent !important;
}

/* =====================================================
   MAIN CONTENT
===================================================== */

.block-container {
    padding-top: 3rem !important;
    padding-bottom: 3rem !important;
    max-width: 1400px !important;
}

/* =====================================================
   SIDEBAR
===================================================== */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #050816 0%,
            #080b1c 50%,
            #050816 100%
        ) !important;

    border-right: 1px solid rgba(99,102,241,0.35);
}

/* Logo */

.logo {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 31px !important;
    font-weight: 800 !important;
    letter-spacing: 4px !important;

    color: #67e8f9 !important;

    text-shadow:
        0 0 8px #06b6d4,
        0 0 18px #06b6d4,
        0 0 35px rgba(99,102,241,0.8);
}

.subtitle {
    color: #94a3b8 !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    letter-spacing: 1px !important;
    margin-top: 5px !important;
}

/* Sidebar navigation title */

section[data-testid="stSidebar"] .stRadio > label {
    color: #64748b !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 1.5px !important;
}

/* Sidebar navigation text */

section[data-testid="stSidebar"] .stRadio label {
    color: #cbd5e1 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    padding: 5px 2px !important;
    transition: all 0.2s ease;
}

section[data-testid="stSidebar"] .stRadio label:hover {
    color: #67e8f9 !important;
    text-shadow: 0 0 8px rgba(34,211,238,0.5);
}

/* Sidebar divider */

section[data-testid="stSidebar"] hr {
    border-color: rgba(99,102,241,0.25) !important;
}

/* Backend status */

.status {
    color: #22c55e !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    text-shadow: 0 0 8px rgba(34,197,94,0.4);
}

/* =====================================================
   HEADINGS
===================================================== */

h1 {
    font-family: 'Orbitron', sans-serif !important;
    color: #f8fafc !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
}

h2 {
    font-family: 'Orbitron', sans-serif !important;
    color: #e0f2fe !important;
    font-weight: 600 !important;
    letter-spacing: 1.5px !important;
}

h3 {
    color: #bae6fd !important;
    font-weight: 600 !important;
}

/* Streamlit markdown headings */

.stMarkdown h1,
.stMarkdown h2,
.stMarkdown h3 {
    color: #e2e8f0 !important;
}

/* =====================================================
   HERO
===================================================== */

.hero {
    padding: 38px !important;

    border-radius: 24px;

    background:
        linear-gradient(
            135deg,
            rgba(30,41,90,0.82),
            rgba(15,23,42,0.68)
        );

    border: 1px solid rgba(99,102,241,0.45);

    box-shadow:
        0 0 30px rgba(99,102,241,0.16),
        inset 0 0 30px rgba(6,182,212,0.03);
}

.hero-title {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 45px !important;
    font-weight: 800 !important;
    letter-spacing: 4px !important;
    color: #f8fafc !important;
}

.hero-title span {
    color: #67e8f9 !important;

    text-shadow:
        0 0 8px #06b6d4,
        0 0 20px #06b6d4,
        0 0 35px #6366f1;
}

.hero-text {
    color: #a5b4fc !important;
    font-size: 16px !important;
    font-weight: 400 !important;
    line-height: 1.7 !important;
}

/* =====================================================
   SECTION TITLES
===================================================== */

.section-title {
    font-family: 'Orbitron', sans-serif !important;

    font-size: 22px !important;
    font-weight: 600 !important;

    letter-spacing: 2px !important;

    color: #e0e7ff !important;

    margin-top: 28px !important;
    margin-bottom: 18px !important;

    text-shadow:
        0 0 8px rgba(129,140,248,0.4);
}

/* =====================================================
   NORMAL TEXT
===================================================== */

p {
    color: #cbd5e1 !important;
    font-size: 14px !important;
    line-height: 1.7 !important;
}

span {
    color: inherit;
}

/* =====================================================
   METRIC CARDS
===================================================== */

.card {
    background:
        linear-gradient(
            145deg,
            rgba(15,23,42,0.90),
            rgba(15,23,42,0.65)
        );

    border: 1px solid rgba(99,102,241,0.32);

    border-radius: 18px;

    padding: 22px;

    box-shadow:
        0 0 20px rgba(99,102,241,0.08);

    transition: all 0.25s ease;
}

.card:hover {
    border-color: rgba(34,211,238,0.65);

    box-shadow:
        0 0 25px rgba(34,211,238,0.14);
}

.metric-title {
    color: #94a3b8 !important;

    font-size: 12px !important;
    font-weight: 600 !important;

    letter-spacing: 1px !important;
    text-transform: uppercase;
}

.metric-value {
    color: #67e8f9 !important;

    font-family: 'Orbitron', sans-serif !important;

    font-size: 28px !important;
    font-weight: 700 !important;

    margin-top: 8px;
}

/* =====================================================
   BUTTONS
===================================================== */

div.stButton > button {

    width: 100%;

    border-radius: 12px !important;

    border: 1px solid rgba(99,102,241,0.55) !important;

    background:
        linear-gradient(
            135deg,
            rgba(30,41,90,0.85),
            rgba(15,23,42,0.85)
        ) !important;

    color: #e0f2fe !important;

    font-size: 14px !important;
    font-weight: 600 !important;

    min-height: 42px;

    transition: all 0.25s ease;
}

div.stButton > button:hover {

    color: #67e8f9 !important;

    border-color: #22d3ee !important;

    box-shadow:
        0 0 18px rgba(34,211,238,0.35);

    transform: translateY(-1px);
}

/* =====================================================
   FILE UPLOADER
===================================================== */

[data-testid="stFileUploader"] {

    background: rgba(15,23,42,0.75) !important;

    border: 1px solid rgba(99,102,241,0.4) !important;

    border-radius: 16px !important;

    padding: 15px !important;
}

/* File uploader text */

[data-testid="stFileUploader"] label {
    color: #e2e8f0 !important;
    font-weight: 600 !important;
}

[data-testid="stFileUploader"] section {
    background: rgba(15,23,42,0.5) !important;
    border: 1px dashed rgba(103,232,249,0.35) !important;
}

[data-testid="stFileUploader"] small {
    color: #94a3b8 !important;
}

/* =====================================================
   INPUT BOXES
===================================================== */

.stTextInput label,
.stTextArea label,
.stSelectbox label,
.stNumberInput label {
    color: #cbd5e1 !important;

    font-size: 13px !important;
    font-weight: 600 !important;
}

/* Input fields */

.stTextInput input,
.stTextArea textarea,
.stNumberInput input {

    background: #0f172a !important;

    color: #f8fafc !important;

    border: 1px solid rgba(99,102,241,0.45) !important;

    border-radius: 10px !important;

    font-size: 14px !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus,
.stNumberInput input:focus {

    border-color: #22d3ee !important;

    box-shadow:
        0 0 12px rgba(34,211,238,0.2) !important;
}

/* Placeholder */

input::placeholder,
textarea::placeholder {
    color: #64748b !important;
}

/* =====================================================
   SELECTBOX
===================================================== */

.stSelectbox div[data-baseweb="select"] > div {

    background: #0f172a !important;

    color: #f8fafc !important;

    border: 1px solid rgba(99,102,241,0.45) !important;

    border-radius: 10px !important;
}

/* =====================================================
   RADIO BUTTON
===================================================== */

.stRadio label {
    color: #cbd5e1 !important;
}

/* =====================================================
   DATAFRAME
===================================================== */

[data-testid="stDataFrame"] {

    border: 1px solid rgba(99,102,241,0.35);

    border-radius: 12px;

    overflow: hidden;
}

/* =====================================================
   ALERTS
===================================================== */

[data-testid="stAlert"] {

    border-radius: 12px !important;

    font-size: 14px !important;

    color: #e2e8f0 !important;
}

/* =====================================================
   EXPANDER
===================================================== */

[data-testid="stExpander"] {

    background: rgba(15,23,42,0.65) !important;

    border: 1px solid rgba(99,102,241,0.3) !important;

    border-radius: 12px !important;
}

[data-testid="stExpander"] summary {

    color: #e2e8f0 !important;

    font-weight: 600 !important;
}

/* =====================================================
   CODE / JSON
===================================================== */

code {
    color: #67e8f9 !important;
    background: rgba(15,23,42,0.8) !important;
}

pre {
    background: #080d1d !important;

    border: 1px solid rgba(99,102,241,0.3);

    border-radius: 12px;

    color: #c4b5fd !important;
}

/* =====================================================
   LINKS
===================================================== */

a {
    color: #67e8f9 !important;
}

a:hover {
    color: #a5f3fc !important;
}

/* =====================================================
   SCROLLBAR
===================================================== */

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #050816;
}

::-webkit-scrollbar-thumb {
    background: #312e81;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #06b6d4;
}

</style>
""", unsafe_allow_html=True)





# =========================================================
# SESSION STATE
# =========================================================

if "dataset" not in st.session_state:
    st.session_state.dataset = None

if "profile" not in st.session_state:
    st.session_state.profile = None


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="logo">TAKSH AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">AI-POWERED DATA INTELLIGENCE</div>',
        unsafe_allow_html=True
    )

    page = st.radio(
        "NAVIGATION",
        [
            "Dashboard",
            "Upload Dataset",
            "Profile",
            "Cleaning",
            "EDA",
            "Feature Analysis",
            "Preprocessing",
            "Model Training",
            "Prediction",
            "AI Insights",
            "Report"
        ]
    )

    st.markdown("---")

    st.markdown(
        '<p class="status">● Backend Connected</p>',
        unsafe_allow_html=True
    )


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.markdown("""
    <div class="hero">
        <div class="hero-title">WELCOME TO <span>TAKSH AI</span></div>
        <div class="hero-text">
            AI-powered data analysis, machine learning and automated insights.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="card">
            <div class="metric-title">DATA ANALYSIS</div>
            <div class="metric-value">01</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <div class="metric-title">ML MODELS</div>
            <div class="metric-value">02+</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
            <div class="metric-title">EDA ENGINE</div>
            <div class="metric-value">ON</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="card">
            <div class="metric-title">AI INSIGHTS</div>
            <div class="metric-value">ON</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">QUICK ACTIONS</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("📂 Upload Dataset", use_container_width=True):
            st.info("Use 'Upload Dataset' from the sidebar.")

    with c2:
        if st.button("📊 Explore Data", use_container_width=True):
            st.info("Use 'EDA' from the sidebar.")

    with c3:
        if st.button("🤖 Train Model", use_container_width=True):
            st.info("Use 'Model Training' from the sidebar.")


# =========================================================
# UPLOAD
# =========================================================

elif page == "Upload Dataset":

    st.markdown(
        '<div class="section-title">UPLOAD DATASET</div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload CSV or XLSX",
        type=["csv", "xlsx"]
    )

    if uploaded_file:

        st.session_state.dataset = uploaded_file

        st.success(
            f"Dataset uploaded: {uploaded_file.name}"
        )

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue()
            )
        }

        try:
            response = requests.post(
                f"{API}/upload",
                files=files
            )

            if response.status_code == 200:

                data = response.json()

                st.session_state.profile = data

                c1, c2 = st.columns(2)

                with c1:
                    st.metric("Rows", data["rows"])

                with c2:
                    st.metric("Columns", data["columns"])

            else:
                st.error(response.text)

        except Exception as e:
            st.error(f"Backend connection error: {e}")


# =========================================================
# PROFILE
# =========================================================

elif page == "Profile":

    st.markdown(
        '<div class="section-title">DATASET PROFILE</div>',
        unsafe_allow_html=True
    )

    if st.session_state.dataset is None:

        st.warning("Please upload a dataset first.")

    else:

        file = st.session_state.dataset

        try:

            response = requests.post(
                f"{API}/profile",
                files={
                    "file": (
                        file.name,
                        file.getvalue()
                    )
                }
            )

            if response.status_code == 200:

                data = response.json()

                c1, c2, c3 = st.columns(3)

                with c1:
                    st.metric("Rows", data["rows"])

                with c2:
                    st.metric("Columns", data["columns"])

                with c3:
                    st.metric(
                        "Duplicates",
                        data["duplicate_rows"]
                    )

                st.subheader("Column Names")

                st.write(data["column_names"])

                st.subheader("Data Types")

                st.json(data["data_types"])

                st.subheader("Missing Values")

                st.json(data["missing_values"])

        except Exception as e:
            st.error(str(e))


# =========================================================
# CLEANING
# =========================================================

elif page == "Cleaning":

    st.markdown(
        '<div class="section-title">DATA CLEANING</div>',
        unsafe_allow_html=True
    )

    if st.session_state.dataset is None:

        st.warning("Upload a dataset first.")

    else:

        file = st.session_state.dataset

        if st.button("🧹 Clean Dataset"):

            try:

                response = requests.post(
                    f"{API}/clean",
                    files={
                        "file": (
                            file.name,
                            file.getvalue()
                        )
                    }
                )

                if response.status_code == 200:

                    data = response.json()

                    c1, c2, c3, c4 = st.columns(4)

                    with c1:
                        st.metric(
                            "Original Rows",
                            data["original_rows"]
                        )

                    with c2:
                        st.metric(
                            "Cleaned Rows",
                            data["cleaned_rows"]
                        )

                    with c3:
                        st.metric(
                            "Missing Before",
                            data["missing_values_before"]
                        )

                    with c4:
                        st.metric(
                            "Missing After",
                            data["missing_values_after"]
                        )

                    st.success(
                        data["status"]
                    )

            except Exception as e:
                st.error(str(e))


# =========================================================
# EDA
# =========================================================

elif page == "EDA":

    st.markdown(
        '<div class="section-title">EXPLORATORY DATA ANALYSIS</div>',
        unsafe_allow_html=True
    )

    if st.session_state.dataset is None:

        st.warning("Upload a dataset first.")

    else:

        file = st.session_state.dataset

        if st.button("📊 Run EDA"):

            try:

                response = requests.post(
                    f"{API}/eda",
                    files={
                        "file": (
                            file.name,
                            file.getvalue()
                        )
                    }
                )

                if response.status_code == 200:

                    data = response.json()

                    c1, c2 = st.columns(2)

                    with c1:
                        st.metric("Rows", data["rows"])

                    with c2:
                        st.metric("Columns", data["columns"])

                    st.subheader("Numerical Columns")

                    st.write(
                        data["numerical_columns"]
                    )

                    st.subheader("Categorical Columns")

                    st.write(
                        data["categorical_columns"]
                    )

                    if data["statistics"]:

                        st.subheader(
                            "Statistical Summary"
                        )

                        stats_df = pd.DataFrame(
                            data["statistics"]
                        )

                        st.dataframe(
                            stats_df,
                            use_container_width=True
                        )

            except Exception as e:
                st.error(str(e))


# =========================================================
# FEATURE ANALYSIS
# =========================================================

elif page == "Feature Analysis":

    st.markdown(
        '<div class="section-title">FEATURE ANALYSIS</div>',
        unsafe_allow_html=True
    )

    if st.session_state.dataset is None:

        st.warning("Upload a dataset first.")

    else:

        file = st.session_state.dataset

        if st.button("🧩 Analyze Features"):

            response = requests.post(
                f"{API}/features",
                files={
                    "file": (
                        file.name,
                        file.getvalue()
                    )
                }
            )

            if response.status_code == 200:

                data = response.json()

                st.write(
                    "Numerical Features:",
                    data["numerical_features"]
                )

                st.write(
                    "Categorical Features:",
                    data["categorical_features"]
                )

                st.json(
                    data["feature_summary"]
                )


# =========================================================
# PREPROCESSING
# =========================================================

elif page == "Preprocessing":

    st.markdown(
        '<div class="section-title">PREPROCESSING</div>',
        unsafe_allow_html=True
    )

    if st.session_state.dataset is None:

        st.warning("Upload a dataset first.")

    else:

        file = st.session_state.dataset

        if st.button("⚙️ Process Dataset"):

            response = requests.post(
                f"{API}/processing",
                files={
                    "file": (
                        file.name,
                        file.getvalue()
                    )
                }
            )

            if response.status_code == 200:

                data = response.json()

                st.metric(
                    "Processed Features",
                    data["processed_columns"]
                )

                st.write(
                    data["processed_feature_names"]
                )

                st.success(
                    data["status"]
                )

            else:
                st.error(response.text)


# =========================================================
# MODEL TRAINING
# =========================================================

elif page == "Model Training":

    st.markdown(
        '<div class="section-title">MODEL TRAINING</div>',
        unsafe_allow_html=True
    )

    if st.session_state.dataset is None:

        st.warning("Upload a dataset first.")

    else:

        file = st.session_state.dataset

        df = pd.read_csv(
            io.BytesIO(file.getvalue())
        ) if file.name.endswith(".csv") else pd.read_excel(
            io.BytesIO(file.getvalue())
        )

        target = st.selectbox(
            "Select Target Column",
            df.columns.tolist()
        )

        if st.button("🤖 Train Models"):

            response = requests.post(
                f"{API}/train",
                files={
                    "file": (
                        file.name,
                        file.getvalue()
                    )
                },
                data={
                    "target_column": target
                }
            )

            if response.status_code == 200:

                data = response.json()

                st.success(
                    data["status"]
                )

                st.write(
                    "Problem Type:",
                    data["problem_type"]
                )

                results = data["results"]

                for model, result in results.items():

                    st.subheader(model)

                    st.json(result)

            else:
                st.error(response.text)


# =========================================================
# PREDICTION
# =========================================================

elif page == "Prediction":

    st.markdown(
        '<div class="section-title">MODEL PREDICTION</div>',
        unsafe_allow_html=True
    )

    st.info(
        "Train a model first. Then provide the saved model name and feature values."
    )

    model_name = st.text_input(
        "Model filename",
        placeholder="random_forest_classifier.joblib"
    )

    data_text = st.text_area(
        "Input data as JSON",
        placeholder='{"feature1": 10, "feature2": "value"}'
    )

    if st.button("🔮 Predict"):

        import json

        try:

            data = json.loads(data_text)

            response = requests.post(
                f"{API}/predict",
                json={
                    "model_name": model_name,
                    "data": data
                }
            )

            if response.status_code == 200:

                result = response.json()

                st.success(
                    "Prediction completed"
                )

                st.json(result)

            else:
                st.error(response.text)

        except Exception as e:
            st.error(str(e))


# =========================================================
# AI INSIGHTS
# =========================================================

elif page == "AI Insights":

    st.markdown(
        '<div class="section-title">AI DATA INSIGHTS</div>',
        unsafe_allow_html=True
    )

    if st.session_state.dataset is None:

        st.warning("Upload a dataset first.")

    else:

        file = st.session_state.dataset

        if st.button("🧠 Generate Insights"):

            response = requests.post(
                f"{API}/insights",
                files={
                    "file": (
                        file.name,
                        file.getvalue()
                    )
                }
            )

            if response.status_code == 200:

                data = response.json()

                for insight in data["insights"]:

                    st.info(
                        f"💡 {insight}"
                    )

                if data["numerical_analysis"]:

                    st.subheader(
                        "Numerical Analysis"
                    )

                    st.dataframe(
                        pd.DataFrame(
                            data["numerical_analysis"]
                        ),
                        use_container_width=True
                    )

                if data["correlations"]:

                    st.subheader(
                        "Feature Correlations"
                    )

                    corr_df = pd.DataFrame(
                        data["correlations"]
                    )

                    st.dataframe(
                        corr_df,
                        use_container_width=True
                    )

            else:
                st.error(response.text)


# =========================================================
# REPORT
# =========================================================

elif page == "Report":

    st.markdown(
        '<div class="section-title">REPORT GENERATION</div>',
        unsafe_allow_html=True
    )

    if st.session_state.dataset is None:

        st.warning("Upload a dataset first.")

    else:

        file = st.session_state.dataset

        if st.button("📄 Generate Report"):

            response = requests.post(
                f"{API}/report",
                files={
                    "file": (
                        file.name,
                        file.getvalue()
                    )
                }
            )

            if response.status_code == 200:

                st.success(
                    "Taksh AI report generated successfully!"
                )

                st.download_button(
                    "⬇️ Download HTML Report",
                    data=response.text,
                    file_name="taksh_ai_report.html",
                    mime="text/html"
                )

            else:
                st.error(response.text)