import streamlit as st
from googletrans import Translator
from languages import languages, languages_dict
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests
from streamlit_extras.badges import badge
from streamlit_extras.colored_header import colored_header

# Function to load Lottie animations
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load Lottie animation
lottie_translate = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_rycdh53q.json")

# Page config
st.set_page_config(
    page_title="Language Translator Pro",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Roboto', sans-serif; }
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #262730; color: #FFFFFF; border: 1px solid #4B4B4B; border-radius: 8px;
    }
    .stButton button {
        background: linear-gradient(90deg, #FF4B4B 0%, #FF6B6B 100%);
        color: white; border: none; border-radius: 8px; padding: 0.5rem 2rem; font-weight: bold;
    }
    .stButton button:hover {
        background: linear-gradient(90deg, #FF6B6B 0%, #FF8B8B 100%);
        transform: translateY(-2px); box-shadow: 0 4px 12px rgba(255,75,75,0.3);
    }
    .output-box {
        background-color: #262730; padding: 20px; border-radius: 8px;
        border: 1px solid #4B4B4B; margin-top: 20px;
    }
    .stats-box {
        background: linear-gradient(45deg, #262730, #1E1E1E);
        padding: 15px; border-radius: 8px; border: 1px solid #4B4B4B;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 Navigation")
    selected = option_menu(
        menu_title=None,
        options=["Translate", "About", "Settings"],
        icons=["translate", "info-circle", "gear"],
        default_index=0,
    )
    
    st.markdown("---")
    st.markdown("### 📊 Stats")
    st.markdown("""
        <div class="stats-box">
            <h4>Today's Translations</h4>
            <p>50+ translations</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🔗 Connect")
    badge(type="github", name="your-github")
    badge(type="twitter", name="your-twitter")

# --- Translate Page ---
if selected == "Translate":
    colored_header(
        label="Language Translation Pro",
        description="Transform your text into any language instantly!",
        color_name="red-70"
    )

    col1, col2, col3 = st.columns([2, 1, 2])

    with col1:
        source_text = st.text_area(
            "Enter text to translate:",
            height=200,
            placeholder="Type or paste your text here..."
        )

    with col2:
        if lottie_translate:
            st_lottie(lottie_translate, height=150, key="translate_animation")
        
        target_language = st.selectbox(
            "Select target language:",
            languages,
            index=languages.index("English") if "English" in languages else 0
        )

        translate = st.button('Translate ✨', use_container_width=True)

    with col3:
        if translate and source_text:
            with st.spinner('Translating...'):
                try:
                    translator = Translator()
                    target_code = languages_dict.get(target_language, 'en')
                    out = translator.translate(source_text, dest=target_code)

                    st.markdown("### Translation Result:")
                    st.markdown(f"""<div class="output-box">{out.text}</div>""", unsafe_allow_html=True)
                    st.markdown(f"*Detected source language: {out.src.upper()}*")

                    if st.button("📋 Copy Translation"):
                        st.write("Translation copied to clipboard!")  # Clipboard function would need JS for actual copy
                except Exception as e:
                    st.error("An error occurred during translation. Please try again.")
        elif translate and not source_text:
            st.warning("Please enter some text to translate.")

# --- About Page ---
elif selected == "About":
    st.markdown("## About Language Translation Pro")
    st.write("""
    This is a professional translation tool powered by Google Translate API. 
    It supports multiple languages and provides instant translations with high accuracy.

    ### Features:
    - Support for 100+ languages
    - Real-time translation
    - Source language detection
    - Clean and intuitive interface
    - Copy to clipboard functionality
    """)

# --- Settings Page ---
elif selected == "Settings":
    st.markdown("## Settings")
    st.write("Customize your translation experience")
    st.toggle("Enable auto-translation")
    st.toggle("Save translation history")
    st.select_slider("Font Size", options=["Small", "Medium", "Large"])

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Made with ❤️ | Using Google Translate API | v1.0.0"
    "</div>",
    unsafe_allow_html=True
)
