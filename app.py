import streamlit as st
import pandas as pd
from recommender import load_data, recommend_schemes

# --- Set Page Config ---
st.set_page_config(
    page_title="PolicyPulse - Your Government Scheme Recommender",
    page_icon="🧭",
    layout="wide", # Crucial for wide layout
    initial_sidebar_state="collapsed"
)

# --- Custom CSS Styling ---
st.markdown("""
    <style>
    /* Color Palette:
       - Primary Blue: #2A6F97
       - Accent Green: #4CAF50
       - Background Light Grey: #F8F9FA
       - Card Background: #FFFFFF
       - Text Dark Grey: #343A40
       - Text Medium Grey: #6C757D
    */

    /* Overall App Background and Font */
    .stApp {
        background-color: #F8F9FA;
        font-family: 'Segoe UI', Arial, sans-serif;
        color: #343A40;
    }

    /* Target the main content container and remove default padding/margins - **REFINED** */
    .css-1d391kg { /* This is a common class for the main content block (might vary slightly) */
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: unset !important; /* Ensure no max-width on this parent container */
    }
    /* Addressed other possible Streamlit internal divs that might constrain width */
    .css-1dp5yy6 { /* Another common main content wrapper */
        max-width: unset !important;
    }
    .css-1r6dm1x { /* A div often wrapping columns */
        max-width: unset !important;
    }

    /* Header/Hero Section */
    .header-container {
        background-color: #2A6F97;
        padding: 50px 0;
        border-radius: 15px;
        margin-bottom: 40px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
        text-align: center;
    }

    .header-title {
        font-size: 4em;
        color: #ffffff;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 15px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }

    .header-subtitle {
        font-size: 1.6em;
        color: #e0e0e0;
        font-weight: 400;
        margin-bottom: 0;
    }

    /* Section Headers */
    h3 {
        color: #2A6F97;
        font-weight: 700;
        font-size: 2em;
        border-bottom: 3px solid #4CAF50;
        padding-bottom: 8px;
        margin-top: 50px;
        margin-bottom: 30px;
        text-align: left;
    }

    /* Custom Labels for Inputs */
    .custom-label {
        font-size: 1.15em;
        font-weight: 600;
        color: #343A40;
        margin-top: 20px;
        margin-bottom: 8px;
    }

    /* --- DROPDOWN TEXT VISIBILITY --- */
    div[data-baseweb="select"] * {
        color: #343A40 !important; /* Force all text inside to be dark */
    }

    div[data-baseweb="select"] > div {
        border-radius: 8px;
        border: 1px solid #ced4da;
        background-color: #ffffff;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.06);
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }

    div[data-baseweb="select"] > div:hover,
    div[data-baseweb="select"] > div:focus-within {
        border-color: #4CAF50;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.06), 0 0 0 0.2rem rgba(76, 175, 80, 0.25);
    }

    div[data-baseweb="select"] input[type="text"] {
        color: #343A40 !important;
        background-color: #ffffff !important;
        font-size: 1.05em;
        padding: 10px 12px;
    }

    div[data-baseweb="select"] input[type="text"]::placeholder {
        color: #6C757D !important;
    }

    div[data-baseweb="select"] svg {
        fill: #6C757D !important;
    }

    div[data-baseweb="select"] ul {
        background-color: #ffffff !important;
        border: 1px solid #ced4da !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
    }

    div[data-baseweb="select"] li {
        color: #343A40 !important;
        background-color: #ffffff !important;
        font-size: 1em;
        padding: 10px 15px;
    }

    div[data-baseweb="select"] li:hover {
        background-color: #E6F0E6 !important;
        color: #2A6F97 !important;
    }
    div[data-baseweb="select"] li[aria-selected="true"] {
        background-color: #D4EDDA !important;
        color: #2A6F97 !important;
        font-weight: 600;
    }


    /* Recommendation Button */
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 10px;
        font-weight: bold;
        font-size: 1.2em;
        transition: background-color 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease;
        margin-top: 40px;
        width: 100%;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    }

    .stButton>button:hover {
        background-color: #388E3C;
        transform: translateY(-3px);
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
    }

    /* Scheme Card Styling - **INCREASED SIZE** */
    .scheme-card {
        background-color: #ffffff;
        padding: 40px; /* Increased padding for more internal space */
        border-radius: 12px;
        margin-bottom: 30px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        color: #343A40;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        border-left: 5px solid #2A6F97;
        width: 100%;
        min-height: 200px; /* Add a minimum height to cards */
        min-width: 600px; /* Add a minimum width to cards, adjust as needed */
        max-width: unset !important; /* Ensure no external max-width limits */
        margin-left: auto;
        margin-right: auto;
    }

    .scheme-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }

    .scheme-card h4 {
        color: #2A6F97;
        margin-bottom: 15px;
        font-size: 2em; /* Slightly larger heading font */
        font-weight: 700;
    }

    .scheme-card p, .scheme-card b {
        color: #6C757D;
        line-height: 2; /* Increased line spacing for readability */
        font-size: 1.1em; /* Slightly larger body font */
    }

    /* Info/Success/Warning Messages */
    .stAlert {
        border-radius: 8px;
        padding: 18px;
        margin-top: 25px;
        font-size: 1.1em;
        max-width: unset !important; /* Ensure alerts can also be wide */
        margin-left: auto;
        margin-right: auto;
    }
    .stAlert > div > div > p {
        font-size: 1.1em;
        color: inherit;
    }

    /* Floating Chatbot Button */
    .chatbot-float {
        position: fixed;
        bottom: 35px;
        right: 35px;
        z-index: 9999;
    }

    .chatbot-float .stButton button {
        background-color: transparent;
        border: none;
        box-shadow: none;
        padding: 0;
        cursor: pointer;
    }

    .chatbot-float .stMarkdown {
        display: none;
    }

    .chatbot-float img {
        width: 75px;
        height: 75px;
        border-radius: 50%;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.45);
        transition: transform 0.2s ease;
        cursor: pointer;
    }

    .chatbot-float img:hover {
        transform: scale(1.15);
    }

    /* Footer */
    .footer-text {
        color: #6C757D;
        text-align: center;
        margin-top: 60px;
        padding: 25px 0;
        border-top: 1px solid #e9ecef;
        font-size: 0.95em;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header/Hero Section ---
st.markdown(
    """
    <div class="header-container">
        <div class="header-title">PolicyPulse</div>
        <div class="header-subtitle">Your Trusted Guide to Government Schemes & Policies</div>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Load scheme data ---
@st.cache_data
def load_scheme_data():
    return load_data("schemes.csv")

df = load_scheme_data()

# --- Main Content Area ---
st.markdown("<h3>🔍 Find Your Ideal Scheme</h3>", unsafe_allow_html=True)

# Use columns for a more organized input section
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="custom-label">Select your state (optional):</div>', unsafe_allow_html=True)
    unique_states = sorted(df['State'].dropna().unique().tolist())
    state = st.selectbox(" ", [""] + unique_states, key="state_select", label_visibility="collapsed")

with col2:
    st.markdown('<div class="custom-label">Select a keyword (optional):</div>', unsafe_allow_html=True)
    # Extract keyword list
    keywords_set = set()
    for col in ['Scheme Name', 'Eligibility', 'Benefit']:
        for val in df[col].fillna(""):
            for word in str(val).lower().replace('.', '').replace(',', '').split():
                if len(word) > 2:
                    keywords_set.add(word)
    unique_keywords = sorted(list(keywords_set))
    keyword = st.selectbox(" ", [""] + unique_keywords, key="keyword_select", label_visibility="collapsed")

# Centered button using a column trick
st.markdown("") # Add some space
search_button_col = st.columns([0.3, 0.4, 0.3])
with search_button_col[1]:
    if st.button("🎯 Get Scheme Recommendations"):
        if not state and not keyword:
            st.warning("Please select a state or keyword to get recommendations.")
        else:
            results = recommend_schemes(df, state, keyword)

            if not results:
                st.info("No matching schemes found. Try different keywords or states.")
            else:
                st.markdown(f"<h3>Results ({len(results)} Schemes)</h3>", unsafe_allow_html=True)
                # Display results in a central column to give them almost full perceived width
                # Slightly reduced side columns for even more width
                results_column = st.columns([0.01, 0.98, 0.01])
                with results_column[1]:
                    for scheme_data in results:
                        eligibility_text = scheme_data['eligibility'] if pd.notna(scheme_data['eligibility']) else 'N/A'
                        benefit_text = scheme_data['benefit'] if pd.notna(scheme_data['benefit']) else 'N/A'
                        st.markdown(f"""
                            <div class="scheme-card">
                                <h4>{scheme_data['name']}</h4>
                                <b>State:</b> {scheme_data['state'] if pd.notna(scheme_data['state']) else 'N/A'}<br>
                                <b>Eligibility:</b> {eligibility_text}<br>
                                <b>Benefit:</b> {benefit_text}
                            </div>
                        """, unsafe_allow_html=True)

# --- Placeholder for "About Us" or "How it Works" ---
st.markdown("<h3>💡 How PolicyPulse Works</h3>", unsafe_allow_html=True)
# Display "How it Works" in a central column as well, using the wider column ratio
how_it_works_col = st.columns([0.01, 0.98, 0.01]) # Use 98% width
with how_it_works_col[1]:
    st.markdown("""
        <div class="scheme-card">
        <p>PolicyPulse simplifies your search for government schemes. We leverage advanced filtering and a smart recommendation system to connect you with the policies that truly matter to you. </p>
        <p>Simply select your state (if applicable) and/or enter a keyword relevant to your interests (e.g., "education", "agriculture", "women empowerment", "housing", "health", "finance"). Click "Get Scheme Recommendations" to see tailored results instantly.</p>
        <p>Our goal is to make government information accessible and easy to understand, helping you unlock the benefits you deserve.</p>
        </div>
    """, unsafe_allow_html=True)

# --- Floating Chatbot Button (Styled) ---
st.markdown("""
    <a href="/chatbot_ui" target="_self" class="chatbot-float">
        <img src="https://cdn-icons-png.flaticon.com/512/4712/4712027.png" alt="Chatbot">
    </a>
""", unsafe_allow_html=True)

# --- Footer ---
st.markdown("---", unsafe_allow_html=True)
st.markdown('<div class="footer-text">Built with ❤️ by Greeshma | PolicyPulse © 2025 | All rights reserved.</div>', unsafe_allow_html=True)