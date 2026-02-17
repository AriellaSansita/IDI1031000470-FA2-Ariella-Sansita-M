import streamlit as st
import google.generativeai as genai
import os

# 🔐 Configure API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# --- 🚀 Instant Load Translation Dictionary ---
# I've pre-filled the main ones. You can add more blocks for other languages.
translations = {
    "English": {
        "title": "🌱 Smart Farming Assistant",
        "loc": "Enter location",
        "stage": "Crop stage",
        "stages": ["Planting", "Growing", "Harvesting"],
        "const": "Constraints (e.g. Organic)",
        "ask": "Your question",
        "btn": "Get Advice",
        "header": "Advice"
    },
    "Hindi": {
        "title": "🌱 स्मार्ट खेती सहायक",
        "loc": "स्थान दर्ज करें",
        "stage": "फसल का चरण",
        "stages": ["बुवाई", "बढ़त", "कटाई"],
        "const": "सीमाएं (जैसे: जैविक)",
        "ask": "आपका प्रश्न",
        "btn": "सलाह लें",
        "header": "सुझाव"
    },
    "Tamil": {
        "title": "🌱 ஸ்மார்ட் விவசாய உதவியாளர்",
        "loc": "இருப்பிடத்தை உள்ளிடவும்",
        "stage": "பயிர் நிலை",
        "stages": ["நடவு", "வளர்ச்சி", "அறுவடை"],
        "const": "கட்டுப்பாடுகள் (எ.கா. இயற்கை)",
        "ask": "உங்கள் கேள்வி",
        "btn": "ஆலோசனை பெறுங்கள்",
        "header": "ஆலோசனை"
    },
    "Telugu": {
        "title": "🌱 స్మార్ట్ ఫార్మింగ్ అసిస్టెంట్",
        "loc": "ప్రాంతాన్ని నమోదు చేయండి",
        "stage": "పంట దశ",
        "stages": ["నాటడం", "పెరుగుదల", "కోత"],
        "const": "పరిమితులు (ఉదా: సేంద్రీయ)",
        "ask": "మీ ప్రశ్న",
        "btn": "సలహా పొందండి",
        "header": "సలహా"
    }
}

# --- 🛠️ Helper Logic ---
languages = ["English", "Hindi", "Tamil", "Telugu", "Bengali", "Marathi", "Kannada", "Malayalam", "Gujarati", "Punjabi"]

# Sidebar Language Selection
selected_lang = st.sidebar.selectbox("🌐 Language / भाषा", languages)

# Fallback to English if translation isn't in our dictionary yet
ui = translations.get(selected_lang, translations["English"])

# --- 🖥️ User Interface ---
st.title(ui["title"])

col1, col2 = st.columns(2)
with col1:
    location = st.text_input(ui["loc"])
with col2:
    crop_stage = st.selectbox(ui["stage"], ui["stages"])

constraints = st.text_input(ui["const"])
query = st.text_area(ui["ask"])

if st.button(ui["btn"]):
    if query.strip():
        # The prompt still asks for the response in the selected language
        prompt = (
            f"Location: {location}, Stage: {crop_stage}, Constraints: {constraints}. "
            f"Question: {query}. Respond ONLY in {selected_lang} in 3-5 simple points."
        )
        
        with st.spinner("..."):
            response = model.generate_content(prompt)
            
        st.subheader(ui["header"])
        st.write(response.text)
    else:
        st.warning("Please enter a question.")
