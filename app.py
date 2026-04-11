import streamlit as st
import time
import pandas as pd
import os
import hashlib
from datetime import datetime

# १. तुझे फिक्स नंबर्स आणि डेटाबेस (No Changes in Features)
CONTACT_NO = "9763158022"    
PAYMENT_NO = "9309146504"    
WA_LINK_NO = "919763158022"  
USER_DB = "users_data.csv"   
BOOKING_DB = "balaji_bookings.csv"

# २. पेज कन्फिगरेशन (Real App Feel)
st.set_page_config(page_title="Balaji Logistics", layout="wide", initial_sidebar_state="collapsed")

# ३. PREMIUM CSS - रियल ॲप औरा आणि लूकसाठी
st.markdown("""
    <style>
    /* Streamlit चे फालतू एलिमेंट्स लपवा */
    header, footer, .stDeployButton, #MainMenu {visibility: hidden;}
    
    /* संपूर्ण ॲप बॅकग्राउंड - Dark Luxury */
    .stApp {
        background: linear-gradient(180deg, #050505 0%, #111111 100%);
        color: white;
    }

    /* प्रीमियम कार्ड्स */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(255, 187, 0, 0.2);
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    /* सर्विस टॅग */
    .service-tag {
        background: linear-gradient(90deg, #FFBB00, #FF8800);
        color: black; padding: 8px 20px; border-radius: 50px;
        font-weight: bold; text-align: center; font-size: 14px;
        display: inline-block; margin-bottom: 10px;
    }

    /* बॉटम नेव्हिगेशन मेनू (Sticky) */
    .nav-bar {
        position: fixed; bottom: 0; left: 0; right: 0;
        background: rgba(10, 10, 10, 0.98);
        padding: 10px 0; border-top: 1.5px solid #FFBB00;
        z-index: 999; display: flex; justify-content: space-around;
    }
    
    /* बटन्स स्टाईल */
    div.stButton > button {
        background-color: transparent !important; color: #888 !important;
        border: none !important; transition: 0.3s; font-weight: normal;
    }
    .active-btn button { color: #FFBB00 !important; font-weight: bold !important; }

    /* इनपुट बॉक्स स्टाईल */
    input { background-color: #1a1a1a !important; color: white !important; border-radius: 10px !important; }
    </style>
""", unsafe_allow_html=True)

# ४. सिक्युरिटी लॉजिक (Your Original Logic)
def make_hashes(password): return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password, hashed_text): return make_hashes(password) == hashed_text

if not os.path.isfile(USER_DB):
    pd.DataFrame(columns=['username', 'password']).to_csv(USER_DB, index=False)

# ५. ॲनिमेटेड फ्लॅश स्क्रीन
if 'flash' not in st.session_state:
    st.markdown("""
        <div style="height: 90vh; display: flex; flex-direction: column; align-items: center; justify-content: center;">
            <h1 style="font-size: 60px; color: #FFBB00; letter-spacing: 10px; text-shadow: 0 0 20px #FFBB00; animation: pulse 2s infinite;">BALAJI</h1>
            <p style="color: white; letter-spacing: 4px; opacity: 0.7;">MAHARASHTRA & ALL INDIA</p>
        </div>
        <style>@keyframes pulse { 0% { opacity: 0.5; } 50% { opacity: 1; } 100% { opacity: 0.5; } }</style>
    """, unsafe_allow_html=True)
    time.sleep(2.5)
    st.session_state.flash = True
    st.rerun()

# ६. स्टेट मॅनेजमेंट
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "Login"

# ७. लॉगिन आणि रजिस्ट्रेशन स्क्रीन
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.session_state.page == "Login":
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color:#FFBB00; text-align:center;'>🚖 LOGIN</h2>", unsafe_allow_html=True)
        u = st.text_input("Username")
        p = st.text_input("Password", type='password')
        if st.button("LOGIN NOW", use_container_width=True):
            users = pd.read_csv(USER_DB)
            if u in users['username'].values and check_hashes(p, users[users['username'] == u]['password'].values[0]):
                st.session_state.logged_in = True; st.session_state.user = u; st.session_state.page = "Home"; st.rerun()
            else: st.error("Invalid Username or Password")
        if st.button("Create New Account"): st.session_state.page = "Register"; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.page == "Register":
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color:#FFBB00; text-align:center;'>➕ REGISTER</h2>", unsafe_allow_html=True)
        new_u = st.text_input("New Username")
        new_p = st.text_input("New Password", type='password')
        if st.button("REGISTER", use_container_width=True):
            if new_u and new_p:
                users = pd.read_csv(USER_DB)
                if new_u in users['username'].values: st.warning("Username Taken!")
                else:
                    new_row = pd.DataFrame([[new_u, make_hashes(new_p)]], columns=['username', 'password'])
                    new_row.to_csv(USER_DB, mode='a', header=False, index=False)
                    st.success("Registered! Go to Login."); time.sleep(1); st.session_state.page = "Login"; st.rerun()
        if st.button("Back to Login"): st.session_state.page = "Login"; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ८. मुख्य ॲप (लॉगिन नंतर)
else:
    if st.session_state.page == "Home":
        st.markdown("<div class='service-tag'>🚩 MAHARASHTRA & ALL INDIA SERVICE</div>", unsafe_allow_html=True)
        st.markdown(f"<h3>Welcome, {st.session_state.user}</h3>", unsafe_allow_html=True)
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1695642938167-17eb9c450c22?q=80&w=1000") # Toyota Innova
        st.markdown("<h4 style='color:#FFBB00;'>💰 दर: १३ रुपये प्रति किमी</h4>", unsafe_allow_html=True)
        st.write("२४ तास नाशिक (अंबड-पाथर्डी) येथून सेवा उपलब्ध.")
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.page == "Booking":
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📝 नवीन बुकिंग")
        with st.form("main_booking"):
            ph = st.text_input("Customer Phone")
            u_from = st.text_input("Pickup Location")
            u_to = st.text_input("Destination")
            cars = {"WagonR": 11, "Swift Dzire": 13, "Ertiga": 18, "Innova": 24, "Tempo": 35}
            v = st.selectbox("Select Car", list(cars.keys()))
            km = st.number_input("Estimated KM", value=100)
            if st.form_submit_button("Confirm & WhatsApp ✅"):
                if ph and u_from and u_to:
                    total = cars[v] * km
                    msg = (f"🚩 *BALAJI LOGISTICS*%0A🌍 *Service:* All India%0A👤 *Cust:* {st.session_state.user}%0A📍 *From:* {u_from}%0A🏁 *To:* {u_to}%0A🚗 *Car:* {v}%0A💰 *Fare:* ₹{total}")
                    st.markdown(f"### [✅ SEND TO WHATSAPP](https://wa.me/{WA_LINK_NO}?text={msg})")
        st.markdown("</div>", unsafe_allow_html=True)

    # ९. REAL APP BOTTOM MENU
    st.write("<br><br><br><br><br>", unsafe_allow_html=True)
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
        if st.button("📞\nCall"): st.success(f"Call: {CONTACT_NO}")
    with c4:
        if st.button("🚪\nExit"): st.session_state.logged_in = False; st.session_state.page="Login"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)