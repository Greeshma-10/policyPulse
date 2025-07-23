import pandas as pd

def load_data(path="schemes.csv"):
    return pd.read_csv(path)

def smart_truncate(text, max_chars=250):
    if not isinstance(text, str):
        return ""
    if len(text) <= max_chars:
        return text
    cutoff = text[:max_chars].rfind('.')
    if cutoff == -1:
        cutoff = text[:max_chars].rfind(' ')
    return text[:cutoff] + "..."

def recommend_schemes(df, state=None, keyword=None, top_n=5):
    df_filtered = df.copy()

    if state:
        df_filtered = df_filtered[df_filtered['State'].str.contains(state, case=False, na=False)]

    if keyword:
        keyword = keyword.lower()
        df_filtered = df_filtered[
            df_filtered['Scheme Name'].str.lower().str.contains(keyword, na=False) | # Added na=False for robustness
            df_filtered['Eligibility'].str.lower().str.contains(keyword, na=False) |
            df_filtered['Benefit'].str.lower().str.contains(keyword, na=False)
        ]

    if df_filtered.empty:
        return [] # Return an empty list if no schemes are found

    df_filtered["Eligibility"] = df_filtered["Eligibility"].apply(smart_truncate)
    df_filtered["Benefit"] = df_filtered["Benefit"].apply(smart_truncate)

    responses = []
    for _, row in df_filtered.head(top_n).iterrows():
        # Return a dictionary with individual components
        scheme_dict = {
            "name": row['Scheme Name'],
            "state": row['State'],
            "eligibility": row['Eligibility'],
            "benefit": row['Benefit']
        }
        responses.append(scheme_dict)
    return responses

# Optional helper function to be called by chatbot (no changes needed here unless you want to return dicts)
def get_recommendations(state=None, keyword=None, top_n=5):
    df = load_data()
    return recommend_schemes(df, state, keyword, top_n)