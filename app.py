import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os

# set up and data
st.set_page_config(page_title="Smart Farmer", page_icon="🌾", layout="centered")

# Start Session State
if 'page' not in st.session_state:
    st.session_state['page'] = 'welcome'

# create translations for both Myanmar and English Languages
translations = {
    'en': {
        'title': "Smart Crop Recommendation System",
        'subheader': "To help farmers select the best crop.",
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
        'title': "စံပြတောင်သူ",
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
        'welcome_title': "စံပြတောင်သူမှ ကြိုဆိုပါတယ်",
        'welcome_sub': "တိကျသော စိုက်ပျိုးရေးနည်းပညာဖြင့် အထွက်နှုန်းတိုးပွားစေရန် ရည်ရွယ်ပါသည်",
        'start_btn': "🚀 စတင်အသုံးပြုမည်"
    }
}

# I add crop data in both langaugaes
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
    'coconut': {'mm': 'အုန်းသီး', 'en': 'Coconut'}, 'cotton': {'mm': 'ဝါဂွမ်း', 'en': 'Cotton'},
    'jute': {'mm': 'ဂုန်လျှော်', 'en': 'Jute'}, 'coffee': {'mm': 'ကော်ဖီ', 'en': 'Coffee'}
}

# I write unique tips for each crops that will show after result
crop_tips = {
    'rice': {
        'mm': 'စပါးသည် ရေကို အလွန်နှစ်သက်သဖြင့် ရေဝပ်သော လယ်ကွင်းများတွင် စိုက်ပျိုးရန် အသင့်တော်ဆုံးဖြစ်သည်။',
        'en': 'Rice loves water! Best grown in flooded fields or areas with high water retention.'
    },
    'maize': {
        'mm': 'ရေစီးရေလာကောင်းမွန်သော မြေတွင် ကောင်းစွာဖြစ်ထွန်းသည်။ ရေဝပ်ဒဏ် မခံနိုင်ပါ။',
        'en': 'Corn needs well-drained soil. Ensure the field does not hold stagnant water.'
    },
    'chickpea': {
        'mm': 'ဆောင်းရာသီတွင် စိုက်ပျိုးရန် အသင့်တော်ဆုံးဖြစ်သည်။ အစိုဓာတ် အနည်းငယ်သာ လိုအပ်သည်။',
        'en': 'Best grown in the winter season. Requires very little moisture.'
    },
    'kidneybeans': {
        'mm': 'သဲနုန်းမြေတွင် ကောင်းစွာ ဖြစ်ထွန်းသည်။ ပေါင်းလိုက်ခြင်းကို ဂရုစိုက်လုပ်ဆောင်ပါ။',
        'en': 'Thrives in sandy loam soil. Weeding is essential for good yield.'
    },
    'pigeonpeas': {
        'mm': 'ခြောက်သွေ့ဒဏ်ခံနိုင်သော ပဲအမျိုးအစားဖြစ်သည်။ သဲဆန်သောမြေတွင်လည်း စိုက်ပျိုးနိုင်သည်။',
        'en': 'Highly drought-resistant. Can grow well even in sandy soils.'
    },
    'mothbeans': {
        'mm': 'အလွန်ခြောက်သွေ့သော ရာသီဥတုတွင်လည်း စိုက်ပျိုးနိုင်သည်။ ရေအနည်းဆုံးဖြင့် အောင်မြင်နိုင်သည်။',
        'en': 'The most drought-tolerant legume. Can grow with very little water.'
    },
    'mungbean': {
        'mm': 'သက်တမ်းတို သီးနှံဖြစ်၍ သီးထပ်အဖြစ် စိုက်ပျိုးရန် အထူးသင့်တော်သည်။',
        'en': 'Short duration crop. Perfect for rotation between rice seasons.'
    },
    'blackgram': {
        'mm': 'ရေထိန်းနိုင်သော မြေစေးနုန်းမြေကို ကြိုက်နှစ်သက်သည်။ အစိုဓာတ်ထိန်းသိမ်းရန် အရေးကြီးသည်။',
        'en': 'Prefers clay loam soil that retains moisture. Avoid waterlogging.'
    },
    'lentil': {
        'mm': 'အေးမြသော ရာသီဥတုကို ကြိုက်နှစ်သက်သည်။ မြေဆီလွှာ အာဟာရပြည့်ဝရန် လိုအပ်သည်။',
        'en': 'Prefers cool weather. Requires nutrient-rich soil for best growth.'
    },
    'pomegranate': {
        'mm': 'ခြောက်သွေ့သော ဒေသများတွင် ကောင်းစွာ ဖြစ်ထွန်းသည်။ ရေသွင်းစိုက်ပျိုးပါက အထွက်နှုန်းကောင်းသည်။',
        'en': 'Thrives in dry areas. Irrigation improves fruit quality significantly.'
    },
    'banana': {
        'mm': 'ရေနှင့် အစိုဓာတ် များစွာ လိုအပ်သည်။ လေပြင်းတိုက်ခတ်ဒဏ်ကို ကာကွယ်ပေးရန် လိုအပ်သည်။',
        'en': 'Needs plenty of water and moisture. Protect from strong winds.'
    },
    'mango': {
        'mm': 'မြေသားနက်သော နုန်းမြေတွင် အကောင်းဆုံး ဖြစ်ထွန်းသည်။ နေရောင်ခြည် ကောင်းစွာရရှိရန် လိုအပ်သည်။',
        'en': 'Grows best in deep, loamy soil. Requires full sun exposure.'
    },
    'grapes': {
        'mm': 'ကိုင်းဖြတ်ပြုပြင်ခြင်း (Pruning) စနစ်တကျ ပြုလုပ်ရန် လိုအပ်သည်။ စင်တင်စိုက်ပျိုးရမည်။',
        'en': 'Requires regular pruning and a trellis system for support.'
    },
    'watermelon': {
        'mm': 'သဲဆန်သော မြေတွင် အကောင်းဆုံး ဖြစ်ထွန်းသည်။ ရေကို ပုံမှန်သွင်းပေးရန် လိုအပ်သည်။',
        'en': 'Best grown in sandy soil. Requires regular watering but good drainage.'
    },
    'muskmelon': {
        'mm': 'ပူနွေးခြောက်သွေ့သော ရာသီဥတုကို ကြိုက်နှစ်သက်သည်။ ရင့်မှည့်ချိန်တွင် ရေလျှော့ပေးပါ။',
        'en': 'Prefers hot and dry climate. Reduce water during ripening.'
    },
    'apple': {
        'mm': 'အေးမြသော တောင်ပေါ်ဒေသများတွင်သာ စိုက်ပျိုးနိုင်သည်။ အပူချိန်နိမ့်ရန် လိုအပ်သည်။',
        'en': 'Requires a cool climate. Best suited for hilly regions.'
    },
    'orange': {
        'mm': 'ရေစီးရေလာကောင်းမွန်သော တောင်ကုန်းမြေများတွင် ဖြစ်ထွန်းသည်။ အမြစ်ပုပ်ရောဂါ သတိပြုပါ။',
        'en': 'Needs well-drained soil, often on slopes. Watch out for root rot.'
    },
    'papaya': {
        'mm': 'ရေဝပ်ဒဏ် မခံနိုင်ပါ။ ရေစီးရေလာ ကောင်းမွန်ရမည်။ နေရောင်ခြည် အပြည့်အဝ လိုအပ်သည်။',
        'en': 'Very sensitive to waterlogging. Needs excellent drainage and full sun.'
    },
    'coconut': {
        'mm': 'ပူအိုက်စိုစွတ်သော ကမ်းရိုးတန်းဒေသများတွင် အကောင်းဆုံးဖြစ်သည်။ ဆားငန်ရေဒဏ် ခံနိုင်ရည်ရှိသည်။',
        'en': 'Thrives in humid coastal areas. Tolerant to saline water.'
    },
    'cotton': {
        'mm': 'မြေနက်တွင် အကောင်းဆုံး ဖြစ်ထွန်းသည်။ ပူနွေးသော ရာသီဥတု လိုအပ်သည်။',
        'en': 'Grows best in black soil. Requires a hot climate and frost-free days.'
    },
    'jute': {
        'mm': 'မြစ်ရေဝင်သော မြေနုကျွန်းများတွင် စိုက်ပျိုးရန် သင့်တော်သည်။ မိုးများသော ဒေသများတွင် ဖြစ်ထွန်းသည်။',
        'en': 'Best suited for alluvial soil in floodplains. Needs heavy rainfall.'
    },
    'coffee': {
        'mm': 'အရိပ်ပင်များအောက်တွင် စိုက်ပျိုးရန် လိုအပ်သည်။ အေးမြသော တောင်ပေါ်ဒေသများနှင့် ကိုက်ညီသည်။',
        'en': 'Needs shade trees. Best suited for cool, hilly regions.'
    },
    'default': {
        'mm': 'မြေဆီလွှာ အစိုဓာတ်နှင့် အာဟာရကို ဂရုစိုက်ပါ။',
        'en': 'Ensure proper soil nutrition and moisture management.'
    }
}

# load tools and add values for better user experience
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

# this is the place I customized bg, font color and box color 
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

    /* Welcome Screen */
    .welcome-box { text-align: center; padding: 40px; }
    .welcome-icon { font-size: 80px; margin-bottom: 20px; display: block; }

    /* Buttons */
    .stButton>button { background-color: #006400; color: white; font-size: 20px; border-radius: 12px; height: 55px; border: 2px solid #D4AF37; width: 100%; }
    .stButton>button:hover { background-color: #228B22; border-color: white; transform: scale(1.02); }

    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #006400; border-right: 2px solid #D4AF37; }
    [data-testid="stSidebar"] * { color: white !important; }

    .tip-box { background-color: #e8f5e9; border-left: 5px solid #006400; padding: 15px; border-radius: 5px; margin-top: 15px; }
    h3 { color: #006400; font-family: 'Padauk', sans-serif; }
    </style>
""", unsafe_allow_html=True)

# Navigation for both languages

def show_welcome():
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


    # I use columns [5, 3, 5] to place the middle column to the center to make equal "empty space" on both sides
    col1, col2, col3 = st.columns([5, 3, 5])
    with col2:
        if st.button(txt['start_btn']):
            st.session_state['page'] = 'main'
            st.rerun()

def show_main_app():
    st.sidebar.header("Language / ဘာသာစကား")
    language_choice = st.sidebar.radio("", ["English", "မြန်မာ"], index=0)
    lang = 'en' if language_choice == "English" else 'mm'
    txt = translations[lang]

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

# run the app
if st.session_state['page'] == 'welcome':
    show_welcome()
else:
    show_main_app()
