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
PHONEPE_NO = "9309146504"  
USER_DB = "users_data.csv"    
BOOKING_DB = "balaji_bookings.csv"
RATES = {"WagonR":11, "Swift Dzire":13, "Ertiga":18, "Innova":24, "Tempo Traveller":35}

st.set_page_config(page_title="Balaji Logistics", layout="wide")

# --- Security Functions ---
def make_hashes(password): return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password, hashed_text): return make_hashes(password) == hashed_text

if not os.path.isfile(USER_DB): pd.DataFrame(columns=['username', 'password', 'mobile']).to_csv(USER_DB, index=False)
if not os.path.isfile(BOOKING_DB): pd.DataFrame(columns=['username', 'date', 'from_loc', 'to_loc', 'vehicle', 'fare', 'pay_mode']).to_csv(BOOKING_DB, index=False)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user' not in st.session_state: st.session_state.user = ""
if 'flash_done' not in st.session_state: st.session_state.flash_done = False
if 'page' not in st.session_state: st.session_state.page = "Home"

# ==========================================
# ⚡ FLASH SCREEN
# ==========================================
if not st.session_state.flash_done:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown(f"""
            <style>
            .flash-bg {{ position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: black; z-index: 9999; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
            .flash-logo {{ font-size: 45px; color: #FFBB00; font-weight: bold; text-align: center; }}
            </style>
            <div class='flash-bg'><div class='flash-logo'>🚩 BALAJI<br><span style='font-size:20px; color:white;'>TOUR'S AND TRAVELS</span></div></div>
        """, unsafe_allow_html=True)
        time.sleep(2.5)
    st.session_state.flash_done = True
    placeholder.empty()
    st.rerun()

# ==========================================
# 🎨 UI STYLES (NO SIDEBAR)
# ==========================================
st.markdown(f"""
    <style>
    header, footer, #MainMenu {{visibility: hidden;}}
    .stApp {{ background: linear-gradient(135deg, #000 0%, #0a0a2e 100%); color: white; }}
    .neon-card {{ background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 15px; border: 1px solid #FFBB00; margin-bottom: 20px; }}
    
    /* Horizontal Menu Buttons */
    .stButton>button {{
        width: 100%; border-radius: 10px; border: 1px solid #FFBB00; background: black; color: white; font-weight: bold;
    }}
    .stButton>button:hover {{ background: #FFBB00; color: black; }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🔐 AUTH
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center; color:#FFBB00;'>🚩 BALAJI LOGISTICS</h2>", unsafe_allow_html=True)
    auth = st.radio("निवडा", ["Login", "Register"], horizontal=True)
    
    if auth == "Login":
        u = st.text_input("नाव")
        p = st.text_input("पासवर्ड", type='password')
        if st.button("LOGIN NOW"):
            users = pd.read_csv(USER_DB)
            if u in users['username'].values:
                if check_hashes(p, users[users['username'] == u]['password'].values[0]):
                    st.session_state.logged_in = True; st.session_state.user = u; st.rerun()
            st.error("माहिती चुकीची आहे!")
    else:
        nu = st.text_input("नाव"); nm = st.text_input("मोबाईल"); np = st.text_input("पासवर्ड", type='password')
        if st.button("CREATE"):
            if nu and nm and np:
                pd.DataFrame([[nu, make_hashes(np), nm]], columns=['username', 'password', 'mobile']).to_csv(USER_DB, mode='a', header=False, index=False)
                st.success("रजिस्ट्रेशन झाले!")

# ==========================================
# 🏠 MAIN CONTENT (HORIZONTAL MENU)
# ==========================================
else:
    # --- TOP MENU TABS ---
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        if st.button("🏠 Home"): st.session_state.page = "Home"
    with m_col2:
        if st.button("📅 Book"): st.session_state.page = "Booking"
    with m_col3:
        if st.button("📜 History"): st.session_state.page = "History"
    with m_col4:
        if st.button("🚪 Out"): st.session_state.logged_in = False; st.rerun()

    st.markdown("---")

    # --- Home ---
    if st.session_state.page == "Home":
        st.markdown("<h2 style='text-align:center;'>🚩 BALAJI LOGISTICS</h2>", unsafe_allow_html=True)
        st.image("https://imgd.aeplcdn.com/1280x720/n/cw/ec/141125/aura-exterior-right-front-three-quarter.jpeg")
        st.markdown(f"""
            <div class='neon-card'>
                <h4>स्वागत आहे, {st.session_state.user}!</h4>
                <p style='color:#FFBB00; font-weight:bold;'>MAHARASHTRA AND ALL INDIA SERVICE.</p>
                <p>Call for Support: {CONTACT_NO}</p>
            </div>
        """, unsafe_allow_html=True)

    # --- Booking ---
    elif st.session_state.page == "Booking":
        st.markdown("<h3 style='text-align:center;'>📅 नवीन बुकिंग</h3>", unsafe_allow_html=True)
        with st.form("b_form"):
            s = st.text_input("Pickup Point")
            d = st.text_input("Drop Point")
            v = st.selectbox("Vehicle", list(RATES.keys()))
            km = st.number_input("Estimated KM", value=50)
            pay = st.radio("Payment", ["Cash", "Online"], horizontal=True)
            if st.form_submit_button("Confirm ✅"):
                fare = km * RATES[v]; bid = f"BT{datetime.now().strftime('%d%H%M')}"
                pd.DataFrame([[st.session_state.user, datetime.now().strftime("%d-%m-%Y"), s, d, v, fare, pay]], columns=['username', 'date', 'from_loc', 'to_loc', 'vehicle', 'fare', 'pay_mode']).to_csv(BOOKING_DB, mode='a', header=False, index=False)
                
                p_note = f"%0A💳 *Payment:* Online (PhonePe: {PHONEPE_NO})" if pay == "Online" else "%0A💳 *Payment:* Cash"
                msg = (f"🚩 *BALAJI TOURS* 🚩%0A━━━━━━━━━━━━%0A🆔 *ID:* #{bid}%0A👤 *Cust:* {st.session_state.user}%0A📍 *Pick:* {s}%0A🏁 *Drop:* {d}%0A🚗 *Veh:* {v}%0A💰 *Fare:* ₹{fare}/-{p_note}%0A━━━━━━━━━━━━%0A⚠️ *Note: Toll & Parking charges extra.*%0A━━━━━━━━━━━━")
                st.success(f"Booking Done! Fare: ₹{fare}")
                st.markdown(f"### [🚀 व्हॉट्सॲपवर पाठवा](https://wa.me/{WA_LINK_NO}?text={msg})")

    # --- History ---
    elif st.session_state.page == "History":
        st.markdown("<h3 style='text-align:center;'>📜 तुमची हिस्ट्री</h3>", unsafe_allow_html=True)
        h = pd.read_csv(BOOKING_DB)
        st.dataframe(h[h['username'] == st.session_state.user][['date', 'from_loc', 'to_loc', 'fare', 'pay_mode']], use_container_width=True)