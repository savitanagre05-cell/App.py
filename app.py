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
USER_DB = "users_data.csv"    
BOOKING_DB = "balaji_bookings.csv"
RATES = {"WagonR":11, "Swift Dzire":13, "Ertiga":18, "Innova":24, "Tempo Traveller":35}

st.set_page_config(page_title="Balaji Logistics", layout="wide", initial_sidebar_state="expanded")

# --- Security Functions ---
def make_hashes(password): return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password, hashed_text): return make_hashes(password) == hashed_text

if not os.path.isfile(USER_DB): pd.DataFrame(columns=['username', 'password', 'mobile']).to_csv(USER_DB, index=False)
if not os.path.isfile(BOOKING_DB): pd.DataFrame(columns=['username', 'date', 'from_loc', 'to_loc', 'vehicle', 'fare', 'pay_mode']).to_csv(BOOKING_DB, index=False)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "Home"
if 'user' not in st.session_state: st.session_state.user = ""
if 'flash_done' not in st.session_state: st.session_state.flash_done = False

# ==========================================
# ⚡ FLASH SCREEN (FIXED)
# ==========================================
if not st.session_state.flash_done:
    flash_holder = st.empty()
    flash_holder.markdown("""
        <style>
        .flash-bg { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: black; z-index: 9999; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        .flash-logo { font-size: 40px; color: #FFBB00; font-weight: bold; text-align: center; font-family: sans-serif; }
        </style>
        <div class='flash-bg'><div class='flash-logo'>🚩 BALAJI<br><span style='font-size:18px; color:white;'>TOUR'S AND TRAVELS</span></div></div>
    """, unsafe_allow_html=True)
    time.sleep(2)
    st.session_state.flash_done = True
    flash_holder.empty()
    st.rerun()

# ==========================================
# 🎨 UI STYLES
# ==========================================
st.markdown(f"""
    <style>
    header, footer, #MainMenu {{visibility: hidden;}}
    .stApp {{ background: linear-gradient(135deg, #000 0%, #0a0a2e 100%); color: white; }}
    .neon-card {{ background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 15px; border: 1px solid #FFBB00; margin-bottom: 20px; }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🔐 AUTH & CONTENT
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<div class='neon-card'><h2>🚖 BALAJI LOGISTICS</h2></div>", unsafe_allow_html=True)
    auth_choice = st.radio("निवडा", ["Login", "Register"], horizontal=True)
    
    if auth_choice == "Login":
        u = st.text_input("नाव")
        p = st.text_input("पासवर्ड", type='password')
        if st.button("LOGIN NOW"):
            users = pd.read_csv(USER_DB)
            if u in users['username'].values:
                db_pass = users[users['username'] == u]['password'].values[0]
                if check_hashes(p, db_pass):
                    st.session_state.logged_in = True; st.session_state.user = u; st.rerun()
            st.error("चुकीची माहिती!")
    else:
        nu = st.text_input("पूर्ण नाव")
        nm = st.text_input("मोबाईल")
        np = st.text_input("पासवर्ड", type='password')
        if st.button("CREATE ACCOUNT"):
            if nu and nm and np:
                pd.DataFrame([[nu, make_hashes(np), nm]], columns=['username', 'password', 'mobile']).to_csv(USER_DB, mode='a', header=False, index=False)
                st.success("रजिस्ट्रेशन झाले! आता लॉगिन करा.")

else:
    # --- Sidebar ---
    with st.sidebar:
        st.markdown("<h2 style='color:#FFBB00;'>🚩 Balaji Menu</h2>", unsafe_allow_html=True)
        choice = st.radio("Navigation", ["Home", "Booking", "History"])
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    # --- Home ---
    if choice == "Home":
        st.markdown("<h2 style='text-align:center;'>🚩 BALAJI LOGISTICS</h2>", unsafe_allow_html=True)
        st.image("https://imgd.aeplcdn.com/1280x720/n/cw/ec/141125/aura-exterior-right-front-three-quarter.jpeg")
        st.markdown(f"<div class='neon-card'><h4>स्वागत आहे, {st.session_state.user}!</h4><p>MAHARASHTRA AND ALL INDIA SERVICE.</p></div>", unsafe_allow_html=True)

    # --- Booking ---
    elif choice == "Booking":
        st.markdown("<h2 style='text-align:center;'>📅 BOOK NOW</h2>", unsafe_allow_html=True)
        with st.form("b_form"):
            s = st.text_input("Pickup Point")
            d = st.text_input("Drop Point")
            v = st.selectbox("गाडी", list(RATES.keys()))
            km = st.number_input("किमी", value=50)
            if st.form_submit_button("Confirm ✅"):
                u_df = pd.read_csv(USER_DB); mob = u_df[u_df['username'] == st.session_state.user]['mobile'].values[0]
                fare = km * RATES[v]; bid = f"BT{datetime.now().strftime('%d%H%M')}"
                pd.DataFrame([[st.session_state.user, datetime.now().strftime("%d-%m-%Y"), s, d, v, fare, "Cash"]], columns=['username', 'date', 'from_loc', 'to_loc', 'vehicle', 'fare', 'pay_mode']).to_csv(BOOKING_DB, mode='a', header=False, index=False)
                
                msg = (f"🚩 *BALAJI TOURS* 🚩%0A━━━━━━━━━━━━%0A🆔 *ID:* #{bid}%0A👤 *Cust:* {st.session_state.user}%0A📍 *Pick:* {s}%0A🏁 *Drop:* {d}%0A🚗 *Veh:* {v}%0A💰 *Fare:* ₹{fare}/-%0A━━━━━━━━━━━━%0A⚠️ *Note: Toll & Parking extra.*%0A━━━━━━━━━━━━")
                st.success("Booking Done!")
                st.markdown(f"### [🚀 व्हॉट्सॲपवर पाठवा](https://wa.me/{WA_LINK_NO}?text={msg})")

    # --- History ---
    elif choice == "History":
        st.markdown("<h2 style='text-align:center;'>📜 HISTORY</h2>", unsafe_allow_html=True)
        h = pd.read_csv(BOOKING_DB)
        st.dataframe(h[h['username'] == st.session_state.user][['date', 'from_loc', 'to_loc', 'fare']], use_container_width=True)