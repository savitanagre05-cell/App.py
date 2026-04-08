import streamlit as st
import pandas as pd
import os
import urllib.parse
from datetime import datetime

# १. ॲप कॉन्फिगरेशन आणि कलर फिक्स (CSS)
st.set_page_config(page_title="Balaji Logistics", layout="centered")

# हे CSS कोड अक्षरांना काळ्या रंगात ठेवण्यास मदत करेल
st.markdown("""
    <style>
    /* सर्व टेक्स्ट काळ्या रंगात करण्यासाठी */
    .stApp, div[data-baseweb="input"] input, label, p, .stMarkdown {
        color: #000000 !important;
    }
    .stApp { background-color: #ffffff !important; }
    
    .main-card {
        background: white; padding: 25px; border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-top: 8px solid #0A3D62;
        margin-bottom: 20px;
        color: black;
    }
    .stButton>button {
        background-color: #0A3D62 !important; color: white !important;
        border-radius: 10px; height: 50px; font-weight: bold;
    }
    h1, h2, h3 { color: #0A3D62 !important; }
    </style>
    """, unsafe_allow_html=True)

# २. डेटाबेस सेटअप
USER_DB = "users_data.csv"
BOOKING_DB = "bookings_data.csv"

for db, cols in [(USER_DB, ["Name", "Mobile", "Password"]), 
                 (BOOKING_DB, ["Time", "User", "Mobile", "From", "To", "Vehicle", "KM", "Fare", "Payment", "UTR"])]:
    if not os.path.exists(db):
        pd.DataFrame(columns=cols).to_csv(db, index=False)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- लॉगिन / रजिस्ट्रेशन ---
if not st.session_state.logged_in:
    if os.path.exists("1000326575.png"):
        st.image("1000326575.png", width=200)
    
    st.title("Balaji Logistics")
    st.subheader("Welcome")
    
    # इथे रंगाचा प्रॉब्लेम येणार नाही
    auth_mode = st.radio("निवडा:", ["Login", "Register"], horizontal=True)

    with st.container():
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        name = st.text_input("पूर्ण नाव") if auth_mode == "Register" else ""
        mob = st.text_input("मोबाईल नंबर")
        pwd = st.text_input("पासवर्ड", type="password")
        
        if st.button("प्रवेश करा"):
            if auth_mode == "Register":
                df = pd.read_csv(USER_DB)
                if str(mob) in df['Mobile'].astype(str).values:
                    st.error("नंबर आधीच आहे!")
                else:
                    pd.DataFrame([[name, mob, pwd]], columns=["Name", "Mobile", "Password"]).to_csv(USER_DB, mode='a', header=False, index=False)
                    st.success("नोंदणी झाली! आता लॉगिन करा.")
            else:
                df = pd.read_csv(USER_DB)
                user = df[(df['Mobile'].astype(str) == str(mob)) & (df['Password'].astype(str) == str(pwd))]
                if not user.empty:
                    st.session_state.logged_in = True
                    st.session_state.user_name = user.iloc[0]['Name']
                    st.session_state.user_mob = mob
                    st.rerun()
                else:
                    st.error("माहिती चुकीची आहे!")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # (बाकीचा बुकिंगचा कोड जो आधी दिला होता तोच राहील)
    st.sidebar.write(f"नमस्ते, {st.session_state.user_name}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
    st.success("तुम्ही लॉगिन झाले आहात! आता बुकिंग करा.")
    # ... तुमचा पुढचा बुकिंग कोड ...