import io
import json
import requests
import pandas as pd
import streamlit as st
import plotly.express as px

API = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="TAKSH AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ========================= CSS =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Orbitron:wght@500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(79,70,229,.18), transparent 30%),
        radial-gradient(circle at 90% 15%, rgba(6,182,212,.12), transparent 30%),
        radial-gradient(circle at 50% 90%, rgba(168,85,247,.10), transparent 35%),
        #050816;
    color:#e5e7eb;
}
[data-testid="stHeader"] { background:transparent !important; }
.block-container { padding-top:2.5rem !important; max-width:1400px !important; }

section[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#050816,#080b1c 50%,#050816) !important;
    border-right:1px solid rgba(99,102,241,.35);
}
.logo {
    font-family:'Orbitron',sans-serif !important;
    font-size:31px !important; font-weight:800 !important;
    letter-spacing:4px !important; color:#67e8f9 !important;
    text-shadow:0 0 8px #06b6d4,0 0 18px #06b6d4,0 0 35px rgba(99,102,241,.8);
}
.subtitle { color:#94a3b8 !important; font-size:11px !important; letter-spacing:1px !important; }
section[data-testid="stSidebar"] .stRadio label { color:#cbd5e1 !important; }
h1,h2 { font-family:'Orbitron',sans-serif !important; color:#f8fafc !important; }
h3 { color:#bae6fd !important; }
p,label { color:#cbd5e1 !important; }

.hero {
    padding:38px; border-radius:24px;
    background:linear-gradient(135deg,rgba(30,41,90,.82),rgba(15,23,42,.68));
    border:1px solid rgba(99,102,241,.45);
    box-shadow:0 0 30px rgba(99,102,241,.16);
}
.hero-title {
    font-family:'Orbitron',sans-serif !important;
    font-size:42px !important; font-weight:800 !important;
    letter-spacing:4px !important; color:#f8fafc !important;
}
.hero-title span {
    color:#67e8f9 !important;
    text-shadow:0 0 8px #06b6d4,0 0 20px #06b6d4,0 0 35px #6366f1;
}
.hero-text { color:#a5b4fc !important; font-size:16px !important; line-height:1.7 !important; }
.section-title {
    font-family:'Orbitron',sans-serif !important; font-size:22px !important;
    font-weight:600 !important; letter-spacing:2px !important;
    color:#e0e7ff !important; margin:25px 0 18px 0 !important;
}
.card {
    background:linear-gradient(145deg,rgba(15,23,42,.90),rgba(15,23,42,.65));
    border:1px solid rgba(99,102,241,.32); border-radius:18px; padding:22px;
}
.metric-title { color:#94a3b8 !important; font-size:12px !important; letter-spacing:1px !important; }
.metric-value {
    color:#67e8f9 !important; font-family:'Orbitron',sans-serif !important;
    font-size:28px !important; font-weight:700 !important;
}
div.stButton > button {
    width:100%; min-height:42px; border-radius:12px !important;
    border:1px solid rgba(99,102,241,.55) !important;
    background:linear-gradient(135deg,rgba(30,41,90,.85),rgba(15,23,42,.85)) !important;
    color:#e0f2fe !important; font-weight:600 !important;
}
div.stButton > button:hover {
    color:#67e8f9 !important; border-color:#22d3ee !important;
    box-shadow:0 0 18px rgba(34,211,238,.35);
}
[data-testid="stFileUploader"] {
    background:rgba(15,23,42,.75) !important;
    border:1px solid rgba(99,102,241,.4) !important;
    border-radius:16px !important; padding:15px !important;
}
.stTextInput input,.stTextArea textarea,.stNumberInput input {
    background:#0f172a !important; color:#f8fafc !important;
    border:1px solid rgba(99,102,241,.45) !important; border-radius:10px !important;
}
.stSelectbox div[data-baseweb="select"] > div {
    background:#0f172a !important; color:#f8fafc !important;
    border:1px solid rgba(99,102,241,.45) !important; border-radius:10px !important;
}
[data-testid="stDataFrame"] { border:1px solid rgba(99,102,241,.35); border-radius:12px; overflow:hidden; }
.status-ok { color:#22c55e !important; font-weight:700; }
.status-bad { color:#ef4444 !important; font-weight:700; }
</style>
""", unsafe_allow_html=True)

# ========================= SESSION =========================
for key, value in {
    "dataset_bytes": None,
    "dataset_name": None,
    "profile": None,
    "last_eda": None,
    "last_training": None,
    "last_insights": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ========================= HELPERS =========================
def backend_get():
    try:
        r = requests.get(f"{API}/", timeout=5)
        return r.status_code == 200
    except requests.RequestException:
        return False

def api_post(endpoint, files=None, data=None, json_data=None, timeout=120):
    try:
        r = requests.post(
            f"{API}{endpoint}",
            files=files,
            data=data,
            json=json_data,
            timeout=timeout,
        )
        if 200 <= r.status_code < 300:
            return r

        try:
            detail = r.json()
        except Exception:
            detail = r.text
        st.error(f"API Error {r.status_code}")
        st.code(json.dumps(detail, indent=2, default=str))
        return None

    except requests.exceptions.ConnectionError:
        st.error(
            "❌ FastAPI backend is not running. "
            "Run: python -m uvicorn backend.main:app --reload"
        )
    except requests.exceptions.Timeout:
        st.error("⏳ Backend request timed out.")
    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")
    return None

def make_files(name, content):
    return {"file": (name, content)}

def get_file():
    return st.session_state.dataset_name, st.session_state.dataset_bytes

def load_df(name, content):
    try:
        if name.lower().endswith(".csv"):
            try:
                return pd.read_csv(io.BytesIO(content))
            except UnicodeDecodeError:
                return pd.read_csv(io.BytesIO(content), encoding="latin1")
        return pd.read_excel(io.BytesIO(content))
    except Exception as e:
        st.error(f"Could not read dataset: {e}")
        return None

def require_dataset():
    name, content = get_file()
    if content is None:
        st.warning("Please upload a dataset first.")
        return None, None
    return name, content

# ========================= SIDEBAR =========================
with st.sidebar:
    st.markdown('<div class="logo">TAKSH AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">AI-POWERED DATA INTELLIGENCE</div>', unsafe_allow_html=True)
    st.markdown("---")

    page = st.radio(
        "NAVIGATION",
        [
            "Dashboard","Upload Dataset","Profile","Cleaning","EDA",
            "Feature Analysis","Preprocessing","Model Training",
            "Prediction","AI Insights","Report"
        ],
    )

    st.markdown("---")
    if backend_get():
        st.markdown('<p class="status-ok">● Backend Connected</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="status-bad">● Backend Offline</p>', unsafe_allow_html=True)

# ========================= DASHBOARD =========================
if page == "Dashboard":
    st.markdown("""
    <div class="hero">
        <div class="hero-title">WELCOME TO <span>TAKSH AI</span></div>
        <div class="hero-text">AI-powered data analysis, machine learning and automated insights.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">PLATFORM OVERVIEW</div>', unsafe_allow_html=True)
    a,b,c,d = st.columns(4)
    for col, title, value in [
        (a,"DATASET","READY"),(b,"ML MODELS","02+"),
        (c,"EDA ENGINE","ON"),(d,"AI INSIGHTS","ON")
    ]:
        with col:
            st.markdown(
                f'<div class="card"><div class="metric-title">{title}</div>'
                f'<div class="metric-value">{value}</div></div>',
                unsafe_allow_html=True
            )

    st.markdown('<div class="section-title">QUICK ACTIONS</div>', unsafe_allow_html=True)
    q1,q2,q3 = st.columns(3)
    with q1:
        if st.button("📂 Go to Upload Dataset"):
            st.info("Select 'Upload Dataset' from the sidebar.")
    with q2:
        if st.button("📊 Go to EDA"):
            st.info("Select 'EDA' from the sidebar.")
    with q3:
        if st.button("🤖 Go to Model Training"):
            st.info("Select 'Model Training' from the sidebar.")

    if st.session_state.dataset_name:
        st.success(f"Current dataset: {st.session_state.dataset_name}")
    else:
        st.info("Upload a CSV or XLSX dataset to begin.")

# ========================= UPLOAD =========================
elif page == "Upload Dataset":
    st.markdown('<div class="section-title">UPLOAD DATASET</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload CSV or XLSX", type=["csv","xlsx"])

    if uploaded is not None:
        content = uploaded.getvalue()
        name = uploaded.name
        st.session_state.dataset_bytes = content
        st.session_state.dataset_name = name

        st.success(f"✅ Dataset loaded: {name}")
        df = load_df(name, content)

        if df is not None:
            a,b,c,d = st.columns(4)
            a.metric("Rows", f"{len(df):,}")
            b.metric("Columns", len(df.columns))
            c.metric("Missing Values", int(df.isna().sum().sum()))
            d.metric("Duplicate Rows", int(df.duplicated().sum()))

            st.subheader("Dataset Preview")
            st.dataframe(df.head(10), width="stretch")

        r = api_post("/upload", files=make_files(name, content))
        if r is not None:
            data = r.json()
            st.session_state.profile = data
            st.success("Backend upload completed.")
            st.json(data)

# ========================= PROFILE =========================
elif page == "Profile":
    st.markdown('<div class="section-title">DATASET PROFILE</div>', unsafe_allow_html=True)
    name, content = require_dataset()

    if content is not None and st.button("🔍 Generate Dataset Profile"):
        r = api_post("/profile", files=make_files(name, content))
        if r is not None:
            data = r.json()
            if "error" in data:
                st.error(data["error"])
            else:
                st.session_state.profile = data
                a,b,c = st.columns(3)
                a.metric("Rows", data.get("rows",0))
                b.metric("Columns", data.get("columns",0))
                c.metric("Duplicates", data.get("duplicate_rows",0))
                st.subheader("Column Names")
                st.write(data.get("column_names",[]))
                st.subheader("Data Types")
                st.json(data.get("data_types",{}))
                st.subheader("Missing Values")
                st.json(data.get("missing_values",{}))

# ========================= CLEANING =========================
elif page == "Cleaning":
    st.markdown('<div class="section-title">DATA CLEANING</div>', unsafe_allow_html=True)
    name, content = require_dataset()

    if content is not None:
        st.info("Cleaning is performed by the backend. Your original uploaded file is kept unchanged.")
        if st.button("🧹 Clean Dataset"):
            r = api_post("/clean", files=make_files(name, content))
            if r is not None:
                data = r.json()
                if "error" in data:
                    st.error(data["error"])
                else:
                    a,b,c,d = st.columns(4)
                    a.metric("Original Rows",data.get("original_rows",0))
                    b.metric("Cleaned Rows",data.get("cleaned_rows",0))
                    c.metric("Missing Before",data.get("missing_values_before",0))
                    d.metric("Missing After",data.get("missing_values_after",0))
                    st.success(data.get("status","Cleaning completed."))

# ========================= EDA =========================
elif page == "EDA":
    st.markdown('<div class="section-title">EXPLORATORY DATA ANALYSIS</div>', unsafe_allow_html=True)
    name, content = require_dataset()

    if content is not None and st.button("📊 Run EDA"):
        r = api_post("/eda", files=make_files(name, content))
        if r is not None:
            data = r.json()
            if "error" in data:
                st.error(data["error"])
            else:
                st.session_state.last_eda = data
                a,b = st.columns(2)
                a.metric("Rows",data.get("rows",0))
                b.metric("Columns",data.get("columns",0))
                st.subheader("Numerical Columns")
                st.write(data.get("numerical_columns",[]))
                st.subheader("Categorical Columns")
                st.write(data.get("categorical_columns",[]))

                if data.get("statistics"):
                    st.subheader("Statistical Summary")
                    st.dataframe(pd.DataFrame(data["statistics"]), width="stretch")

                if data.get("categorical_summary"):
                    st.subheader("Categorical Summary")
                    for col, values in data["categorical_summary"].items():
                        st.write(f"**{col}**")
                        st.dataframe(
                            pd.DataFrame(list(values.items()),columns=["Value","Count"]),
                            width="stretch"
                        )

                if data.get("correlation"):
                    st.subheader("Correlation Matrix")
                    corr = pd.DataFrame(data["correlation"])
                    st.dataframe(corr, width="stretch")
                    try:
                        fig = px.imshow(corr, text_auto=True, aspect="auto", title="Feature Correlation")
                        st.plotly_chart(fig, width="stretch")
                    except Exception:
                        pass
                st.success(data.get("status","EDA completed."))

# ========================= FEATURES =========================
elif page == "Feature Analysis":
    st.markdown('<div class="section-title">FEATURE ANALYSIS</div>', unsafe_allow_html=True)
    name, content = require_dataset()

    if content is not None and st.button("🧩 Analyze Features"):
        r = api_post("/features", files=make_files(name, content))
        if r is not None:
            data = r.json()
            if "error" in data:
                st.error(data["error"])
            else:
                st.success(data.get("status","Feature analysis completed."))
                a,b = st.columns(2)
                with a:
                    st.subheader("Numerical Features")
                    st.write(data.get("numerical_features",[]))
                with b:
                    st.subheader("Categorical Features")
                    st.write(data.get("categorical_features",[]))
                st.subheader("Feature Summary")
                st.json(data.get("feature_summary",{}))

# ========================= PREPROCESSING =========================
elif page == "Preprocessing":
    st.markdown('<div class="section-title">PREPROCESSING</div>', unsafe_allow_html=True)
    name, content = require_dataset()

    if content is not None and st.button("⚙️ Process Dataset"):
        r = api_post("/processing", files=make_files(name, content))
        if r is not None:
            data = r.json()
            if "error" in data:
                st.error(data["error"])
            else:
                st.metric("Processed Features",data.get("processed_columns",0))
                st.subheader("Processed Feature Names")
                st.write(data.get("processed_feature_names",[]))
                st.success(data.get("status","Preprocessing completed."))

# ========================= TRAINING =========================
elif page == "Model Training":
    st.markdown('<div class="section-title">MODEL TRAINING</div>', unsafe_allow_html=True)
    name, content = require_dataset()

    if content is not None:
        df = load_df(name, content)
        if df is not None and not df.empty:
            st.info("Select the column that the model should predict.")
            target = st.selectbox("Select Target Column",df.columns.tolist())
            st.write(
                f"Target: **{target}** | Type: **{df[target].dtype}** | "
                f"Unique values: **{df[target].nunique()}**"
            )

            if st.button("🤖 Train Models"):
                with st.spinner("Training models..."):
                    r = api_post(
                        "/train",
                        files=make_files(name,content),
                        data={"target_column":target},
                        timeout=300
                    )

                if r is not None:
                    data = r.json()
                    if "error" in data:
                        st.error(data["error"])
                    else:
                        st.session_state.last_training = data
                        st.success(data.get("status","Training completed."))
                        st.write("Problem Type:",data.get("problem_type","Unknown"))
                        results = data.get("results",{})
                        for model,result in results.items():
                            with st.expander(f"📈 {model}",expanded=True):
                                st.json(result)
                        st.info("Saved models are stored in the backend project's models/ folder.")

# ========================= PREDICTION =========================
elif page == "Prediction":
    st.markdown('<div class="section-title">MODEL PREDICTION</div>', unsafe_allow_html=True)
    st.info("Train a model first, then enter its saved filename and feature values as JSON.")

    model_name = st.text_input("Model filename",placeholder="random_forest_classifier.joblib")
    data_text = st.text_area(
        "Input data as JSON",
        placeholder='{"feature1": 10, "feature2": "value"}',
        height=160
    )

    if st.button("🔮 Predict"):
        if not model_name.strip():
            st.warning("Enter a model filename.")
        elif not data_text.strip():
            st.warning("Enter input JSON.")
        else:
            try:
                input_data = json.loads(data_text)
                if not isinstance(input_data,dict):
                    st.error("JSON input must be an object/dictionary.")
                else:
                    r = api_post(
                        "/predict",
                        json_data={"model_name":model_name.strip(),"data":input_data}
                    )
                    if r is not None:
                        result = r.json()
                        st.success(result.get("status","Prediction completed."))
                        st.json(result)
            except json.JSONDecodeError as e:
                st.error(f"Invalid JSON: {e}")

# ========================= INSIGHTS =========================
elif page == "AI Insights":
    st.markdown('<div class="section-title">AI DATA INSIGHTS</div>', unsafe_allow_html=True)
    name, content = require_dataset()

    if content is not None and st.button("🧠 Generate Insights"):
        with st.spinner("Generating insights..."):
            r = api_post("/insights",files=make_files(name,content),timeout=180)

        if r is not None:
            data = r.json()
            if "error" in data:
                st.error(data["error"])
            else:
                st.session_state.last_insights = data

                for insight in data.get("insights",[]):
                    st.info(f"💡 {insight}")

                if data.get("numerical_analysis"):
                    st.subheader("Numerical Analysis")
                    st.dataframe(pd.DataFrame(data["numerical_analysis"]),width="stretch")

                if data.get("categorical_analysis"):
                    st.subheader("Categorical Analysis")
                    st.dataframe(pd.DataFrame(data["categorical_analysis"]),width="stretch")

                if data.get("correlations"):
                    st.subheader("Feature Correlations")
                    corr = pd.DataFrame(data["correlations"])
                    st.dataframe(corr,width="stretch")
                    try:
                        fig = px.bar(
                            corr,x="feature_1",y="correlation",
                            color="feature_2",title="Feature Correlation Values"
                        )
                        st.plotly_chart(fig,width="stretch")
                    except Exception:
                        pass

                st.success(data.get("status","Insights generated successfully."))

# ========================= REPORT =========================
elif page == "Report":
    st.markdown('<div class="section-title">REPORT GENERATION</div>', unsafe_allow_html=True)
    name, content = require_dataset()

    if content is not None and st.button("📄 Generate Report"):
        with st.spinner("Generating report..."):
            r = api_post("/report",files=make_files(name,content),timeout=180)

        if r is not None:
            st.success("✅ Taksh AI report generated successfully!")
            st.download_button(
                "⬇️ Download HTML Report",
                data=r.text,
                file_name="taksh_ai_report.html",
                mime="text/html",
                width="stretch"
            )
            with st.expander("Preview Report"):
                st.components.v1.html(r.text,height=600,scrolling=True)
