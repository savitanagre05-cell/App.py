import streamlit as st
import pandas as pd

# १. अ‍ॅप सेटिंग्स (Real App Look & Feel)
st.set_page_config(page_title="Balaji Logistics Pro", page_icon="🚕", layout="wide")

# २. मास्टर CSS (Professional Mobile App UI)
st.markdown("""
    <style>
    /* बॅकग्राउंड आणि फॉन्ट */
    .stApp { background-color: #F8F9FA; }
    
    /* टॉप हेडर (Sticky Header) */
    .app-header {
        background-color: black;
        color: white;
        padding: 15px;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        border-radius: 0 0 20px 20px;
        margin-bottom: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }

    /* मुख्य कार्ड्स डिझाइन */
    .app-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.0
