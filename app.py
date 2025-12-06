import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os

# --- 1. SETUP & DATA ---
st.set_page_config(page_title="Smart Farmer", page_icon="🌾", layout="centered")

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
        'acidic': "Acidic", 'neutral': "Neutral", 'alkaline': "Alkaline"
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
        'acidic': "အချဉ်ဓာတ်များ", 'neutral': "သာမန်", 'alkaline': "အငန်ဓာတ်များ"
    }
}

# B. CROP DATA
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
