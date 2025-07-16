# {
#  "cells": [],
#  "metadata": {},
#  "nbformat": 4,
#  "nbformat_minor": 5
# }
import pandas as pd

def load_data(path):
    return pd.read_csv(path)

def recommend_schemes(df, state=None, keyword=None, top_n=5):
    df_filtered = df.copy()

    if state:
        df_filtered = df_filtered[df_filtered['State'].str.contains(state, case=False, na=False)]

    if keyword:
        keyword = keyword.lower()
        df_filtered = df_filtered[
            df_filtered['Scheme Name'].str.lower().str.contains(keyword) |
            df_filtered['Eligibility'].str.lower().str.contains(keyword) |
            df_filtered['Benefit'].str.lower().str.contains(keyword)
        ]

    if df_filtered.empty:
        return pd.DataFrame()

    def smart_truncate(text, max_chars=250):
        if not isinstance(text, str):
            return ""
        if len(text) <= max_chars:
            return text
        cutoff = text[:max_chars].rfind('.')
        if cutoff == -1:
            cutoff = text[:max_chars].rfind(' ')
        return text[:cutoff] + "..."

    df_filtered["Eligibility"] = df_filtered["Eligibility"].apply(smart_truncate)
    df_filtered["Benefit"] = df_filtered["Benefit"].apply(smart_truncate)

    return df_filtered[['State', 'Scheme Name', 'Eligibility', 'Benefit']].head(top_n)
