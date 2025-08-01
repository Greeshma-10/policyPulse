# PolicyPulse: Your Guide to Government Schemes

**PolicyPulse** is a user-friendly web application designed to simplify the discovery and understanding of Indian government schemes and policies. Whether you're looking for education support, health benefits, agricultural assistance, or women's empowerment programs, PolicyPulse helps you find relevant schemes based on your **location**, **interests**, and **needs** — with the help of an intelligent chatbot.

---

## ✨ Features

### 🔐 Secure User Authentication
- Robust login & registration system.
- Passwords are **securely hashed** using SHA256.
- User credentials are stored in a local `config.yaml` file.

### 🧠 Intelligent Scheme Recommender
- **State-Based Filtering**: Choose your state to view relevant schemes.
- **Keyword Search**: Search by terms like _education_, _housing_, _women empowerment_, etc.
- **Tailored Results**: Combine filters for personalized scheme recommendations.

### 💬 Conversational Chatbot for Scheme Details
- Get a **comprehensive overview**, **eligibility criteria**, and **application process**.
- Ask follow-up questions conversationally.
- Transforms complex government documents into simple explanations.

### 🎨 Intuitive User Interface
- Built with **Streamlit** for a modern, responsive, and clean UI.
- Mobile-friendly card-based layout for easy browsing.

---

## 🚀 Getting Started

### ✅ Prerequisites
- Python 3.8 or higher
- `pip` package installer

### 🔧 Installation

1. Clone the repository:
```bash
git clone [your-repository-url]
cd policyPulse
```

2. Create and activate a virtual environment:
```bash
python -m venv streamlit_venv
streamlit_venv\Scripts\activate
```

## Install the required libraries:

1. Create a requirements.txt file:

```txt
streamlit
pandas
PyYAML
```
2. Then run:
```bash
pip install -r requirements.txt
```
3.Set up your configuration file:
Create a config.yaml file in the root directory with:

```yaml
credentials:
  usernames: {}
```
New users will automatically be added to this file when they register.

## ▶️ Running the Application
1. Activate your virtual environment.

2. Run the app:

```bash
streamlit run app.py
```
3. The app will open in your browser at: http://localhost:8501

### 🛠️ Usage
1. Login / Sign Up: First-time users can register via the sign-up form.

2. Find a Scheme: Use dropdowns and search to filter schemes.

3. Use the Chatbot: Ask detailed questions about any scheme via the chatbot in the sidebar.

## 📁 Project Structure
```pgsql

policyPulse/
├── .gitignore
├── app.py              # Main app logic and UI
├── 0_login.py          # Login & Registration
├── recommender.py      # Scheme recommendation logic
├── schemes.csv         # Dataset of government schemes
├── config.yaml         # Encrypted user credentials
└── streamlit_venv/     # Virtual environment (optional to commit)
```
## 👩‍💻 Credits
Built with ❤️ by Greeshma
