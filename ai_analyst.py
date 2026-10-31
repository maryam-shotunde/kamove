from google import genai
import streamlit as st


def get_gemini_client():
    api_key = st.secrets["Gemma_API_key"]
    return genai.Client(api_key=api_key)

