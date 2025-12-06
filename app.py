import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os

# --- 1. SETUP & TRANSLATIONS ---
st.set_page_config(page_title="Myanmar Smart Farmer", page_icon="🌾", layout="centered")

# Burmese Translation Dictionary
crop_dict_mm = {
    'rice': 'စပါး (Rice)', 'maize': 'ပြောင်း (Maize)', 'chickpea': 'ကုလားပဲ (Chickpea)',
    'kidneybeans': 'ပဲကြီး (Kidney Beans)', 'pigeonpeas': 'ပဲစင်းငုံ (Pigeon Peas)',
    'mothbeans': 'မတ်ပဲ (Moth Beans)', 'mungbean': 'ပဲတီစိမ်း (Mung Bean)',
    'blackgram': 'မတ်ပဲ (Black Gram)', 'lentil': 'ပဲနီလေး (Lentil)',
    'pomegranate': 'သလဲသီး (Pomegranate)', 'banana': 'ငှက်ပျော (Banana)',
    'mango': 'သရက်သီး (Mango)', 'grapes': 'စပျစ်သီး (Grapes)',
    'watermelon': 'ဖရဲသီး (Watermelon)', 'muskmelon': 'သခွားမွှေး (Muskmelon)',
    'apple': 'ပန်းသီး (Apple)', 'orange': 'လိမ္မော်သီး (Orange)',
    'papaya': 'သင်္ဘောသီး (Papaya)', 'coconut': 'အုန်းသီး (Coconut)',
    'cotton': 'ဝါ (Cotton)', 'jute': 'ဂုန်လျှော် (Jute)', 'coffee': 'ကော်ဖီ (Coffee)'
}

# --- 2. LOAD TOOLS ---
@st.cache_resource
def load_tools():
    with open('model.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

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
    .stApp {
        background: linear-gradient(to bottom right, #D9F2C7, #2E8B57);
        background-attachment: fixed;
    }
    .block-container {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        margin-top: 2rem;
        border: 2px solid #F0E68C;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .stButton>button {
        background-color: #006400;
        color: white;
        font-size: 20px;
        border-radius: 12px;
        height: 55px;
        border: 2px solid #D4AF37;
    }
    .stButton>button:hover {
        background-color: #228B22;
        border-color: white;
    }
    h1, h2, h3 {
        color: #006400;
        font-family: 'Padauk', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. APP INTERFACE ---

st.markdown("<h1 style='text-align: center;'>🌾 🌽 🍉</h1>", unsafe_allow_html=True)
st.title("Myanmar Smart Farmer")
st.subheader("မြန်မာတောင်သူကြီးများအတွက် သီးနှံရွေးချယ်ရန် အကူအညီ")
st.write("---")

col1, col2 = st.columns(2)
with col1:
    st.markdown("### 🌱 မြေဆီလွှာ (Soil)")
    N = st.slider("နိုက်ထရိုဂျင် (N)", 0, 140, 50)
    P = st.slider("ဖော့စဖရပ် (P)", 5, 145, 50)
    K = st.slider("ပိုတက်ဆီယမ် (K)", 5, 205, 50)
    ph = st.slider("မြေချဉ်ငံကိန်း (pH)", 0.0, 14.0, 6.5, step=0.1)
with col2:
    st.markdown("### 🌦️ ရာသီဥတု (Weather)")
    temperature = st.number_input("အပူချိန် (°C)", 0.0, 60.0, 25.0)
    humidity = st.number_input("စိုထိုင်းဆ (%)", 0.0, 100.0, 70.0)
    rainfall = st.number_input("မိုးရေချိန် (mm)", 0.0, 300.0, 100.0)

# --- 5. PREDICTION & LOCAL IMAGE DISPLAY ---
st.write("---")

if st.button("🔍 အသင့်တော်ဆုံး သီးနှံကို ရှာဖွေပါ (Find Best Crop)"):
    user_input = [[N, P, K, temperature, humidity, ph, rainfall]]
    user_input_scaled = scaler.transform(user_input)
    prediction = model.predict(user_input_scaled)
    result_english = prediction[0]
    result_myanmar = crop_dict_mm.get(result_english, result_english.upper())
    
    st.success(f"သင့်မြေအတွက် အသင့်တော်ဆုံး သီးနှံမှာ (Recommended Crop):")
    
    # 1. Show Text Result
    st.markdown(f"<h2 style='text-align: center; color: #006400;'>🌾 {result_myanmar} 🌾</h2>", unsafe_allow_html=True)
    
    # 2. Show Local Image
    # It looks for a file like "crop_images/rice.jpg" or "crop_images/maize.jpg"
    image_path = f"crop_images/{result_english}.png"
    
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        if os.path.exists(image_path):
            st.image(image_path, caption=f"{result_myanmar}", use_column_width=True)
        else:
            # If you forgot to upload the image, it shows a warning instead of crashing
            st.warning(f"⚠️ Image not found: {image_path}")
    
    # 3. Show Tips
    if result_english in ['rice', 'jute', 'coffee']:
        st.info("💡 **အကြံပြုချက်:** ဤသီးနှံသည် ရေများများ လိုအပ်ပါသည်။ (Needs plenty of water)")
    elif result_english in ['mothbeans', 'chickpea', 'mungbean', 'lentil']:
        st.info("💡 **အကြံပြုချက်:** ရေငတ်ဒဏ်ခံနိုင်သော သီးနှံဖြစ်သည်။ (Drought tolerant)")

st.markdown("---")
st.markdown("<div style='text-align: center;'>🍉 🌽 🌾</div>", unsafe_allow_html=True)
st.caption("Developed for Myanmar Agriculture | Student Project")
