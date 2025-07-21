import streamlit as st
import pandas as pd
from recommender import load_data, recommend_schemes

# Set page config
st.set_page_config(
    page_title="PolicyPulse - Scheme Recommender",
    page_icon="🧭",
    layout="wide"
)

# Custom CSS styling
st.markdown("""
    <style>
    .stApp {
        background-color: #ADEED9 !important;
    }

    section.main > div {
        background-color: #ADEED9 !important;
    }

    .title {
        font-size: 2.5em;
        color: #0ABAB5;
        font-weight: bold;
        text-align: center;
    }

    .subtitle {
        font-size: 1.2em;
        font-weight: 500;
        text-align: center;
        color: #000000;
        margin-bottom: 20px;
    }

    .custom-label {
        font-size: 1.1em;
        font-weight: 600;
        color: #000000;
        margin-top: 10px;
    }

    .scheme-card {
        background-color: #56DFCF;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
        color: #000000;
    }

    .scheme-card h4 {
        color: #0ABAB5;
        margin-bottom: 8px;
    }

    .scheme-card p, .scheme-card b {
        color: #000000;
    }

    .stButton>button {
        background-color: #0ABAB5;
        color: white;
        border: none;
        padding: 10px 18px;
        border-radius: 8px;
        font-weight: bold;
    }

    .stButton>button:hover {
        background-color: #068e8e;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="title">🧠 PolicyPulse</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Find the best government schemes tailored to you</div>', unsafe_allow_html=True)
st.markdown("")

# Load data
@st.cache_data
def load_scheme_data():
    return load_data("schemes.csv")

df = load_scheme_data()

# Filters
st.markdown('<h3 style="color: black;">🔍 Filter Options</h3>', unsafe_allow_html=True)
unique_states = sorted(df['State'].dropna().unique().tolist())

# Extract keyword list
keywords_set = set()
for col in ['Scheme Name', 'Eligibility', 'Benefit']:
    for val in df[col].fillna(""):
        for word in val.split():
            if len(word) > 3:
                keywords_set.add(word.lower())
unique_keywords = sorted(keywords_set)

# Custom labels with black text
st.markdown('<div class="custom-label">Select your state (optional):</div>', unsafe_allow_html=True)
state = st.selectbox("", [""] + unique_states)

st.markdown('<div class="custom-label">Select a keyword (optional):</div>', unsafe_allow_html=True)
keyword = st.selectbox("", [""] + unique_keywords)

# Recommendation logic
if st.button("🎯 Get Scheme Recommendations"):
    if not state and not keyword:
        st.warning("Please select a state or keyword to get recommendations.")
    else:
        results = recommend_schemes(df, state, keyword)

        if results.empty:
            st.info("No matching schemes found. Try different keywords or states.")
        else:
            st.success(f"Found {len(results)} scheme(s):")
            for _, row in results.iterrows():
                st.markdown(f"""
                    <div class="scheme-card">
                        <h4>{row['Scheme Name']}</h4>
                        <b>State:</b> {row['State']}<br>
                        <b>Eligibility:</b> {row['Eligibility']}<br>
                        <b>Benefit:</b> {row['Benefit']}
                    </div>
                """, unsafe_allow_html=True)

# ✅ Link to chatbot (already handled correctly by you!)
st.page_link("pages/chatbot_ui.py", label="💬 Open Chatbot Assistant", icon="🤖")

# Footer
st.markdown("---")
st.caption('<div style="color:black">"Built with ❤️ by Greeshma | Powered by Streamlit"</div>', unsafe_allow_html=True)