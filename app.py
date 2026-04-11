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

# --- Security Functions ---
def make_hashes(password): return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password, hashed_text): return make_hashes(password) == hashed_text

if not os.path.isfile(USER_DB): pd.DataFrame(columns=['username', 'password']).to_csv(USER_DB, index=False)
if not os.path.isfile(BOOKING_DB): pd.DataFrame(columns=['username', 'date', 'from_loc', 'to_loc', 'vehicle', 'fare', 'pay_mode']).to_csv(BOOKING_DB, index=False)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "Login"
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
            @keyframes pulse { 0% { transform: scale(1); opacity: 0.8; } 50% { transform: scale(1.1); opacity: 1; } 100% { transform: scale(1); opacity: 0.8; } }
            </style>
            <div class="flash-bg">
                <div class="flash-logo">🚩 BALAJI<br><span style='font-size:20px; color:white;'>TOUR'S AND TRAVELS</span></div>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(2.5)
    st.session_state.flash_done = True
    placeholder.empty()
    st.rerun()

# ==========================================
# 🎨 UI DESIGN
# ==========================================
st.markdown("""
    <style>
    header, footer, #MainMenu {visibility: hidden;}
    .stApp { background: linear-gradient(135deg, #000 0%, #0a0a2e 100%); color: white; }
    .neon-card { background: rgba(255, 255, 255, 0.07); padding: 20px; border-radius: 20px; border: 2px solid #FFBB00; margin-bottom: 20px; box-shadow: 0 0 15px rgba(255,187,0,0.2); }
    
    /* 📱 HORIZONTAL NAV BAR */
    .nav-container { position: fixed; bottom: 0; left: 0; right: 0; background: rgba(10, 10, 10, 0.98); border-top: 1px solid #333; padding: 10px 0; z-index: 1000; }
    [data-testid="column"] { display: flex; justify-content: center; align-items: center; }
    
    div.stButton > button { background: transparent !important; color: #888 !important; border: none !important; font-size: 13px !important; width: 100% !important; padding: 0 !important; }
    .active-tab button { color: #00f2ff !important; font-weight: bold !important; text-shadow: 0 0 10px #00f2ff; }
    
    .main-title { color: #00f2ff; text-align: center; font-size: 26px; font-weight: bold; text-shadow: 0 0 10px #00f2ff; }
    .sub-title { color: #FFBB00; text-align: center; font-size: 16px; font-weight: 500; margin-bottom: 20px; }
    .pay-box { background: #FFBB00; color: black; padding: 12px; border-radius: 12px; font-weight: bold; text-align: center; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- LOGIN / REGISTER ---
if not st.session_state.logged_in:
    if st.session_state.page == "Login":
        st.markdown("<div class='neon-card' style='text-align:center;'><h2>🚖 BALAJI LOGIN</h2>", unsafe_allow_html=True)
        u = st.text_input("नाव"); p = st.text_input("पासवर्ड", type='password')
        if st.button("LOGIN NOW", use_container_width=True):
            users = pd.read_csv(USER_DB)
            if u in users['username'].values and check_hashes(p, users[users['username'] == u]['password'].values[0]):
                st.session_state.logged_in = True; st.session_state.user = u; st.session_state.page = "Home"; st.rerun()
        if st.button("नवीन अकाउंट बनवा"): st.session_state.page = "Register"; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    elif st.session_state.page == "Register":
        st.markdown("<div class='neon-card'><h3>➕ Register</h3>", unsafe_allow_html=True)
        nu = st.text_input("Full Name"); np = st.text_input("Password", type='password')
        if st.button("CREATE ACCOUNT"):
            pd.DataFrame([[nu, make_hashes(np)]], columns=['username', 'password']).to_csv(USER_DB, mode='a', header=False, index=False)
            st.session_state.page = "Login"; st.rerun()

else:
    # --- HOME PAGE ---
    if st.session_state.page == "Home":
        st.markdown("<div class='main-title'>🚩 BALAJI LOGISTICS TOUR'S AND TRAVELS</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-title'>Maharashtra and All India Service</div>", unsafe_allow_html=True)
        st.image("https://imgd.aeplcdn.com/664x374/n/cw/ec/141125/aura-exterior-right-front-three-quarter.jpeg?isig=0&q=80", use_container_width=True)
        st.markdown(f"<div class='neon-card' style='text-align:center;'><h4>स्वागत आहे, {st.session_state.user}! ✨</h4><p>स्वच्छ गाड्या आणि सुरक्षित प्रवास सेवा.</p></div>", unsafe_allow_html=True)

    # --- BOOKING PAGE ---
    elif st.session_state.page == "Booking":
        st.markdown(f"<div class='pay-box'>💳 PhonePe/GPay: {PAYMENT_NO}</div>", unsafe_allow_html=True)
        st.markdown("<div class='neon-card'><h3>📝 बुकिंग फॉर्म</h3>", unsafe_allow_html=True)
        with st.form("book"):
            s = st.text_input("Pickup"); d = st.text_input("Drop")
            v = st.selectbox("गाडी", list(RATES.keys()))
            km = st.number_input("अंदाजे किमी", value=100)
            pay_m = st.radio("पेमेंट", ["PhonePe", "Cash", "GPay"], horizontal=True)
            if st.form_submit_button("Confirm Booking ✅"):
                fare = km * RATES[v]
                pd.DataFrame([[st.session_state.user, datetime.now().strftime("%d-%m-%Y"), s, d, v, fare, pay_m]], 
                             columns=['username', 'date', 'from_loc', 'to_loc', 'vehicle', 'fare', 'pay_mode']).to_csv(BOOKING_DB, mode='a', header=False, index=False)
                msg = (f"🚀 *NEW BOOKING CONFIRMED* 🚀%0A━━━━━━━━━━━━━━━━━━%0A🚩 *BALAJI TOUR'S AND TRAVELS*%0A👤 *Cust:* {st.session_state.user}%0A📍 *From:* {s}%0A🏁 *To:* {d}%0A🚗 *Car:* {v}%0A💰 *Fare:* ₹{fare}%0A💳 *Pay:* {pay_m}%0A━━━━━━━━━━━━━━━━━━%0A📌 *Notes:*%0A✅ टोल, पार्किंग वेगळी असेल.%0A✅ बॉर्डर टॅक्स कस्टमरचा.%0A✅ जादा किमीचे पैसे लागतील.%0A🙏 *Safe Journey!*")
                st.markdown(f"### [🚀 व्हॉट्सॲप मेसेज पाठवा](https://wa.me/{WA_LINK_NO}?text={msg})")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- HISTORY PAGE ---
    elif st.session_state.page == "History":
        st.markdown("<h3 style='color:#FFBB00;'>📊 तुमची हिस्ट्री</h3>", unsafe_allow_html=True)
        h = pd.read_csv(BOOKING_DB)
        u_h = h[h['username'] == st.session_state.user]
        st.dataframe(u_h[['date', 'from_loc', 'to_loc', 'vehicle', 'fare', 'pay_mode']], use_container_width=True)

    # ==========================================
    # 📱 HORIZONTAL BOTTOM MENU
    # ==========================================
    st.write("<br><br><br><br><br>", unsafe_allow_html=True)
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    cols = st.columns(5)
    with cols[0]:
        if st.session_state.page == "Home": st.markdown('<div class="active-tab">', unsafe_allow_html=True)
        if st.button("🏠\nHome"): st.session_state.page = "Home"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with cols[1]:
        if st.session_state.page == "Booking": st.markdown('<div class="active-tab">', unsafe_allow_html=True)
        if st.button("📅\nBook"): st.session_state.page = "Booking"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with cols[2]:
        if st.session_state.page == "History": st.markdown('<div class="active-tab">', unsafe_allow_html=True)
        if st.button("📜\nHistory"): st.session_state.page = "History"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with cols[3]:
        if st.button("📞\nCall"): st.success(f"Dial: {CONTACT_NO}")
    with cols[4]:
        if st.button("🚪\nExit"): st.session_state.logged_in = False; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)