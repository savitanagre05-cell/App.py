import streamlit as st

# १. अ‍ॅप सेटिंग्स (Mobile Friendly UI)
st.set_page_config(page_title="Balaji Logistics", page_icon="🚕", layout="wide")

# २. प्रीमियम CSS (Real App Look)
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; }
    /* टॉप हेडर */
    .app-header {
        background-color: black;
        color: white;
        padding: 15px;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        border-radius: 0 0 15px 15px;
        margin-bottom: 20px;
    }
    /* कार्ड स्टाईल */
    .app-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        border: 1px solid #eee;
    }
    /* भाडे कार्ड */
    .price-card {
        background-color: #e3f2fd;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #90caf9;
    }
    /* बटन्स */
    .stButton>button {
        width: 100%;
        background-color: black;
        color: white
