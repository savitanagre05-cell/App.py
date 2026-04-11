import streamlit as st
import time
import pandas as pd
import os
import hashlib
from datetime import datetime

# ==========================================
# 📝 APP CONFIGURATION & NOTES
# ==========================================
WA_LINK_NO = "919767981986"   
CONTACT_NO = "9767981986"     
PAYMENT_NO = "9309146504"     
USER_DB = "users_data.csv"    
BOOKING_DB = "balaji_bookings.csv"

# गाड्यांचे दर (Rates)
RATES = {"WagonR":11, "Swift Dzire":13, "Ertiga":18, "Innova":24, "Tempo Traveller":35}

st.set_page_config(page_title="Balaji Logistics", layout="wide")

# --- सुरक्षा ---
def make_hashes(password): return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password, hashed_text): return make_hashes(password) == hashed_text

if not os.path.isfile(USER_DB): pd.DataFrame(columns=['username', 'password']).to_csv(USER_DB, index=False)
if not os.path.isfile(BOOKING_DB): pd.DataFrame(columns=['username', 'date', 'from_loc', 'to_loc', 'vehicle', 'fare', 'pay_mode']).to_csv(BOOKING_DB, index=False)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "Login"

# ==========================================
# 🎨 COLORFUL NEON UI
# ==========================================
st.markdown("""
    <style>
    header, footer, #MainMenu {visibility: hidden;}
    .stApp { background: linear-gradient(135deg, #000 0%, #0a0a2e 100%); color: white; }
    .neon-card { background: rgba(255, 255, 255, 0.07); padding: 20px; border-radius: 20px; border: 2px solid #FFBB00; box-shadow: 0 0 20px rgba(255, 187, 0, 0.2); margin-bottom: 20px; }
    .nav-bar { background: rgba(15, 15, 45, 0.98); padding: 15px; border-radius: 30px 30px 0 0; border-top: 3px solid #00f2ff; position: fixed; bottom: 0; left: 0; right: 0; z-index: 1000; }
    div.stButton > button { background: #111 !important; color: white !important; border: 1px solid #333 !important; border-radius: 12px !important; }
    .active-btn button { border: 2px solid #00f2ff !important; box-shadow: 0 0 12px #00f2ff; color: #00f2ff !important; font-weight: bold !important; }
    </style>
""", unsafe_allow_html=True)

# --- लॉगिन / रजिस्ट्रेशन ---
if not st.session_state.logged_in:
    if st.session_state.page == "Login":
        st.markdown("<div class='neon-card' style='text-align:center;'><h1>🚖 BALAJI LOGISTICS</h1>", unsafe_allow_html=True)
        u = st.text_input("नाव टाका"); p = st.text_input("पासवर्ड", type='password')
        if st.button("LOGIN NOW"):
            users = pd.read_csv(USER_DB)
            if u in users['username'].values and check_hashes(p, users[users['username'] == u]['password'].values[0]):
                st.session_state.logged_in = True; st.session_state.user = u; st.session_state.page = "Home"; st.rerun()
        if st.button("नवीन ग्राहक? येथे नोंदणी करा"): st.session_state.page = "Register"; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    elif st.session_state.page == "Register":
        st.markdown("<div class='neon-card'><h3>➕ नवीन रजिस्ट्रेशन</h3>", unsafe_allow_html=True)
        nu = st.text_input("पूर्ण नाव"); np = st.text_input("पासवर्ड सेट करा", type='password')
        if st.button("REGISTER"):
            pd.DataFrame([[nu, make_hashes(np)]], columns=['username', 'password']).to_csv(USER_DB, mode='a', header=False, index=False)
            st.success("नोंदणी यशस्वी!"); st.session_state.page = "Login"; time.sleep(1); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- मुख्य होम पेज ---
    if st.session_state.page == "Home":
        st.markdown("<h2 style='color:#00f2ff; text-align:center;'>🚩 BALAJI LOGISTICS</h2>", unsafe_allow_html=True)
        st.image("https://imgd.aeplcdn.com/664x374/n/cw/ec/141125/aura-exterior-right-front-three-quarter.jpeg?isig=0&q=80")
        st.markdown(f"<div class='neon-card'><h4>स्वागत आहे, {st.session_state.user}! ✨</h4><p>स्वच्छ गाड्या आणि सुरक्षित प्रवास - आमचे ध्येय.</p></div>", unsafe_allow_html=True)
        st.warning(f"💳 Payment (PhonePe/GPay): {PAYMENT_NO}")

    # --- बुकिंग पेज ---
    elif st.session_state.page == "Booking":
        st.markdown("<div class='neon-card'><h3>📝 प्रवासाची माहिती भरा</h3>", unsafe_allow_html=True)
        with st.form("book"):
            col1, col2 = st.columns(2)
            with col1: s = st.text_input("पिकअप ठिकाण")
            with col2: d = st.text_input("ड्रॉप ठिकाण")
            v = st.selectbox("गाडी निवडा", list(RATES.keys()))
            km = st.number_input("अंदाजे एकूण किमी", value=100)
            pay = st.radio("पेमेंट मोड", ["PhonePe", "Cash", "Google Pay"], horizontal=True)
            
            if st.form_submit_button("Confirm Booking & Send WhatsApp ✅"):
                fare = km * RATES[v]
                pd.DataFrame([[st.session_state.user, datetime.now().strftime("%d-%m-%Y"), s, d, v, fare, pay]], 
                             columns=['username', 'date', 'from_loc', 'to_loc', 'vehicle', 'fare', 'pay_mode']).to_csv(BOOKING_DB, mode='a', header=False, index=False)
                
                # --- PREMIUM WHATSAPP MESSAGE ---
                msg = (f"🚀 *NEW BOOKING CONFIRMED* 🚀%0A"
                       f"━━━━━━━━━━━━━━━━━━%0A"
                       f"🚩 *BALAJI LOGISTICS*%0A"
                       f"━━━━━━━━━━━━━━━━━━%0A%0A"
                       f"👤 *Cust:* {st.session_state.user}%0A"
                       f"📍 *From:* {s}%0A"
                       f"🏁 *To:* {d}%0A"
                       f"🚗 *Car:* {v}%0A"
                       f"📅 *Date:* {datetime.now().strftime('%d-%m-%Y')}%0A%0A"
                       f"💰 *Estimated Fare:* *₹{fare}*%0A"
                       f"💳 *Payment:* {pay}%0A%0A"
                       f"━━━━━━━━━━━━━━━━━━%0A"
                       f"📌 *महत्त्वाच्या अटी (Notes):*%0A"
                       f"✅ टोल आणि पार्किंग वेगळी असेल.%0A"
                       f"✅ बॉर्डर टॅक्स ग्राहकाचा असेल.%0A"
                       f"✅ जादा किमीचे पैसे लागतील.%0A"
                       f"━━━━━━━━━━━━━━━━━━%0A"
                       f"🙏 *आमच्यावर विश्वास ठेवल्याबद्दल धन्यवाद!*")
                
                st.markdown(f"### [🚀 व्हॉट्सॲपवर बुकिंग पाठवा](https://wa.me/{WA_LINK_NO}?text={msg})")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- हिस्ट्री पेज ---
    elif st.session_state.page == "History":
        st.markdown("<h3 style='color:#FFBB00;'>📊 तुमची बुकिंग हिस्ट्री</h3>", unsafe_allow_html=True)
        h = pd.read_csv(BOOKING_DB)
        u_data = h[h['username'] == st.session_state.user]
        if u_data.empty: st.info("अजून कोणतेही बुकिंग नाही.")
        else: st.dataframe(u_data[['date', 'from_loc', 'to_loc', 'vehicle', 'fare', 'pay_mode']], use_container_width=True)

    # --- ४x३ ग्रिड मेनू ---
    st.write("<br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
    st.markdown('<div class="nav-bar">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.session_state.page == "Home": st.markdown('<div class="active-btn">', unsafe_allow_html=True)
        if st.button("🏠\nHome"): st.session_state.page = "Home"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        if st.session_state.page == "Booking": st.markdown('<div class="active-btn">', unsafe_allow_html=True)
        if st.button("📅\nBook"): st.session_state.page = "Booking"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        if st.button("🚪\nExit"): st.session_state.logged_in = False; st.rerun()
    with c4:
        if st.button("🚩\nJoin"): st.balloons()

    c5, c6, c7 = st.columns(3)
    with c5:
        if st.session_state.page == "History": st.markdown('<div class="active-btn">', unsafe_allow_html=True)
        if st.button("📜\nHistory"): st.session_state.page = "History"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c6:
        if st.button("⚙️\nAdmin"): st.toast("Admin Section")
    with c7:
        if st.button("📞\nCall"): st.success(f"Dial: {CONTACT_NO}")
    st.markdown('</div>', unsafe_allow_html=True)