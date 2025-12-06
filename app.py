import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os

# --- 1. SETUP & DATA ---
st.set_page_config(page_title="Smart Farmer", page_icon="🌾", layout="centered")

# Initialize Session State for Page Navigation
if 'page' not in st.session_state:
    st.session_state['page'] = 'welcome'

# A. TRANSLATIONS
translations = {
    'en': {
        'title': "Smart Crop Recommendation System",
        'subheader': "AI-powered tool to help farmers select the best crop.",
        'soil_header': "🌱 Soil Condition",
        'weather_header': "🌦️ Weather Conditions",
        'nitrogen': "Nitrogen (N)",
        'phosphorus': "Phosphorus (P)",
        'potassium': "Potassium (K)",
        'ph': "Soil pH Level",
        'temp': "Temperature (°C)",
        'humidity': "Humidity (%)",
        'rain': "Rainfall (mm)",
        'predict_btn': "🔍 Find Best Crop",
        'result_msg': "The most suitable crop for your farm is:",
        'tip_header': "💡 Agricultural Tip:",
        'download_btn': "📥 Download Report",
        'footer': "Developed for Agriculture | Student Project",
        'low': "Low", 'optimal': "Optimal", 'high': "High",
        'acidic': "Acidic", 'neutral': "Neutral", 'alkaline': "Alkaline",
        'welcome_title': "Welcome to Smart Farmer",
        'welcome_sub': "Your companion for smarter agriculture decisions.",
        'start_btn': "🚀 Get Started"
    },
    'mm': {
        'title': "မြန်မာစမတ်တောင်သူ (Smart Farmer)",
        'subheader': "မြန်မာတောင်သူကြီးများအတွက် သီးနှံရွေးချယ်ရန် အကူအညီ",
        'soil_header': "🌱 မြေဆီလွှာ အခြေအနေ",
        'weather_header': "🌦️ ရာသီဥတု အခြေအနေ",
        'nitrogen': "နိုက်ထရိုဂျင် (N)",
        'phosphorus': "ဖော့စဖရပ် (P)",
        'potassium': "ပိုတက်ဆီယမ် (K)",
        'ph': "မြေချဉ်ငံကိန်း (pH)",
        'temp': "အပူချိန် (°C)",
        'humidity': "စိုထိုင်းဆ (%)",
        'rain': "မိုးရေချိန် (mm)",
        'predict_btn': "🔍 အသင့်တော်ဆုံး သီးနှံကို ရှာဖွေပါ",
        'result_msg': "သင့်မြေအတွက် အသင့်တော်ဆုံး သီးနှံမှာ -",
        'tip_header': "💡 စိုက်ပျိုးရေး အကြံပြုချက် -",
        'download_btn': "📥 မှတ်တမ်းသိမ်းဆည်းမည်",
        'footer': "မြန်မာ့စိုက်ပျိုးရေးအတွက် တီထွင်ထားသည် | ကျောင်းသားပရောဂျက်",
        'low': "နည်းလွန်းသည်", 'optimal': "သင့်တင့်သည်", 'high': "များလွန်းသည်",
        'acidic': "အချဉ်ဓာတ်များ", 'neutral': "သာမန်", 'alkaline': "အငန်ဓာတ်များ",
        'welcome_title': "မြန်မာစမတ်တောင်သူ မှ ကြိုဆိုပါတယ်",
        'welcome_sub': "တိကျသော စိုက်ပျိုးရေးနည်းပညာဖြင့် အထွက်နှုန်းတိုးပွားစေရန်",
        'start_btn': "🚀 စတင်အသုံးပြုမည်"
    }
}

# B. CROP DATA (Names & Tips)
crop_names = {
    'rice': {'mm': 'စပါး', 'en': 'Rice'}, 'maize': {'mm': 'ပြောင်း', 'en': 'Maize'},
    'chickpea': {'mm': 'ကုလားပဲ', 'en': 'Chickpea'}, 'kidneybeans': {'mm': 'ပဲကြီး', 'en': 'Kidney Beans'},
    'pigeonpeas': {'mm': 'ပဲစင်းငုံ', 'en': 'Pigeon Peas'}, 'mothbeans': {'mm': 'မတ်ပဲ', 'en': 'Moth Beans'},
    'mungbean': {'mm': 'ပဲတီစိမ်း', 'en': 'Mung Bean'}, 'blackgram': {'mm': 'မတ်ပဲ (Black Gram)', 'en': 'Black Gram'},
    'lentil': {'mm': 'ပဲနီလေး', 'en': 'Lentil'}, 'pomegranate': {'mm': 'သလဲသီး', 'en': 'Pomegranate'},
    'banana': {'mm': 'ငှက်ပျော', 'en': 'Banana'}, 'mango': {'mm': 'သရက်သီး', 'en': 'Mango'},
    'grapes': {'mm': 'စပျစ်သီး', 'en': 'Grapes'}, 'watermelon': {'mm': 'ဖရဲသီး', 'en': 'Watermelon'},
    'muskmelon': {'mm': 'သခွားမွှေး', 'en': 'Muskmelon'}, 'apple': {'mm': 'ပန်းသီး', 'en': 'Apple'},
    'orange': {'mm': 'လိမ္မော်သီး', 'en': 'Orange'}, 'papaya': {'mm': 'သင်္ဘောသီး', 'en': 'Papaya'},
    'coconut': {'mm': 'အုန်းသီး', 'en': 'Coconut'}, 'cotton': {'mm': 'ဝါ', 'en': 'Cotton'},
    'jute': {'mm': 'ဂုန်လျှော်', 'en': 'Jute'}, 'coffee': {'mm': 'ကော်ဖီ', 'en': 'Coffee'}
}

crop_tips = {
    'rice': {'mm': 'စပါးသည် ရေကို အလွန်နှစ်သက်သဖြင့် ရေဝပ်သော လယ်ကွင်းများတွင် စိုက်ပျိုးရန် အသင့်တော်ဆုံးဖြစ်သည်။', 'en': 'Rice loves water! Best grown in flooded fields.'},
    'maize': {'mm': 'ရေစီးရေလာကောင်းမွန်သော မြေတွင် ကောင်းစွာဖြစ်ထွန်းသည်။ ရေဝပ်ဒဏ် မခံနိုင်ပါ။', 'en': 'Needs well-drained soil. Avoid waterlogging.'},
    'watermelon': {'mm': 'သဲဆန်သော မြေတွင် အကောင်းဆုံး ဖြစ်ထွန်းသည်။', 'en': 'Best grown in sandy soil.'},
    'default': {'mm': 'မြေဆီလွှာ အစိုဓာတ်နှင့် အာဟာရကို ဂရုစိုက်ပါ။', 'en': 'Ensure proper soil nutrition and moisture management.'}
}

# --- 2. LOAD TOOLS ---
@st.cache_resource
def load_tools():
    with open('model.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

def get_soil_status(value, type, lang_dict):
    if type == 'N':
        if value < 50: return f"🔴 {lang_dict['low']}"
        elif value > 120: return f"🔴 {lang_dict['high']}"
        return f"🟢 {lang_dict['optimal']}"
    elif type == 'pH':
        if value < 5.5: return f"🟠 {lang_dict['acidic']}"
        elif value > 7.5: return f"🔵 {lang_dict['alkaline']}"
        return f"🟢 {lang_dict['neutral']}"
    return ""

try:
    data = load_tools()
    model = data['model']
    scaler = data['scaler']
except FileNotFoundError:
    st.error("⚠️ Model file not found. Please upload 'model.pkl'.")
    st.stop()

# --- 3. CUSTOM CSS ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp { background: linear-gradient(to bottom right, #D9F2C7, #2E8B57); background-attachment: fixed; }
    
    /* Content Box */
    .block-container { background-color: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 2rem; margin-top: 2rem; border: 2px solid #F0E68C; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
    
    /* Header Box */
    .header-box { background-color: #006400; padding: 20px; border-radius: 15px; margin-bottom: 30px; text-align: center; border: 2px solid #D4AF37; }
    .header-box h1 { color: white !important; font-family: 'Padauk', sans-serif; font-size: 32px; margin-bottom: 10px; }
    .header-box h3 { color: #e8f5e9 !important; font-family: 'Padauk', sans-serif; font-size: 18px; font-weight: normal; }
    
    /* Welcome Screen Box */
    .welcome-box { text-align: center; padding: 50px; }
    .welcome-icon { font-size: 80px; margin-bottom: 20px; display: block; }
    
    /* Buttons */
    .stButton>button { background-color: #006400; color: white; font-size: 20px; border-radius: 12px; height: 55px; border: 2px solid #D4AF37; width: 100%; }
    .stButton>button:hover { background-color: #228B22; border-color: white; transform: scale(1.02); }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] { background-color: #006400; border-right: 2px solid #D4AF37; }
    [data-testid="stSidebar"] * { color: white !important; }
    
    .tip-box { background-color: #e8f5e9; border-left: 5px solid #006400; padding: 15px; border-radius: 5px; margin-top: 15px; }
    h3 { color: #006400; font-family: 'Padauk', sans-serif; }
    </style>
""", unsafe_allow_html=True)

# --- 4. NAVIGATION LOGIC ---

def show_welcome():
    # Simple Language Toggle for Welcome Screen
    lang_welcome = st.radio("Language / ဘာသာစကား", ["English", "မြန်မာ"], horizontal=True)
    lang_code = 'en' if lang_welcome == "English" else 'mm'
    txt = translations[lang_code]

    st.markdown(f"""
        <div class="welcome-box">
            <span class="welcome-icon">🌾</span>
            <div class="header-box">
                <h1>{txt['welcome_title']}</h1>
            </div>
            <h3>{txt['welcome_sub']}</h3>
            <br>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(txt['start_btn']):
            st.session_state['page'] = 'main'
            st.rerun()

def show_main_app():
    # Sidebar Language Switcher
    st.sidebar.header("Language / ဘာသာစကား")
    language_choice = st.sidebar.radio("", ["English", "မြန်မာ"], index=0)
    lang = 'en' if language_choice == "English" else 'mm'
    txt = translations[lang]

    # Main Interface
    st.markdown(f"""<div class="header-box"><h1>🌾 {txt['title']} 🌾</h1><h3>{txt['subheader']}</h3></div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"### {txt['soil_header']}")
        N = st.slider(txt['nitrogen'], 0, 140, 50)
        st.caption(get_soil_status(N, 'N', txt))
        P = st.slider(txt['phosphorus'], 5, 145, 50)
        K = st.slider(txt['potassium'], 5, 205, 50)
        ph = st.slider(txt['ph'], 0.0, 14.0, 6.5, step=0.1)
        st.caption(get_soil_status(ph, 'pH', txt))

    with col2:
        st.markdown(f"### {txt['weather_header']}")
        temperature = st.number_input(txt['temp'], 0.0, 60.0, 25.0)
        humidity = st.number_input(txt['humidity'], 0.0, 100.0, 70.0)
        rainfall = st.number_input(txt['rain'], 0.0, 300.0, 100.0)

    st.write("---")
    
    if st.button(txt['predict_btn']):
        user_input = [[N, P, K, temperature, humidity, ph, rainfall]]
        user_input_scaled = scaler.transform(user_input)
        prediction = model.predict(user_input_scaled)
        result_raw = prediction[0]
        
        display_name = crop_names.get(result_raw, {}).get(lang, result_raw.upper())
        tip_text = crop_tips.get(result_raw, crop_tips['default']).get(lang, "")
        
        st.success(txt['result_msg'])
        st.markdown(f"<h2 style='text-align: center; color: #006400;'>🌾 {display_name} 🌾</h2>", unsafe_allow_html=True)
        
        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_center:
            st.image(f"crop_images/{result_raw}.png", caption=display_name, use_column_width=True)
                
        st.markdown(f"""<div class="tip-box"><b>{txt['tip_header']}</b><br>{tip_text}</div>""", unsafe_allow_html=True)
        
        report_text = f"{txt['title']}\n--------------------\n{txt['soil_header']}:\nN: {N}, P: {P}, K: {K}, pH: {ph}\n\n{txt['result_msg']} {display_name}\n\n{txt['tip_header']} {tip_text}"
        st.download_button(label=txt['download_btn'], data=report_text, file_name="crop_recommendation.txt", mime="text/plain")
    
    st.markdown("---")
    # Back to Home Button
    if st.button("🏠 Home / ပင်မစာမျက်နှာ"):
        st.session_state['page'] = 'welcome'
        st.rerun()
    st.caption(txt['footer'])

# --- 5. RUN APP ---
if st.session_state['page'] == 'welcome':
    show_welcome()
else:
    show_main_app()
