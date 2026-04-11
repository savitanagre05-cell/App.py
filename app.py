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
PHONEPE_NO = "9309146504"  # तुझा PhonePe नंबर
USER_DB = "users_data.csv"    
BOOKING_DB = "balaji_bookings.csv"
RATES = {"WagonR":11, "Swift Dzire":13, "Ertiga":18, "Innova":24, "Tempo Traveller":35}

# Sidebar नेव्हिगेशन दिसण्यासाठी 'expanded' ठेवले आहे
st.set_page_config(page_title="Balaji Logistics", layout="wide", initial_sidebar_state="expanded")

# --- Security Functions ---
def make_hashes(password): return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password, hashed_text): return make_hashes(password) == hashed_text

# Database Files तयार करणे
if not os.path.isfile(USER_DB): pd.DataFrame(columns=['username', 'password', 'mobile']).to_csv(USER_DB, index=False)
if not os.path.isfile(BOOKING_DB): pd.DataFrame(columns=['username', 'date', 'from_loc', 'to_loc', 'vehicle', 'fare', 'pay_mode']).to_csv(BOOKING_DB, index=False)

# Session States
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user' not in st.session_state: st.session_state.user = ""
if 'flash_done' not in st.session_state: st.session_state.flash_done = False

# ==========================================
# ⚡ FLASH SCREEN (ब्लॅक स्क्रीन फिक्स)
# ==========================================
if not st.session_state.flash_done:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown(f"""
            <style>
            .flash-bg {{ position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: black; z-index: 9999; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
            .flash-logo {{ font-size: 45px; color: #FFBB00; font-weight: bold; text-align: center; font-family: sans-serif; }}
            </style>
            <div class='flash-bg'><div class='flash-logo'>🚩 BALAJI<br><span style='font-size:20px; color:white;'>TOUR'S AND TRAVELS</span></div></div>
        """, unsafe_allow_html=True)
        time.sleep(2.5)
    st.session_state.flash_done = True
    placeholder.empty()
    st.rerun()

# ==========================================
# 🎨 UI STYLES (Neon Theme)
# ==========================================
st.markdown(f"""
    <style>
    header, footer, #MainMenu {{visibility: hidden;}}
    .stApp {{ background: linear-gradient(135deg, #000 0%, #0a0a2e 100%); color: white; }}
    .neon-card {{ background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 15px; border: 1px solid #FFBB00; margin-bottom: 20px; }}
    
    /* Input fields styling */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {{
        background-color: #1a1a1a !important; color: white !important; border: 1px solid #FFBB00 !important;
    }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🔐 LOGIN & REGISTER
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center; color:#FFBB00;'>🚩 BALAJI LOGISTICS</h2>", unsafe_allow_html=True)
    auth_choice = st.radio("पर्याय निवडा", ["Login", "Register"], horizontal=True)
    
    if auth_choice == "Login":
        with st.container():
            u = st.text_input("Username")
            p = st.text_input("Password", type='password')
            if st.button("LOGIN NOW"):
                users = pd.read_csv(USER_DB)
                if u in users['username'].values:
                    db_p = users[users['username'] == u]['password'].values[0]
                    if check_hashes(p, db_p):
                        st.session_state.logged_in = True; st.session_state.user = u; st.rerun()
                st.error("चुकीची माहिती! कृपया पुन्हा प्रयत्न करा.")
    else:
        with st.container():
            nu = st.text_input("तुमचे पूर्ण नाव")
            nm = st.text_input("मोबाईल नंबर")
            np = st.text_input("नवीन पासवर्ड", type='password')
            if st.button("CREATE ACCOUNT"):
                if nu and nm and np:
                    pd.DataFrame([[nu, make_hashes(np), nm]], columns=['username', 'password', 'mobile']).to_csv(USER_DB, mode='a', header=False, index=False)
                    st.success("रजिस्ट्रेशन यशस्वी! आता लॉगिन करा.")
                else:
                    st.warning("सर्व माहिती भरणे आवश्यक आहे.")

# ==========================================
# 🏠 MAIN APP CONTENT
# ==========================================
else:
    # --- SIDEBAR नेव्हिगेशन ---
    with st.sidebar:
        st.markdown("<h2 style='color:#FFBB00;'>🚩 Balaji Menu</h2>", unsafe_allow_html=True)
        st.write(f"User: **{st.session_state.user}**")
        menu = st.radio("Navigation", ["Home", "Booking", "History"])
        st.markdown("---")
        st.markdown(f"📞 [Call Support](tel:{CONTACT_NO})")
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.rerun()

    # --- HOME PAGE ---
    if menu == "Home":
        st.markdown("<h2 style='text-align:center;'>🚩 BALAJI LOGISTICS</h2>", unsafe_allow_html=True)
        st.image("https://imgd.aeplcdn.com/1280x720/n/cw/ec/141125/aura-exterior-right-front-three-quarter.jpeg")
        st.markdown(f"""
            <div class='neon-card'>
                <h4>स्वागत आहे, {st.session_state.user}!</h4>
                <p style='color:#FFBB00; font-weight:bold; font-size:18px;'>MAHARASHTRA AND ALL INDIA SERVICE.</p>
                <p>अत्यंत रास्त दरात सुरक्षित प्रवास.</p>
            </div>
        """, unsafe_allow_html=True)

    # --- BOOKING PAGE ---
    elif menu == "Booking":
        st.markdown("<h2 style='text-align:center;'>📅 BOOK NOW</h2>", unsafe_allow_html=True)
        with st.form("booking_form"):
            col1, col2 = st.columns(2)
            with col1:
                s = st.text_input("Pickup Point")
                v = st.selectbox("गाडी निवडा", list(RATES.keys()))
            with col2:
                d = st.text_input("Drop Point")
                km = st.number_input("अंदाजे किमी", value=50, min_value=1)
            
            pay_mode = st.radio("पेमेंट मोड", ["Cash", "Online"], horizontal=True)
            
            if st.form_submit_button("Booking Confirm करा ✅"):
                if s and d:
                    fare = km * RATES[v]
                    bid = f"BT{datetime.now().strftime('%d%H%M')}"
                    
                    # डेटाबेसमध्ये बुकिंग सेव्ह करणे
                    pd.DataFrame([[st.session_state.user, datetime.now().strftime("%d-%m-%Y"), s, d, v, fare, pay_mode]], 
                                 columns=['username', 'date', 'from_loc', 'to_loc', 'vehicle', 'fare', 'pay_mode']).to_csv(BOOKING_DB, mode='a', header=False, index=False)
                    
                    st.success(f"बुकिंग झाले! एकूण भाडे: ₹{fare}")
                    
                    # Payment Note
                    pay_note = ""
                    if pay_mode == "Online":
                        st.warning(f"कृपया PhonePe वर पेमेंट करा: {PHONEPE_NO}")
                        pay_note = f"%0A💳 *Payment:* Online (PhonePe: {PHONEPE_NO})"
                    else:
                        pay_note = "%0A💳 *Payment:* Cash to Driver"

                    # WhatsApp Message Formatting
                    msg = (f"🚩 *BALAJI TOURS* 🚩%0A━━━━━━━━━━━━%0A🆔 *ID:* #{bid}%0A👤 *Cust:* {st.session_state.user}%0A📍 *Pick:* {s}%0A🏁 *Drop:* {d}%0A🚗 *Veh:* {v}%0A💰 *Fare:* ₹{fare}/-{pay_note}%0A━━━━━━━━━━━━%0A⚠️ *Note: Toll & Parking charges extra.*%0A━━━━━━━━━━━━%0A🙏 *Thank you for choosing Balaji!*")
                    
                    st.markdown(f"### [🚀 व्हॉट्सॲपवर माहिती पाठवा](https://wa.me/{WA_LINK_NO}?text={msg})")
                else:
                    st.error("कृपया पिकअप आणि ड्रॉप लोकेशन टाका.")

    # --- HISTORY PAGE ---
    elif menu == "History":
        st.markdown("<h2 style='text-align:center;'>📜 BOOKING HISTORY</h2>", unsafe_allow_html=True)
        if os.path.exists(BOOKING_DB):
            h_df = pd.read_csv(BOOKING_DB)
            user_h = h_df[h_df['username'] == st.session_state.user]
            if not user_h.empty():
                st.dataframe(user_h[['date', 'from_loc', 'to_loc', 'vehicle', 'fare', 'pay_mode']], use_container_width=True)
            else:
                st.info("अजून कोणतीही बुकिंग केलेली नाही.")