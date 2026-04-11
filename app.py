import streamlit as st
import time
import pandas as pd
import os
import hashlib
from datetime import datetime

# ==========================================
# 📝 CONFIGURATION
# ==========================================
WA_LINK_NO = "919767981986"   
CONTACT_NO = "9767981986"     
PAYMENT_NO = "9309146504"     
USER_DB = "users_data.csv"    
BOOKING_DB = "balaji_bookings.csv"

RATES = {"WagonR":11, "Swift Dzire":13, "Ertiga":18, "Innova":24, "Tempo Traveller":35}

st.set_page_config(page_title="Balaji Logistics", layout="wide", initial_sidebar_state="collapsed")

# --- Security ---
def make_hashes(password): return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password, hashed_text): return make_hashes(password) == hashed_text

if not os.path.isfile(USER_DB): pd.DataFrame(columns=['username', 'password']).to_csv(USER_DB, index=False)
if not os.path.isfile(BOOKING_DB): pd.DataFrame(columns=['username', 'date', 'from_loc', 'to_loc', 'vehicle', 'fare', 'pay_mode']).to_csv(BOOKING_DB, index=False)

# --- Session State Fix ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "Home" # Default page
if 'flash_done' not in st.session_state: st.session_state.flash_done = False

# ==========================================
# ⚡ FLASH SCREEN
# ==========================================
if not st.session_state.flash_done:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("""
            <style>
            .flash-bg { background: black; height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }
            .flash-logo { font-size: 50px; color: #FFBB00; font-weight: bold; animation: pulse 2s infinite; }
            </style>
            <div class="flash-bg"><div class="flash-logo">🚩 BALAJI<br><span style='font-size:20px; color:white;'>TOUR'S AND TRAVELS</span></div></div>
        """, unsafe_allow_html=True)
        time.sleep(2.0)
    st.session_state.flash_done = True
    st.session_state.page = "Home" # फ्लॅश नंतर होम पेजच उघडेल
    placeholder.empty()
    st.rerun()

# ==========================================
# 🎨 UI DESIGN (FIXED CSS)
# ==========================================
st.markdown("""
    <style>
    header, footer, #MainMenu {visibility: hidden;}
    .stApp { background: linear-gradient(135deg, #000 0%, #0a0a2e 100%); color: white; margin-bottom: 100px; }
    .neon-card { background: rgba(255, 255, 255, 0.07); padding: 15px; border-radius: 20px; border: 2px solid #FFBB00; margin-bottom: 15px; }
    
    .fixed-nav {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background: #080808; border-top: 1px solid #444;
        padding: 10px 0px; z-index: 9999;
        display: flex; justify-content: space-around;
    }
    
    div.stButton > button {
        background-color: transparent !important; border: none !important;
        color: #999 !important; font-size: 14px !important; width: 100% !important;
        display: flex; flex-direction: column; align-items: center;
    }
    .active-tab button { color: #00f2ff !important; font-weight: bold !important; }
    .next-btn button { background: #FFBB00 !important; color: black !important; font-weight: bold !important; border-radius: 12px !important; }
    </style>
""", unsafe_allow_html=True)

# --- MAIN APP LOGIC ---
if not st.session_state.logged_in:
    # जर लॉगिन नसेल तर लॉगिन पेज दाखवा
    st.markdown("<div class='neon-card' style='text-align:center;'><h2>🚖 BALAJI LOGIN</h2>", unsafe_allow_html=True)
    u = st.text_input("नाव"); p = st.text_input("पासवर्ड", type='password')
    if st.button("LOGIN NOW"):
        users = pd.read_csv(USER_DB)
        if u in users['username'].values:
            st.session_state.logged_in = True; st.session_state.user = u; st.session_state.page = "Home"; st.rerun()
    if st.button("नवीन ग्राहक?"): st.session_state.page = "Register"; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- PAGES ---
    if st.session_state.page == "Home":
        st.markdown("<h2 style='text-align:center; color:#00f2ff;'>🚩 BALAJI LOGISTICS</h2>", unsafe_allow_html=True)
        st.image("https://imgd.aeplcdn.com/1280x720/n/cw/ec/141125/aura-exterior-right-front-three-quarter.jpeg", use_container_width=True)
        st.markdown(f"<div class='neon-card' style='text-align:center;'><h4>स्वागत आहे, {st.session_state.user}!</h4></div>", unsafe_allow_html=True)
        if st.button("NEXT: BOOK YOUR RIDE ➡️", key="next_home_btn"):
            st.session_state.page = "Booking"; st.rerun()

    elif st.session_state.page == "Booking":
        st.markdown("<h2 style='text-align:center;'>📅 BOOK NOW</h2>", unsafe_allow_html=True)
        with st.form("my_form"):
            s = st.text_input("Pickup"); d = st.text_input("Drop")
            v = st.selectbox("Car", list(RATES.keys()))
            if st.form_submit_button("Confirm ✅"):
                st.success("Booking Done! व्हॉट्सॲपवर मेसेज पाठवा.")

    # --- HORIZONTAL MENU BAR ---
    st.markdown('<div class="fixed-nav">', unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        if st.session_state.page == "Home": st.markdown('<div class="active-tab">', unsafe_allow_html=True)
        if st.button("🏠\nHome"): st.session_state.page = "Home"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        if st.session_state.page == "Booking": st.markdown('<div class="active-tab">', unsafe_allow_html=True)
        if st.button("📅\nBook"): st.session_state.page = "Booking"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        if st.button("📜\nHist"): st.session_state.page = "History"; st.rerun()
    with c4:
        if st.button("📞\nCall"): st.info(f"Dial: {CONTACT_NO}")
    with c5:
        if st.button("🚪\nExit"): st.session_state.logged_in = False; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)