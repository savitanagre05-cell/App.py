import streamlit as st
import time
import pandas as pd
import os
import hashlib
from datetime import datetime

# ==========================================
# 📝 CONFIGURATION (तुझी माहिती इथे आहे)
# ==========================================
WA_LINK_NO = "919767981986"   
CONTACT_NO = "9767981986"     
PAYMENT_NO = "9309146504"     
USER_DB = "users_data.csv"    
BOOKING_DB = "balaji_bookings.csv"

# गाड्यांचे अधिकृत दर
RATES = {"WagonR":11, "Swift Dzire":13, "Ertiga":18, "Innova":24, "Tempo Traveller":35}

st.set_page_config(page_title="Balaji Logistics", layout="wide", initial_sidebar_state="collapsed")

# --- Security Functions ---
def make_hashes(password): return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password, hashed_text): return make_hashes(password) == hashed_text

# डेटाबेस फाईल्स चेक करा
if not os.path.isfile(USER_DB): pd.DataFrame(columns=['username', 'password']).to_csv(USER_DB, index=False)
if not os.path.isfile(BOOKING_DB): pd.DataFrame(columns=['username', 'date', 'from_loc', 'to_loc', 'vehicle', 'fare', 'pay_mode']).to_csv(BOOKING_DB, index=False)

# Session States
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "Login"
if 'flash_done' not in st.session_state: st.session_state.flash_done = False

# ==========================================
# ⚡ FLASH SCREEN (ॲप उघडतानाची ॲनिमेशन)
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
    placeholder.empty()
    st.rerun()

# ==========================================
# 🎨 UI DESIGN (CSS FOR FIXED HORIZONTAL MENU)
# ==========================================
st.markdown("""
    <style>
    header, footer, #MainMenu {visibility: hidden;}
    /* मुख्य बॅकग्राउंड */
    .stApp {
        background: linear-gradient(135deg, #000 0%, #0a0a2e 100%);
        color: white;
        margin-bottom: 80px; /* खालच्या मेनूसाठी जागा */
    }
    
    /* कडक नेऑन कार्ड */
    .neon-card {
        background: rgba(255, 255, 255, 0.07);
        padding: 20px;
        border-radius: 20px;
        border: 2px solid #FFBB00;
        margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(255,187,0,0.2);
    }
    
    /* 📱 FIXED BOTTOM NAV BAR (No Scroll) */
    .fixed-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: rgba(10, 10, 10, 0.98);
        border-top: 1px solid #444;
        display: flex;
        justify-content: space-around;
        padding: 12px 0px;
        z-index: 9999;
    }
    
    /* बटन स्टाइल फिक्स (Emojji वर, नाव खाली) */
    div.stButton > button {
        background-color: transparent !important;
        border: none !important;
        color: #aaaaaa !important;
        font-size: 14px !important;
        width: 100% !important;
        padding: 0px !important;
        height: auto !important;
        display: flex;
        flex-direction: column;
        align-items: center;
        margin: 0 !important;
    }
    
    /* सिलेक्ट केलेल्या बटनचा रंग (Neon Blue) */
    .active-tab button {
        color: #00f2ff !important;
        font-weight: bold !important;
        text-shadow: 0 0 8px #00f2ff;
    }

    /* Next Button Style */
    .next-btn button {
        background: #FFBB00 !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        padding: 12px !important;
        margin-top: 20px !important;
        width: 100% !important;
    }

    /* मुख्य टायटल आणि टॅगलाईन */
    .main-title {
        color: #00f2ff;
        text-align: center;
        font-size: 26px;
        font-weight: bold;
        text-shadow: 0 0 10px #00f2ff;
        margin-top: 10px;
    }
    
    .sub-title {
        color: #FFBB00;
        text-align: center;
        font-size: 16px;
        font-weight: 500;
        margin-bottom: 20px;
    }

    /* पे-बॉक्स स्टाइल */
    .pay-box {
        background: #FFBB00;
        color: black;
        padding: 12px;
        border-radius: 12px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOGIN / REGISTER SYSTEM ---
if not st.session_state.logged_in:
    if st.session_state.page == "Login":
        st.markdown("<div class='neon-card' style='text-align:center;'><h2>🚖 BALAJI LOGIN</h2>", unsafe_allow_html=True)
        u = st.text_input("तुमचे नाव"); p = st.text_input("पासवर्ड", type='password')
        if st.button("LOGIN NOW", key="lgn"):
            users = pd.read_csv(USER_DB)
            if u in users['username'].values and check_hashes(p, users[users['username'] == u]['password'].values[0]):
                st.session_state.logged_in = True; st.session_state.user = u; st.session_state.page = "Home"; st.rerun()
        if st.button("नवीन ग्राहक? इथे क्लिक करा"): st.session_state.page = "Register"; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    elif st.session_state.page == "Register":
        st.markdown("<div class='neon-card'><h3>➕ Register</h3>", unsafe_allow_html=True)
        nu = st.text_input("Full Name"); np = st.text_input("Password", type='password')
        if st.button("CREATE ACCOUNT"):
            pd.DataFrame([[nu, make_hashes(np)]], columns=['username', 'password']).to_csv(USER_DB, mode='a', header=False, index=False)
            st.session_state.page = "Login"; st.rerun()

else:
    # --- HOME PAGE CONTENT (Aura Car + Tagline) ---
    if st.session_state.page == "Home":
        st.markdown("<div class='main-title'>🚩 BALAJI LOGISTICS</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-title'>Maharashtra and All India Service</div>", unsafe_allow_html=True)
        
        # 🚗 AURA IMAGE (तुझ्या गॅलरीमधून किंवा लिंकवरून)
        st.image("https://imgd.aeplcdn.com/1280x720/n/cw/ec/141125/aura-exterior-right-front-three-quarter.jpeg", caption="Travel with Comfort", use_container_width=True)
        
        st.markdown(f"<div class='neon-card' style='text-align:center;'><h4>स्वागत आहे, {st.session_state.user}! ✨</h4><p>स्वच्छ गाड्या आणि सुरक्षित प्रवास सेवा.</p></div>", unsafe_allow_html=True)
        
        # ➡️ NEXT PAGE BUTTON
        st.markdown('<div class="next-btn">', unsafe_allow_html=True)
        if st.button("NEXT: BOOK YOUR RIDE ➡️", key="next_h"):
            st.session_state.page = "Booking"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # --- BOOKING PAGE CONTENT (Payment Number Here) ---
    elif st.session_state.page == "Booking":
        st.markdown("<div class='main-title'>📅 BOOK NOW</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='pay-box'>💳 PhonePe/GPay: {PAYMENT_NO}</div>", unsafe_allow_html=True)
        st.markdown("<div class='neon-card'><h3>📝 प्रवासाची माहिती भरा</h3>", unsafe_allow_html=True)
        with st.form("book_form"):
            s = st.text_input("Pickup Point"); d = st.text_input("Drop Point")
            v = st.selectbox("गाडी निवडा", list(RATES.keys()))
            km = st.number_input("अंदाजे किमी", value=100)
            pay_m = st.radio("पेमेंट मोड", ["PhonePe", "Cash", "GPay"], horizontal=True)
            if st.form_submit_button("Confirm Booking ✅"):
                fare = km * RATES[v]
                pd.DataFrame([[st.session_state.user, datetime.now().strftime("%d-%m-%Y"), s, d, v, fare, pay_m]], 
                             columns=['username', 'date', 'from_loc', 'to_loc', 'vehicle', 'fare', 'pay_mode']).to_csv(BOOKING_DB, mode='a', header=False, index=False)
                # WHATSAPP MSG FOR PREMIUM LOGS
                msg = (f"🚀 *NEW BOOKING*%0A🚩 *BALAJI TOUR'S*%0A👤 Cust: {st.session_state.user}%0A📍 From: {s}%0A🏁 To: {d}%0A🚗 Car: {v}%0A💰 Fare: ₹{fare}%0A💳 Pay: {pay_m}%0A---%0A✅ टोल, पार्किंग वेगळा.")
                st.markdown(f"### [🚀 व्हॉट्सॲपवर पाठवा](https://wa.me/{WA_LINK_NO}?text={msg})")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- HISTORY PAGE ---
    elif st.session_state.page == "History":
        st.markdown("<h3 style='color:#FFBB00;'>📊 तुमची हिस्ट्री</h3>", unsafe_allow_html=True)
        h = pd.read_csv(BOOKING_DB)
        u_h = h[h['username'] == st.session_state.user]
        st.dataframe(u_h[['date', 'from_loc', 'to_loc', 'vehicle', 'fare', 'pay_mode']], use_container_width=True)

    # ==========================================
    # 📱 THE FINAL HORIZONTAL BOTTOM MENU
    # ==========================================
    # ५ कोलम वापरून आडवा मेनू (Watsapp लुक)
    st.markdown('<div class="fixed-nav">', unsafe_allow_html=True)
    m1, m2, m3, m4, m5 = st.columns(5)
    
    with m1:
        if st.session_state.page == "Home": st.markdown('<div class="active-tab">', unsafe_allow_html=True)
        if st.button("🏠\nHome"): st.session_state.page = "Home"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with m2:
        if st.session_state.page == "Booking": st.markdown('<div class="active-tab">', unsafe_allow_html=True)
        if st.button("📅\nBook"): st.session_state.page = "Booking"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with m3:
        if st.session_state.page == "History": st.markdown('<div class="active-tab">', unsafe_allow_html=True)
        if st.button("📜\nHist"): st.session_state.page = "History"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with m4:
        if st.button("📞\nCall"): st.success(f"Dial: {CONTACT_NO}")
    with m5:
        if st.button("🚪\nExit"): st.session_state.logged_in = False; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)