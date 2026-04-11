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

st.set_page_config(page_title="Balaji Logistics", layout="wide", initial_sidebar_state="collapsed")

# --- Security Functions ---
def make_hashes(password): return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password, hashed_text): return make_hashes(password) == hashed_text

if not os.path.isfile(USER_DB): pd.DataFrame(columns=['username', 'password', 'mobile']).to_csv(USER_DB, index=False)
if not os.path.isfile(BOOKING_DB): pd.DataFrame(columns=['username', 'date', 'from_loc', 'to_loc', 'vehicle', 'fare', 'pay_mode']).to_csv(BOOKING_DB, index=False)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "Login"
if 'user' not in st.session_state: st.session_state.user = ""
if 'flash_done' not in st.session_state: st.session_state.flash_done = False

# ==========================================
# ⚡ FLASH SCREEN
# ==========================================
if not st.session_state.flash_done:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("""
            <style>
            .flash-bg { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: black; z-index: 999999; display: flex; flex-direction: column; align-items: center; justify-content: center; }
            .flash-logo { font-size: 50px; color: #FFBB00; font-weight: bold; text-align: center; }
            </style>
            <div class='flash-bg'><div class='flash-logo'>🚩 BALAJI<br><span style='font-size:20px; color:white;'>TOUR'S AND TRAVELS</span></div></div>
        """, unsafe_allow_html=True)
        time.sleep(2.5)
    st.session_state.flash_done = True
    placeholder.empty()
    st.rerun()

# ==========================================
# 🎨 UI & HORIZONTAL MENU (STRICT CSS)
# ==========================================
st.markdown(f"""
    <style>
    header, footer, #MainMenu {{visibility: hidden;}}
    .stApp {{ background: linear-gradient(135deg, #000 0%, #0a0a2e 100%); color: white; }}
    
    /* 📱 मोबाईलवर आडव्या ओळीत (Horizontal) ठेवण्यासाठी */
    div[data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important; /* हेच कॉलम्सना आडवं ठेवतं */
        justify-content: space-between !important;
        position: fixed !important;
        bottom: 0 !important; left: 0 !important; width: 100% !important;
        background: #000000 !important;
        padding: 10px 5px !important;
        z-index: 999999 !important;
        border-top: 1px solid #FFBB00 !important;
    }}

    div[data-testid="column"] {{
        flex: 1 !important;
        min-width: 0px !important;
        text-align: center !important;
    }}

    div.stButton > button {{
        background: transparent !important; border: none !important;
        color: #aaaaaa !important; font-size: 10px !important;
        padding: 0px !important; width: 100% !important;
        display: flex !important; flex-direction: column !important;
        align-items: center !important;
    }}
    
    .active-tab button {{ color: #FFBB00 !important; font-weight: bold !important; }}
    .neon-card {{ background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 15px; border: 1px solid #FFBB00; margin-bottom: 20px; }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🔐 AUTH
# ==========================================
if not st.session_state.logged_in:
    if st.session_state.page == "Login":
        st.markdown("<div class='neon-card'><h2>🚖 LOGIN</h2>", unsafe_allow_html=True)
        u = st.text_input("नाव")
        p = st.text_input("पासवर्ड", type='password')
        if st.button("LOGIN NOW"):
            users = pd.read_csv(USER_DB)
            if u in users['username'].values:
                db_pass = users[users['username'] == u]['password'].values[0]
                if check_hashes(p, db_pass):
                    st.session_state.logged_in = True; st.session_state.user = u; st.session_state.page = "Home"; st.rerun()
            st.error("चुकीची माहिती!")
        if st.button("Register New"): st.session_state.page = "Register"; st.rerun()

    elif st.session_state.page == "Register":
        st.markdown("<div class='neon-card'><h3>➕ REGISTER</h3>", unsafe_allow_html=True)
        nu = st.text_input("नाव"); nm = st.text_input("मोबाईल"); np = st.text_input("पासवर्ड", type='password')
        if st.button("CREATE"):
            if nu and nm and np:
                pd.DataFrame([[nu, make_hashes(np), nm]], columns=['username', 'password', 'mobile']).to_csv(USER_DB, mode='a', header=False, index=False)
                st.session_state.page = "Login"; st.rerun()

# ==========================================
# 🏠 CONTENT
# ==========================================
else:
    if st.session_state.page == "Home":
        st.markdown("<h2 style='text-align:center;'>🚩 BALAJI LOGISTICS</h2>", unsafe_allow_html=True)
        st.image("https://imgd.aeplcdn.com/1280x720/n/cw/ec/141125/aura-exterior-right-front-three-quarter.jpeg")
        st.markdown(f"<div class='neon-card'><h4>स्वागत आहे, {st.session_state.user}!</h4><p>अंबड आणि पाथर्डी फाटा परिसरात सेवा.</p></div>", unsafe_allow_html=True)

    elif st.session_state.page == "Booking":
        st.markdown("<h2 style='text-align:center;'>📅 BOOK NOW</h2>", unsafe_allow_html=True)
        with st.form("b_form"):
            s = st.text_input("Pickup Point")
            d = st.text_input("Drop Point")
            v = st.selectbox("गाडी", list(RATES.keys()))
            km = st.number_input("किमी", value=50)
            pm = st.radio("पेमेंट", ["Cash", "Online"], horizontal=True)
            if st.form_submit_button("Confirm ✅"):
                u_df = pd.read_csv(USER_DB); mob = u_df[u_df['username'] == st.session_state.user]['mobile'].values[0]
                fare = km * RATES[v]; bid = f"BT{datetime.now().strftime('%d%H%M')}"
                pd.DataFrame([[st.session_state.user, datetime.now().strftime("%d-%m-%Y"), s, d, v, fare, pm]], columns=['username', 'date', 'from_loc', 'to_loc', 'vehicle', 'fare', 'pay_mode']).to_csv(BOOKING_DB, mode='a', header=False, index=False)
                
                msg = (f"🚩 *BALAJI TOURS* 🚩%0A━━━━━━━━━━━━%0A🆔 *ID:* #{bid}%0A👤 *Cust:* {st.session_state.user}%0A📞 *Mob:* {mob}%0A📍 *Pick:* {s}%0A🏁 *Drop:* {d}%0A🚗 *Veh:* {v}%0A💰 *Fare:* ₹{fare}/-%0A━━━━━━━━━━━━")
                st.success("Booking Done!")
                st.markdown(f"### [🚀 व्हॉट्सॲपवर पाठवा](https://wa.me/{WA_LINK_NO}?text={msg})")

    elif st.session_state.page == "History":
        h = pd.read_csv(BOOKING_DB)
        st.dataframe(h[h['username'] == st.session_state.user][['date', 'from_loc', 'to_loc', 'fare']], use_container_width=True)

    # --- 📱 HORIZONTAL BOTTOM MENU ---
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
        st.markdown(f'<a href="tel:{CONTACT_NO}" style="text-decoration:none;"><div style="text-align:center; color:#aaaaaa; font-size:10px; padding-top:5px;">📞<br>Call</div></a>', unsafe_allow_html=True)
        
    with cols[4]:
        if st.button("🚪\nExit"): st.session_state.logged_in = False; st.session_state.page = "Login"; st.rerun()