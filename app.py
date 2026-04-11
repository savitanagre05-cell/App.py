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

if not os.path.isfile(USER_DB): pd.DataFrame(columns=['username', 'password', 'mobile']).to_csv(USER_DB, index=False)
if not os.path.isfile(BOOKING_DB): pd.DataFrame(columns=['username', 'date', 'from_loc', 'to_loc', 'vehicle', 'fare', 'pay_mode']).to_csv(BOOKING_DB, index=False)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "Home"
if 'flash_done' not in st.session_state: st.session_state.flash_done = False

# ==========================================
# ⚡ FLASH SCREEN
# ==========================================
if not st.session_state.flash_done:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("""
            <style>
            .flash-bg { background: black; height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; }
            .flash-logo { font-size: 50px; color: #FFBB00; font-weight: bold; animation: pulse 2s infinite; }
            </style>
            <div class='flash-bg'><div class='flash-logo'>🚩 BALAJI<br><span style='font-size:20px; color:white;'>TOUR'S AND TRAVELS</span></div></div>
        """, unsafe_allow_html=True)
        time.sleep(2.0)
    st.session_state.flash_done = True
    placeholder.empty()
    st.rerun()

# ==========================================
# 🎨 UI & HORIZONTAL MENU CSS (STRICT FIX)
# ==========================================
st.markdown(f"""
    <style>
    header, footer, #MainMenu {{visibility: hidden;}}
    .stApp {{ background: linear-gradient(135deg, #000 0%, #0a0a2e 100%); color: white; }}
    
    /* 📱 मोबाईलवर कॉलम्सना एकाच ओळीत ठेवण्यासाठी (Horizontal Fix) */
    div[data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        justify-content: space-around !important;
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        width: 100% !important;
        background: #0a0a0a !important;
        padding: 12px 0px !important;
        z-index: 999999 !important;
        border-top: 2px solid #FFBB00 !important;
    }}

    /* प्रत्येक कॉलमची रुंदी समान ठेवणे */
    div[data-testid="column"] {{
        flex: 1 1 0% !important;
        min-width: 0px !important;
        text-align: center !important;
    }}

    /* बटण डिझाइन */
    div.stButton > button {{
        background-color: transparent !important; border: none !important;
        color: #aaaaaa !important; font-size: 11px !important;
        display: flex !important; flex-direction: column !important;
        align-items: center !important; width: 100% !important;
        padding: 0px !important; gap: 2px;
    }}
    
    .main-title {{ color: #00f2ff; text-align: center; font-size: 24px; font-weight: bold; margin-bottom: 5px; }}
    .neon-card {{ background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 15px; border: 1px solid #FFBB00; text-align: center; margin-bottom: 20px; }}
    
    /* Active टॅबसाठी पिवळा रंग */
    .active-tab button {{ color: #FFBB00 !important; font-weight: bold !important; }}
    </style>
""", unsafe_allow_html=True)

# --- LOGIN / REGISTER ---
if not st.session_state.logged_in:
    if st.session_state.page == "Login":
        st.markdown("<div class='neon-card'><h2>🚖 LOGIN</h2>", unsafe_allow_html=True)
        u = st.text_input("नाव")
        p = st.text_input("पासवर्ड", type='password')
        if st.button("LOGIN NOW"):
            users = pd.read_csv(USER_DB)
            if u in users['username'].values and check_hashes(p, users[users['username'] == u]['password'].values[0]):
                st.session_state.logged_in = True; st.session_state.user = u; st.session_state.page = "Home"; st.rerun()
        if st.button("Register New"): st.session_state.page = "Register"; st.rerun()
    elif st.session_state.page == "Register":
        st.markdown("<div class='neon-card'><h3>➕ REGISTER</h3>", unsafe_allow_html=True)
        nu = st.text_input("नाव"); nm = st.text_input("मोबाईल"); np = st.text_input("पासवर्ड", type='password')
        if st.button("CREATE"):
            pd.DataFrame([[nu, make_hashes(np), nm]], columns=['username', 'password', 'mobile']).to_csv(USER_DB, mode='a', header=False, index=False)
            st.session_state.page = "Login"; st.rerun()

else:
    # --- PAGES ---
    if st.session_state.page == "Home":
        st.markdown("<div class='main-title'>🚩 BALAJI LOGISTICS</div>", unsafe_allow_html=True)
        # Hyundai Aura Image Fix
        st.image("https://imgd.aeplcdn.com/1280x720/n/cw/ec/141125/aura-exterior-right-front-three-quarter.jpeg", use_container_width=True)
        st.markdown(f"<div class='neon-card'><h4>स्वागत आहे, {st.session_state.user}! ✨</h4><p>अंबड आणि पाथर्डी फाटा परिसरात २४ तास सेवा.</p></div>", unsafe_allow_html=True)

    elif st.session_state.page == "Booking":
        st.markdown("<div class='main-title'>📅 BOOK NOW</div>", unsafe_allow_html=True)
        with st.form("b_form"):
            s = st.text_input("Pickup Point")
            d = st.text_input("Drop Point")
            v = st.selectbox("गाडी", list(RATES.keys()))
            km = st.number_input("किमी", value=100)
            pm = st.radio("पेमेंट", ["Cash", "Online"], horizontal=True)
            if st.form_submit_button("Confirm ✅"):
                u_df = pd.read_csv(USER_DB); mob = u_df[u_df['username'] == st.session_state.user]['mobile'].values[0]
                fare = km * RATES[v]
                pd.DataFrame([[st.session_state.user, datetime.now().strftime("%d-%m-%Y"), s, d, v, fare, pm]], columns=['username', 'date', 'from_loc', 'to_loc', 'vehicle', 'fare', 'pay_mode']).to_csv(BOOKING_DB, mode='a', header=False, index=False)
                
                # Professional Message
                msg = (f"🚩 *BALAJI TOURS & TRAVELS* 🚩%0A━━━━━━━━━━━━━━━━━━━━%0A"
                       f"👤 *ग्राहक:* {st.session_state.user}%0A📞 *संपर्क:* {mob}%0A📍 *पिकअप:* {s}%0A🏁 *ड्रॉप:* {d}%0A"
                       f"🚗 *गाडी:* {v}%0A💰 *भाडे:* ₹{fare}/-%0A━━━━━━━━━━━━━━━━━━━━")
                st.markdown(f"### [🚀 व्हॉट्सॲपवर पाठवा](https://wa.me/{WA_LINK_NO}?text={msg})")
                st.balloons()

    elif st.session_state.page == "History":
        st.markdown("<div class='main-title'>📜 HISTORY</div>", unsafe_allow_html=True)
        h = pd.read_csv(BOOKING_DB)
        st.dataframe(h[h['username'] == st.session_state.user][['date', 'from_loc', 'to_loc', 'vehicle', 'fare']], use_container_width=True)

    # --- 📱 FIXED HORIZONTAL BOTTOM MENU ---
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
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
        if st.button("📜\nHist"): st.session_state.page = "History"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    with cols[3]:
        st.markdown(f'<a href="tel:{CONTACT_NO}" style="text-decoration:none;"><div style="text-align:center; color:#aaaaaa; font-size:11px;">📞<br>Call</div></a>', unsafe_allow_html=True)
        
    with cols[4]:
        if st.button("🚪\nExit"): st.session_state.logged_in = False; st.rerun()