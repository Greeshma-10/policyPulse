import streamlit as st
import pandas as pd
from recommender import load_data, recommend_schemes # Assuming this is correct

# Initialize logged_in status if not set (important for direct page access)
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- Conditional Content Display ---
if not st.session_state['logged_in']:
    st.set_page_config(
        page_title="PolicyPulse - Login Required",
        page_icon="🧭",
        layout="centered",
        initial_sidebar_state="collapsed" # Collapse sidebar when not logged in
    )
    st.markdown("""
        <style>
        body, .stApp { background-color: #FFFBDE; font-family: 'Segoe UI', Arial, sans-serif; color: #343A40; }
        .main .block-container { padding-top: 4rem; text-align: center; }
        h2 { color: #096B68; margin-bottom: 20px; font-size: 2.5em; }
        p { font-size: 1.1em; color: #6C757D; margin-bottom: 30px; }
        </style>
    """, unsafe_allow_html=True)
    st.markdown("<h2>Access Denied</h2>", unsafe_allow_html=True)
    st.markdown("<p>Please log in to access PolicyPulse. Navigate to the 'Login' page in the sidebar.</p>", unsafe_allow_html=True)

else:
    # --- START OF YOUR ORIGINAL app.py CONTENT (INDENT ALL OF IT) ---
    st.set_page_config(
        page_title="PolicyPulse - Your Government Scheme Recommender",
        page_icon="🧭",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # --- Custom CSS Styling (ensure this matches your latest full app.py CSS) ---
    st.markdown("""
        <style>
        /* New Color Palette (from https://colorhunt.co/palette/fffbde90d1ca129990096b68):
            - Background: #FFFBDE
            - Lighter Accent (selection/hover): #90D1CA
            - Medium Accent (buttons, borders): #129990
            - Primary Accent (headers, strong lines): #096B68

            - Card Background: #FFFFFF (retained for contrast)
            - Text Dark: #343A40 (retained for readability)
            - Text Medium: #6C757D (retained for readability)
        */

        /* Overall App Background and Font */
        .stApp {
            background-color: #FFFBDE; /* New main background color */
            font-family: 'Segoe UI', Arial, sans-serif; /* Consistent font */
            color: #343A40; /* Consistent dark grey text */
        }

        /* Target the main content container and remove default padding/margins for true wide layout */
        .css-1d391kg, .css-1dp5yy6, .css-1r6dm1x, .css-1sp8zjk { /* Common Streamlit wrappers for wide mode */
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            max-width: unset !important; /* Ensure no max-width on these parent containers */
        }

        /* Header/Hero Section */
        .header-container {
            background-color: #096B68; /* New primary accent for header background */
            padding: 50px 0;
            border-radius: 15px;
            margin-bottom: 40px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
            text-align: center;
            width: calc(100% - 40px);
            margin: 0 auto;
            max-width: 1200px;
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
            color: #096B68; /* New primary accent for section headers */
            font-weight: 700;
            font-size: 2em;
            border-bottom: 3px solid #129990; /* New medium accent for border */
            padding-bottom: 8px;
            margin-top: 50px;
            margin-bottom: 30px;
            text-align: left;
            max-width: 900px;
            margin-left: auto;
            margin-right: auto;
        }

        /* Custom Labels for Inputs */
        .custom-label {
            font-size: 1.15em;
            font-weight: 600;
            color: #343A40;
            margin-top: 20px;
            margin-bottom: 8px;
        }

        /* --- DROPDOWN (Selectbox) Styling --- */
        div[data-baseweb="select"] * {
            color: #343A40 !important; /* Force all text inside to be dark */
        }

        div[data-baseweb="select"] > div {
            border-radius: 10px;
            border: 1px solid #ced4da;
            background-color: #ffffff;
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.06);
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }

        div[data-baseweb="select"] > div:hover,
        div[data-baseweb="select"] > div:focus-within {
            border-color: #129990; /* New medium accent on hover/focus */
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.06), 0 0 0 0.2rem rgba(18, 153, 144, 0.25); /* Adjusted rgba based on new accent */
        }

        div[data-baseweb="select"] input[type="text"] {
            color: #343A40 !important;
            background-color: #ffffff !important;
            font-size: 1.05em;
            padding: 12px 15px;
        }

        div[data-baseweb="select"] input[type="text"]::placeholder {
            color: #6C757D !important;
        }

        div[data-baseweb="select"] svg {
            fill: #6C757D !important;
        }

        div[data-baseweb="select"] ul { /* Dropdown options list */
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
            background-color: #90D1CA !important; /* New lighter accent on hover for options */
            color: #096B68 !important; /* New primary accent text on hover */
        }
        div[data-baseweb="select"] li[aria-selected="true"] {
            background-color: #90D1CA !important; /* New lighter accent for selected option */
            color: #096B68 !important; /* New primary accent text for selected option */
            font-weight: 600;
        }

        /* Recommendation Button */
        .stButton>button {
            background-color: #129990; /* New medium accent for button */
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
            background-color: #096B68; /* New primary accent on hover */
            transform: translateY(-3px);
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
        }

        /* Scheme Card Styling */
        .scheme-card {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 25px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            color: #343A40;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            border-left: 5px solid #096B68; /* New primary accent left border */
            width: 100%;
            min-height: 180px;
            max-width: 900px;
            margin-left: auto;
            margin-right: auto;
        }

        .scheme-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }

        .scheme-card h4 {
            color: #096B68; /* New primary accent for card headings */
            margin-bottom: 12px;
            font-size: 1.8em;
            font-weight: 700;
        }

        .scheme-card p, .scheme-card b {
            color: #6C757D;
            line-height: 1.8;
            font-size: 1.05em;
        }

        /* Info/Success/Warning Messages */
        .stAlert {
            border-radius: 8px;
            padding: 18px;
            margin-top: 25px;
            font-size: 1.1em;
            max-width: 900px;
            margin-left: auto;
            margin-right: auto;
        }
        .stAlert > div > div > p {
            font-size: 1.1em;
            color: inherit;
        }

        /* Floating Chatbot Icon (Static, for guidance) */
        .chatbot-float-container {
            position: fixed;
            bottom: 35px;
            right: 35px;
            z-index: 9999;
            cursor: pointer;
        }

        .chatbot-float-icon {
            width: 75px;
            height: 75px;
            border-radius: 50%;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.45);
            transition: transform 0.2s ease;
        }

        .chatbot-float-icon:hover {
            transform: scale(1.15);
        }

        /* Custom tooltip for the icon */
        .chatbot-tooltip {
            visibility: hidden;
            background-color: rgba(0, 0, 0, 0.7);
            color: #fff;
            text-align: center;
            border-radius: 6px;
            padding: 5px 10px;
            position: absolute;
            z-index: 1;
            bottom: 100%; /* Position the tooltip above the icon */
            left: 50%;
            margin-left: -70px; /* Center the tooltip */
            width: 140px;
        }

        .chatbot-float-container:hover .chatbot-tooltip {
            visibility: visible;
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
    input_section_cols = st.columns([0.1, 0.8, 0.1])
    with input_section_cols[1]:
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown('<div class="custom-label">Select your state (optional):</div>', unsafe_allow_html=True)
            unique_states = sorted(df['State'].dropna().unique().tolist())
            state = st.selectbox(" ", [""] + unique_states, key="state_select", label_visibility="collapsed")

        with col2:
            st.markdown('<div class="custom-label">Select a keyword (optional):</div>', unsafe_allow_html=True)
            keywords_set = set()
            for col_name in ['Scheme Name', 'Eligibility', 'Benefit']:
                for val in df[col_name].fillna(""):
                    for word in str(val).lower().replace('.', '').replace(',', '').split():
                        if len(word) > 2:
                            keywords_set.add(word)
            unique_keywords = sorted(list(keywords_set))
            keyword = st.selectbox(" ", [""] + unique_keywords, key="keyword_select", label_visibility="collapsed")

    # Centered button
    with input_section_cols[1]:
        st.markdown("")
        search_button_col = st.columns([0.2, 0.6, 0.2])
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
                        inner_results_column = st.columns([0.01, 0.98, 0.01])
                        with inner_results_column[1]:
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
    how_it_works_col = st.columns([0.01, 0.98, 0.01])
    with how_it_works_col[1]:
        st.markdown("""
            <div class="scheme-card">
            <p>PolicyPulse simplifies your search for government schemes. We leverage advanced filtering and a smart recommendation system to connect you with the policies that truly matter to you. </p>
            <p>Simply select your state (if applicable) and/or enter a keyword relevant to your interests (e.g., "education", "agriculture", "women empowerment", "housing", "health", "finance"). Click "Get Scheme Recommendations" to see tailored results instantly.</p>
            <p>Our goal is to make government information accessible and easy to understand, helping you unlock the benefits you deserve.</p>
            </div>
        """, unsafe_allow_html=True)

    # --- Floating Chatbot Icon (Directs user to sidebar) ---
    st.markdown("""
        <div class="chatbot-float-container">
            <img src="https://cdn-icons-png.flaticon.com/512/4712/4712027.png" alt="Chatbot" class="chatbot-float-icon">
            <span class="chatbot-tooltip">Click the chatbot icon in the sidebar!</span>
        </div>
    """, unsafe_allow_html=True)

    # --- Footer ---
    st.markdown("---", unsafe_allow_html=True)
    st.markdown('<div class="footer-text">Built with ❤️ by Greeshma | PolicyPulse © 2025 | All rights reserved.</div>', unsafe_allow_html=True)
