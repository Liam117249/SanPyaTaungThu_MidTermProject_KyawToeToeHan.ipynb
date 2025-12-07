# 🌾 Myanmar Smart Farmer (AI Crop Recommendation System)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://smartfarmermm.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Scikit-Learn](https://img.shields.io/badge/Library-Scikit--Learn-orange)
![Accuracy](https://img.shields.io/badge/Model%20Accuracy-96%25-green)

A Machine Learning web application designed to assist Myanmar farmers in practicing **Precision Agriculture**. This tool predicts the optimal crop to cultivate based on specific soil nutrients (Nitrogen, Phosphorus, Potassium) and environmental conditions (Temperature, Humidity, Rainfall, pH).

### 🔗 **Live Demo:** [Click Here to Open App](https://smartfarmermm.streamlit.app/)

---

## 📖 Project Overview
Agriculture is the backbone of Myanmar's economy. However, traditional farming often relies on guesswork, leading to lower yields and soil degradation. 

**Smart Farmer** solves this by using the **K-Nearest Neighbors (KNN)** algorithm to analyze soil data and recommend the scientifically best crop. It bridges the gap between complex data science and rural farmers through a bilingual, user-friendly interface.

---

## ✨ Key Features
* **🇲🇲 Bilingual Interface:** Full support for **English** and **Myanmar (Burmese)** languages, making it accessible to local farmers.
* **🧠 AI-Powered Prediction:** Uses a trained KNN model to classify crops with **96% accuracy**.
* **🧪 Real-Time Soil Analysis:** Instantly visualizes if soil nutrients (N, P, K) or pH levels are **Low 🔴**, **Optimal 🟢**, or **High 🔴** as the user adjusts inputs.
* **💡 Smart Agricultural Tips:** Provides specific cultivation advice for every predicted crop (e.g., water requirements for Rice vs. drought tolerance for Moth Beans).
* **📥 Digital Prescription:** Allows farmers to download a `.txt` report of their soil status and recommendation to take to agriculture supply shops.
* **🖼️ Visual Results:** Displays high-quality images of the recommended crop for easy identification.

---

## 🛠️ Technical Architecture

### 1. Data Pipeline (`TaungThu_MidTermProject.ipynb`)
* **Dataset:** [Crop Recommendation Dataset](https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset) (2200 samples, 22 crops).
* **Preprocessing:** * **Data Cleaning:** Handled missing values using **`KNNImputer`** (Mastery Level) to preserve data integrity.
    * **Feature Scaling:** Applied **`MinMaxScaler`** to normalize features (e.g., Rainfall 200mm vs pH 6.5) for distance-based calculations.
* **Model Selection:** * Chosen Algorithm: **K-Nearest Neighbors (KNN)**.
    * Why? KNN effectively captures the spatial similarity of soil clusters (e.g., "If neighboring soil points grow Rice, this point likely grows Rice too").
* **Evaluation:**
    * Achieved **96% Accuracy** on the test set.
    * Verified using **Confusion Matrix**, **Precision**, **Recall**, and **F1-Score**.

### 2. Web Interface (`app.py`)
* Built with **Streamlit**.
* Implements **Session State** for a seamless "Welcome Screen" to "Main App" transition.
* Uses custom **CSS** for the "Green/Gold" agricultural theme and styling.

---

## 📂 Repository Structure
