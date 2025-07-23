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

    /* Floating chatbot icon */
    .chatbot-float {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 9999;
    }

    .chatbot-float .stButton button {
        background-color: transparent;
        border: none;
        box-shadow: none;
        padding: 0;
    }

    .chatbot-float .stMarkdown {
        display: none; /* hides label container */
    }

    .chatbot-float img {
        width: 70px;
        height: 70px;
        border-radius: 50%;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
        transition: transform 0.2s ease;
        cursor: pointer;
    }

    .chatbot-float img:hover {
        transform: scale(1.1);
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="title">🧠 PolicyPulse</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Find the best government schemes tailored to you</div>', unsafe_allow_html=True)
st.markdown("")

# Load scheme data
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
        for word in str(val).split(): # Ensure val is string before split
            if len(word) > 3:
                keywords_set.add(word.lower())
unique_keywords = sorted(list(keywords_set)) # Convert set to list

# Custom labels
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

        if not results: # Check if the list is empty
            st.info("No matching schemes found. Try different keywords or states.")
        else:
            st.success(f"Found {len(results)} scheme(s):")
            for scheme_data in results: # Iterate over the list of dictionaries
                st.markdown(f"""
                    <div class="scheme-card">
                        <h4>{scheme_data['name']}</h4>
                        <b>State:</b> {scheme_data['state']}<br>
                        <b>Eligibility:</b> {scheme_data['eligibility']}<br>
                        <b>Benefit:</b> {scheme_data['benefit']}
                    </div>
                """, unsafe_allow_html=True)

# Floating Chatbot Button (Styled)
st.markdown("""
    <a href="/chatbot_ui" target="_self" class="chatbot-float">
        <img src="https://cdn-icons-png.flaticon.com/512/4712/4712027.png" alt="Chatbot">
    </a>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption('<div style="color:black">"Built with ❤️ by Greeshma | Powered by Streamlit"</div>', unsafe_allow_html=True)