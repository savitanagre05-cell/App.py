import streamlit as st
import time
import pandas as pd
import os
import hashlib

# १. तुझे अपडेटेड नंबर्स आणि डेटाबेस
WA_LINK_NO = "919767981986"  
CONTACT_NO = "9767981986"    
PAYMENT_NO = "9309146504"    
USER_DB = "users_data.csv"   

st.set_page_config(page_title="Balaji Logistics", layout="wide")

# २. फीचर्स (No Changes)
def make_hashes(password): return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password, hashed_text): return make_hashes(password) == hashed_text

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "Home"

# ३. स्टाईल - काळा लूक आणि ग्रिड मेनूसाठी
st.markdown("""
    <style>
    header, footer, #MainMenu {visibility: hidden;}
    .stApp { background-color: #000; color: white; }
    
    /* ४x३ ग्रिड मेनू बॉक्स */
    .menu-container {
        background-color: #111; padding: 15px; border-radius: 20px 20px 0 0;
        border-top: 2.5px solid #FFBB00; position: fixed; bottom: 0; left: 0; right: 0; z-index: 1000;
    }
    
    /* बटनांची कडक स्टाईल */
    div.stButton > button {
        background-color: transparent !important; color: white !important;
        border: none !important; font-size: 14px !important; width: 100%;
    }
    .active-btn button { color: #FFBB00 !important; font-weight: bold !important; }
    </style>
""", unsafe_allow_html=True)

# ४. लॉगिन सिस्टिम
if not st.session_state.logged_in:
    st.markdown("<h2 style='color:#FFBB00; text-align:center;'>🚖 BALAJI LOGIN</h2>", unsafe_allow_html=True)
    u = st.text_input("Username")
    p = st.text_input("Password", type='password')
    if st.button("Access App"):
        if os.path.isfile(USER_DB):
            users = pd.read_csv(USER_DB)
            if u in users['username'].values and check_hashes(p, users[users['username'] == u]['password'].values[0]):
                st.session_state.logged_in = True; st.session_state.user = u; st.rerun()
else:
    # ५. होम पेज - औरा गाडीसह
    if st.session_state.page == "Home":
        st.markdown("<h2 style='color:#FFBB00; text-align:center;'>🚩 ALL INDIA SERVICE</h2>", unsafe_allow_html=True)
        # Hyundai Aura Photo
        st.image("https://imgd.aeplcdn.com/664x374/n/cw/ec/141125/aura-exterior-right-front-three-quarter.jpeg?isig=0&q=80")
        st.markdown("<h4 style='text-align:center;'>💰 दर: १३ रुपये / किमी</h4>", unsafe_allow_html=True)
        st.write(f"Welcome, {st.session_state.user}!")

    # ६. बुकिंग पेज
    elif st.session_state.page == "Booking":
        st.subheader("📝 नवीन बुकिंग")
        with st.form("book_form"):
            s = st.text_input("From"); e = st.text_input("To")
            v = st.selectbox("Vehicle", ["WagonR", "Swift Dzire", "Ertiga", "Innova", "Tempo"])
            km = st.number_input("KM", value=100)
            if st.form_submit_button("Book via WhatsApp ✅"):
                msg = f"🚩 *BALAJI LOGISTICS*%0A📍 From: {s}%0A🏁 To: {e}%0A🚗 Car: {v}%0A💰 Fare: ₹{km*13}"
                st.markdown(f"### [✅ SEND NOW](https://wa.me/{WA_LINK_NO}?text={msg})")

    # ७. तुझा ४ x ३ ग्रिड मेनू (Bottom Navigation)
    st.write("<br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
    st.markdown('<div class="menu-container">', unsafe_allow_html=True)
    
    # पहिली ओळ (४ बटन्स)
    r1_c1, r1_c2, r1_c3, r1_c4 = st.columns(4)
    with r1_c1:
        if st.session_state.page == "Home": st.markdown('<div class="active-btn">', unsafe_allow_html=True)
        if st.button("🏠\nHome"): st.session_state.page = "Home"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with r1_c2:
        if st.session_state.page == "Booking": st.markdown('<div class="active-btn">', unsafe_allow_html=True)
        if st.button("📖\nBook"): st.session_state.page = "Booking"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with r1_c3:
        if st.button("🔐\nLogout"): st.session_state.logged_in = False; st.rerun()
    with r1_c4:
        if st.button("➕\nJoin"): st.info("Joined")

    # दुसरी ओळ (३ बटन्स)
    r2_c1, r2_c2, r2_c3 = st.columns(3)
    with r2_c1:
        if st.button("📊\nHistory"): st.info("Dashboard")
    with r2_c2:
        if st.button("🛡️\nAdmin"): st.warning("Locked")
    with r2_c3:
        if st.button("📞\nCall"): st.success(f"Call: {CONTACT_NO}")
    
    st.markdown('</div>', unsafe_allow_html=True)