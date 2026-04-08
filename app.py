import streamlit as st
import pandas as pd
import os
import urllib.parse
from datetime import datetime

# १. ॲप कॉन्फिगरेशन आणि संपूर्ण थीम फिक्स
st.set_page_config(page_title="Balaji Logistics", layout="centered")

st.markdown("""
    <style>
    /* संपूर्ण ॲप पांढऱ्या बॅकग्राउंडवर आणि काळ्या अक्षरात */
    .stApp {
        background-color: #ffffff !important;
    }
    
    /* सर्व इनपुट बॉक्सचे रंग स्पष्ट करणे */
    input {
        color: #000000 !important;
        background-color: #f8f9fa !important;
        border: 1px solid #0A3D62 !important;
    }
    
    /* लेबल आणि मजकूर काळा करणे */
    label, p, span, .stMarkdown {
        color: #000000 !important;
        font-weight: 500;
    }

    .main-card {
        background: #ffffff; 
        padding: 20px; 
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1); 
        border: 1px solid #dee2e6;
        margin-bottom: 20px;
    }

    .stButton>button {
        background-color: #0A3D62 !important; 
        color: white !important;
        border-radius: 8px; 
        height: 45px; 
        width: 100%;
        font-weight: bold;
    }
    
    h1, h2, h3 {
        color: #0A3D62 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# २. डेटाबेस फाईल्स
USER_DB = "users_data.csv"
BOOKING_DB = "bookings_data.csv"

for db, cols in [(USER_DB, ["Name", "Mobile", "Password"]), 
                 (BOOKING_DB, ["Time", "User", "Mobile", "From", "To", "Vehicle", "KM", "Fare", "Payment", "UTR"])]:
    if not os.path.exists(db):
        pd.DataFrame(columns=cols).to_csv(db, index=False)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- लॉगिन / रजिस्ट्रेशन विभाग ---
if not st.session_state.logged_in:
    if os.path.exists("1000326575.png"):
        st.image("1000326575.png", width=180)
    
    st.title("Balaji Logistics")
    
    # पर्याय निवडणे
    auth_mode = st.radio("निवडा:", ["Login", "Register"], horizontal=True)

    # पांढऱ्या कार्डमध्ये फॉर्म
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    if auth_mode == "Register":
        name = st.text_input("तुमचे पूर्ण नाव", key="reg_name")
    
    mob = st.text_input("मोबाईल नंबर", key="auth_mob")
    pwd = st.text_input("पासवर्ड", type="password", key="auth_pwd")
    
    if st.button("प्रवेश करा"):
        if auth_mode == "Register":
            if name and mob and pwd:
                df = pd.read_csv(USER_DB)
                if str(mob) in df['Mobile'].astype(str).values:
                    st.error("हा नंबर आधीच नोंदणीकृत आहे!")
                else:
                    pd.DataFrame([[name, mob, pwd]], columns=["Name", "Mobile", "Password"]).to_csv(USER_DB, mode='a', header=False, index=False)
                    st.success("नोंदणी झाली! आता 'Login' निवडून प्रवेश करा.")
            else:
                st.warning("कृपया सर्व माहिती भरा!")
        else:
            df = pd.read_csv(USER_DB)
            user = df[(df['Mobile'].astype(str) == str(mob)) & (df['Password'].astype(str) == str(pwd))]
            if not user.empty:
                st.session_state.logged_in = True
                st.session_state.user_name = user.iloc[0]['Name']
                st.session_state.user_mob = mob
                st.rerun()
            else:
                st.error("नंबर किंवा पासवर्ड चुकीचा आहे!")
    st.markdown('</div>', unsafe_allow_html=True)

# --- लॉगिन झाल्यानंतरचा बुकिंग विभाग ---
else:
    st.sidebar.title(f"नमस्ते, {st.session_state.user_name}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # Admin Panel
    if st.sidebar.checkbox("🔒 Admin Panel"):
        apwd = st.sidebar.text_input("Password", type="password")
        if apwd == "balaji123":
            st.subheader("📊 बुकिंग डेटा")
            st.dataframe(pd.read_csv(BOOKING_DB))

    st.header("🚖 तुमची गाडी बुक करा")
    
    # इथून पुढे तुमची कार लिस्ट आणि किलोमीटर कॅल्क्युलेटर सुरू होईल...
    # (जो आधीच्या कोडमध्ये दिला होता तोच इकडे जोडा)
    st.info("लॉगिन यशस्वी झाले आहे! आता तुम्ही प्रवासाची माहिती भरू शकता.")