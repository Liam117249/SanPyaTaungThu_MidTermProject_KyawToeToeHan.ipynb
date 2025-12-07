# 🌾 Myanmar Smart Farmer (Crop Recommendation System)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://smartfarmermm.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Scikit-Learn](https://img.shields.io/badge/Library-Scikit--Learn-orange)
![Accuracy](https://img.shields.io/badge/Accuracy-97%25-green)

A web app that helps farmers choose the best crop to grow. It uses Machine Learning to analyze soil nutrients (N, P, K) and weather conditions to recommend the perfect crop for high yield.

### 🔗 **[Click Here to Open App](https://smartfarmermm.streamlit.app/)**

---

## ✨ Features
* **🇲🇲 Bilingual:** Works in both **English** and **Myanmar (Burmese)**.
* **🧠 High Accuracy:** Uses the **K-Nearest Neighbors (KNN)** algorithm with **97% accuracy**.
* **🖼️ Visual Results:** Shows the predicted crop name along with a clear image.
* **💡 Smart Tips:** Gives specific farming advice for each crop (e.g., "Needs high water" or "Drought tolerant").
* **🧪 Soil Status:** Instantly tells if Nitrogen, Phosphorus, or pH levels are **Low**, **Optimal**, or **High**.
* **📥 Download Report:** Farmers can download the recommendation as a text file.

---

## 🛠️ Technical Details
* **Dataset:** 2200 samples of 22 different crops (Rice, Maize, Coffee, etc.).
* **Preprocessing:**
    * Used **KNN Imputer** to smartly fill missing values.
    * Used **MinMaxScaler** to scale features for better accuracy.
* **Model:** K-Nearest Neighbors (KNN) optimized with Hyperparameter Tuning.
* **App:** Built with **Streamlit** using custom CSS for a green agriculture theme.

---

## 📂 Files in this Repo
* **`app.py`**: The main code for the website interface.
* **`model.pkl`**: The saved model (KNN + Scaler + Imputer).
* **`crop_images/`**: Folder containing images for all crops.
* **`requirements.txt`**: List of Python libraries needed.
* **`TaungThu_MidTermProject.ipynb`**: The notebook used to train and test the model.

---

## 👨‍💻 Author
**Kyaw Toe Toe Han -**
**Parami University**
*/Mid-Term Project for ML Web App Development*
