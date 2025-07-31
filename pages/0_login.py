import streamlit as st
import yaml
from yaml.loader import SafeLoader
import hashlib # For password hashing
import uuid # For generating unique user IDs

# --- Set Page Config for the Login Page ---
st.set_page_config(
    page_title="PolicyPulse Login/Signup",
    layout="centered", # Centered layout is good for login pages
    initial_sidebar_state="collapsed" # Hide sidebar initially
)

# --- Custom CSS Styling for Login Page (Matching app.py theme) ---
st.markdown("""
    <style>
    /* Consolidated from app.py for a consistent look and feel */
    body, .stApp {
        background-color: #FFFBDE; /* Main app background */
        font-family: 'Segoe UI', Arial, sans-serif;
        color: #343A40; /* Dark text */
    }
    /* Adjust padding for the main content block on login page */
    .main .block-container {
        padding-top: 4rem;
        padding-bottom: 4rem;
        max-width: 500px; /* Constrain width for login form */
        margin: 0 auto;
    }
    /* Header styling to match app.py and chatbot_ui.py */
    .header-container {
        background-color: #096B68; /* New primary accent for header background */
        padding: 35px 0;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
        text-align: center;
        width: 100%;
    }
    .header-title {
        font-size: 2.5em;
        color: #ffffff;
        font-weight: 800;
        letter-spacing: 1.8px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        margin: 0;
        line-height: 1.2;
    }
    /* Style for text input fields */
    .stTextInput > label {
        color: #343A40; /* Make labels visible */
        font-weight: 600;
        font-size: 1.05em;
        margin-top: 15px;
        margin-bottom: 5px;
    }
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 1px solid #ced4da;
        padding: 12px 15px;
        font-size: 1.05em;
        color: #343A40;
        background-color: #ffffff;
        box-shadow: inset 0 1px 4px rgba(0,0,0,0.08);
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .stTextInput > div > div > input:focus {
        border-color: #129990; /* Medium accent on focus */
        box-shadow: inset 0 1px 4px rgba(0,0,0,0.08), 0 0 0 0.2rem rgba(18, 153, 144, 0.25);
        outline: none;
    }
    /* Style for buttons */
    .stButton>button {
        background-color: #129990 !important; /* New medium accent for button */
        color: white !important; /* Ensure text color is white */
        border: none;
        padding: 12px 25px;
        border-radius: 10px;
        font-weight: bold;
        font-size: 1.1em;
        transition: background-color 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        width: 100%; /* Make buttons full width for login/signup */
        margin-top: 15px;
    }
    .stButton>button:hover {
        background-color: #096B68 !important; /* New primary accent on hover */
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
    }
    /* Style for headings */
    h2 {
        color: #096B68; /* Primary accent for headings */
        text-align: center;
        margin-bottom: 30px;
        font-size: 2.5em; /* Larger heading */
        font-weight: 700;
        border-bottom: 3px solid #129990; /* New medium accent for border */
        padding-bottom: 8px;
    }
    h3 {
        color: #096B68; /* Primary accent for headings */
        text-align: center;
        margin-top: 40px;
        margin-bottom: 20px;
        font-weight: 700;
        font-size: 2em;
        border-bottom: 3px solid #129990; /* New medium accent for border */
        padding-bottom: 8px;
    }
    /* Error/Warning messages */
    .stAlert {
        border-radius: 8px;
        padding: 15px;
        font-size: 1.05em;
        margin-bottom: 20px;
        max-width: 500px;
        margin-left: auto;
        margin-right: auto;
    }
    /* Override alert text color for visibility */
    .stAlert > div > div > p {
        color: #343A40 !important;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# --- Helper function for password hashing ---
def hash_password(password):
    """Hashes a password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

# --- Load config file ---
try:
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
except FileNotFoundError:
    st.error("Configuration file (config.yaml) not found. Please create it in the root directory with a 'credentials' section.")
    st.stop() # Stop the app if config is missing

# Ensure 'usernames' key exists in credentials
if 'usernames' not in config['credentials']:
    config['credentials']['usernames'] = {}
    # Optionally save the updated config if 'usernames' was missing
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

# Initialize session state for authentication status if not present
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None
if 'logged_in' not in st.session_state: # Our custom flag for access control
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None
if 'name' not in st.session_state:
    st.session_state['name'] = None

# --- Custom Header Section (matches chatbot header) ---
st.markdown(
    """
    <div class="header-container">
        <div class="header-title">PolicyPulse Access</div>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Custom Login Logic ---
if st.session_state['authentication_status'] is None or st.session_state['authentication_status'] == False:
    st.subheader("Login")
    login_username = st.text_input("Username", key="login_username_input")
    login_password = st.text_input("Password", type="password", key="login_password_input")

    if st.button("Login", key="login_button"):
        if login_username in config['credentials']['usernames']:
            user_data = config['credentials']['usernames'][login_username]
            hashed_password_in_config = user_data.get('password') # 'password' key stores hashed password
            name_in_config = user_data.get('name')

            if hashed_password_in_config and hash_password(login_password) == hashed_password_in_config:
                st.session_state['authentication_status'] = True
                st.session_state['logged_in'] = True
                st.session_state['username'] = login_username
                st.session_state['name'] = name_in_config
                st.success(f'Welcome, {name_in_config}! You are now logged in.')
                st.info("You can now navigate to PolicyPulse from the sidebar.")
                st.rerun() # Rerun to update the page immediately
            else:
                st.error('Username/password is incorrect')
        else:
            st.error('Username/password is incorrect')
elif st.session_state['authentication_status'] == True:
    st.success(f'Welcome, {st.session_state["name"]}! You are already logged in.')
    st.info("You can now navigate to PolicyPulse from the sidebar.")


# --- Custom Registration Logic ---
if st.session_state['authentication_status'] == False or st.session_state['authentication_status'] is None:
    st.markdown("---")
    st.markdown("<h3>New User? Sign Up!</h3>", unsafe_allow_html=True)

    with st.form("registration_form"):
        new_name = st.text_input("Name", key="reg_name")
        new_username = st.text_input("New Username (Email)", key="reg_username")
        new_password = st.text_input("New Password", type="password", key="reg_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm_password")

        submitted = st.form_submit_button("Register")

        if submitted:
            if not new_name or not new_username or not new_password or not confirm_password:
                st.warning("Please fill in all fields.")
            elif new_password != confirm_password:
                st.error("Passwords do not match.")
            elif new_username in config['credentials']['usernames']:
                st.error("Username already exists. Please choose a different one.")
            else:
                try:
                    hashed_new_password = hash_password(new_password)
                    # Add new user to config
                    config['credentials']['usernames'][new_username] = {
                        'email': new_username, # Storing email as username for consistency
                        'name': new_name,
                        'password': hashed_new_password, # Store hashed password
                        'id': str(uuid.uuid4()) # Unique ID for the user
                    }

                    # Save updated config back to file
                    with open('config.yaml', 'w') as file:
                        yaml.dump(config, file, default_flow_style=False)
                    st.success('User registered successfully! Please login.')
                    st.rerun() # Rerun to clear form and show login
                except Exception as e:
                    st.error(f"Error during registration: {e}")

# --- Custom Logout Logic (in sidebar) ---
if st.session_state['logged_in']:
    with st.sidebar:
        st.markdown(f"**Welcome, {st.session_state['name']}!**")
        if st.button("Logout", key="logout_button"):
            st.session_state['authentication_status'] = None
            st.session_state['logged_in'] = False
            st.session_state['username'] = None
            st.session_state['name'] = None
            st.success("You have been logged out.")
            st.rerun() # Rerun to show login page
