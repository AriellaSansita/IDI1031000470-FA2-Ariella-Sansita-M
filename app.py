import streamlit as st
import google.generativeai as genai
import os

# 🔐 Configure API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# --- UI Translation Function ---
def translate_ui(target_language):
    """Uses Gemini to translate the static UI labels into the target language."""
    # If English, return original labels to save API calls
    if target_language == "English":
        return {
            "title": "🌱 Smart Farming Assistant",
            "subtitle": "Get region-specific farming advice.",
            "loc_label": "Enter your location",
            "stage_label": "Select crop stage",
            "stages": ["Planting", "Growing", "Harvesting"],
            "const_label": "Constraints (e.g., organic-only)",
            "query_label": "Ask your farming question",
            "btn": "Get Advice",
            "output_head": "Farming Advice"
        }

    # Prompt Gemini to return a Python-style dictionary string
    translation_prompt = f"""
    Translate the following UI labels into {target_language}. 
    Keep the tone helpful and professional for farmers.
    Return ONLY a valid Python dictionary format.
    
    Labels to translate:
    - title: "Smart Farming Assistant"
    - subtitle: "Get region-specific farming advice."
    - loc_label: "Enter your location"
    - stage_label: "Select crop stage"
    - stages: ["Planting", "Growing", "Harvesting"]
    - const_label: "Constraints (e.g., organic-only)"
    - query_label: "Ask your farming question"
    - btn: "Get Advice"
    - output_head: "Farming Advice"
    """
    
    response = model.generate_content(translation_prompt)
    # Using eval() is risky in production; for a simple tool, we parse the text
    # In a real app, you'd use json.loads() and ask Gemini for JSON.
    try:
        return eval(response.text.strip().replace("```python", "").replace("```", ""))
    except:
        # Fallback to English if translation fails
        return translate_ui("English")

# --- App Setup ---
st.set_page_config(page_title="Smart Farmer", layout="centered")

# Sidebar for Language
languages = ["English", "Hindi", "Bengali", "Telugu", "Marathi", "Tamil", "Urdu", "Gujarati", "Kannada", "Odia", "Malayalam", "Punjabi", "Assamese", "Maithili", "Santali", "Kashmiri", "Nepali", "Konkani", "Sindhi", "Dogri", "Manipuri", "Bodo", "Sanskrit"]
selected_lang = st.sidebar.selectbox("🌐 Choose Language", languages)

# 🔄 Dynamic Translation (Cached to prevent re-running every click)
@st.cache_data
def get_cached_ui(lang):
    return translate_ui(lang)

ui = get_cached_ui(selected_lang)

# --- Main Interface ---
st.title(ui["title"])
st.write(ui["subtitle"])

col1, col2 = st.columns(2)
with col1:
    location = st.text_input(ui["loc_label"])
with col2:
    crop_stage = st.selectbox(ui["stage_label"], ui["stages"])

constraints = st.text_input(ui["const_label"])
query = st.text_area(ui["query_label"])

if st.button(ui["btn"]):
    if query:
        advice_prompt = (
            f"Context: {location}, Stage: {crop_stage}, Constraints: {constraints}. "
            f"Question: {query}. Respond in {selected_lang} using 3-5 simple bullet points."
        )
        
        with st.spinner("..."):
            response = model.generate_content(advice_prompt)
            
        st.divider()
        st.subheader(ui["output_head"])
        st.write(response.text)
    else:
        st.error("Please enter a question.")
