import streamlit as st
import time
import pandas as pd
import os
from datetime import datetime
import hashlib

# १. तुझे नंबर्स (No Changes)
CONTACT_NO = "9763158022"    
PAYMENT_NO = "9309146504"    
WA_LINK_NO = "919763158022"  
USER_DB = "users_data.csv"   
BOOKING_DB = "balaji_bookings.csv"

st.set_page_config(page_title="Balaji Logistics", layout="wide")

# २. ॲनिमेटेड फ्लॅश स्क्रीन
if 'flash' not in st.session_state:
    st.markdown("""
        <style>
        @keyframes glow { 0% { text-shadow: 0 0 5px #FFBB00; } 50% { text-shadow: 0 0 20px #FFBB00; } 100% { text-shadow: 0 0 5px #FFBB00; } }
        .flash { height: 90vh; display: flex; flex-direction: column; align-items: center; justify-content: center; background-color: #000; color: #FFBB00; }
        .title { font-size: 55px; font-weight: bold; animation: glow 2s infinite; letter-spacing: 5px; }
        </style>
        <div class="flash"><div class="title">BALAJI</div><p style='color:white;'>MAHARASHTRA & ALL INDIA</p></div>
    """, unsafe_allow_html=True)
    time.sleep(2.5)
    st.session_state.flash = True
    st.rerun()

# ३. लॉजिक
def make_hashes(password): return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password, hashed_text): return make_hashes(password) == hashed_text

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "Home"

# ४. थीम आणि ग्रिड मेनू स्टाईल
st.markdown("""
    <style>
    .stApp { background-color: #000; color: white; }
    .menu-box {
        background-color: #111; padding: 15px; border-radius: 10px; border: 1px solid #333;
        position: fixed; bottom: 10px; left: 5%; right: 5%; z-index: 1000;
    }
    div.stButton > button { background-color: transparent !important; color: white !important; border: none !important; font-size: 12px !important; width: 100%; }
    .active-btn button { background-color: #FFBB00 !important; color: black !important; font-weight: bold !important; border-radius: 5px !important; }
    .service-tag { background: #FFBB00; color: black; padding: 8px 15px; border-radius: 5px; font-weight: bold; text-align: center; margin-bottom: 15px; }
    
    /* आणि 'Aura' साठी नवीन CSS */
    .business-aura {
        background: radial-gradient(circle, #222 0%, #000 70%);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #FFBB00;
        text-align: center;
        box-shadow: 0 0 15px #FFBB00;
        margin-bottom: 20px;
    }
    .main-logo {
        font-size: 45px;
        font-weight: 900;
        letter-spacing: 5px;
        color: #FFBB00;
        text-shadow: 0 0 10px #FFBB00;
        margin-bottom: 10px;
    }
    .aura-subtitle {
        color: white;
        opacity: 0.8;
        letter-spacing: 2px;
    }
    </style>
""", unsafe_allow_html=True)

# ५. मुख्य कंटेंट
if not st.session_state.logged_in:
    st.markdown("<h2 style='color:#FFBB00; text-align:center;'>🚖 BALAJI LOGIN</h2>", unsafe_allow_html=True)
    u = st.text_input("Username")
    p = st.text_input("Password", type='password')
    if st.button("Login"):
        if os.path.isfile(USER_DB):
            users = pd.read_csv(USER_DB)
            if u in users['username'].values and check_hashes(p, users[users['username'] == u]['password'].values[0]):
                st.session_state.logged_in = True; st.session_state.user = u; st.rerun()
else:
    if st.session_state.page == "Home":
        st.markdown("<div class='service-tag'>🚩 MAHARASHTRA & ALL INDIA SERVICE 🌍</div>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#FFBB00; text-align:center;'>💰 दर: १३ रुपये प्रति किलोमीटर</h4>", unsafe_allow_html=True)
        
        # --- आणि 'Business Aura' सेक्शन (फोटो आणि ब्रँडिंग) ---
        st.markdown("""
            <div class="business-aura">
                <div class="main-logo">BALAJI</div>
                <div class="aura-subtitle">LOGISTICS & TOURS</div>
            </div>
        """, unsafe_allow_html=True)
        
        # तीच गाडीचा फोटो (Toyota Innova)
        st.image("https://images.unsplash.com/photo-1695642938167-17eb9c450c22?q=80&w=1000")
        
        st.markdown("""
            <div style='text-align:center;'>
                <p style='font-size:18px;'>आमची प्रीमियम आणि विश्वसनीय सेवा तुमच्यासाठी.</p>
                <p style='color:#888;'>नाशिक (अंबड आणि पाथर्डी फाटा) येथून २४ तास बुकिंग सुरू.</p>
            </div>
        """, unsafe_allow_html=True)

    elif st.session_state.page == "Booking":
        st.subheader("📝 Booking Form (Maharashtra & India)")
        with st.form("all_india_booking"):
            phone = st.text_input("Customer Mobile")
            u_from = st.text_input("Pickup City/Area")
            u_to = st.text_input("Destination City (India)")
            cars = {"WagonR": 11, "Swift Dzire": 13, "Ertiga": 18, "Innova": 24, "Tempo": 35}
            sel_car = st.selectbox("Vehicle", list(cars.keys()))
            km = st.number_input("Estimated KM", value=100)
            pay = st.radio("Payment Mode", ["Cash", "PhonePe"], horizontal=True)
            st.error("⚠️ Note: Toll, Parking & Border Tax Extra")
            
            if st.form_submit_button("Confirm on WhatsApp ✅"):
                if phone and u_from and u_to:
                    msg = (f"🚀 *NEW BOOKING - BALAJI LOGISTICS*%0A"
                           f"🌍 *Service:* Maharashtra & All India%0A"
                           f"👤 *Cust:* {st.session_state.user}%0A"
                           f"📞 *Mob:* {phone}%0A"
                           f"📍 *Pickup:* {u_from}%0A"
                           f"🏁 *Drop:* {u_to}%0A"
                           f"🚗 *Car:* {sel_car}%0A"
                           f"💰 *Fare:* ₹{cars[sel_car]*km}%0A"
                           f"⚠️ *Note:* Toll, Parking & Border Tax Extra")
                    st.markdown(f"### [✅ SEND NOW](https://wa.me/{WA_LINK_NO}?text={msg})")

    # ६. फोटोसारखा GRID MENU (४ x ३) - No Changes
    st.write("<br><br><br><br><br><br><br>", unsafe_allow_html=True)
    st.markdown('<div class="menu-box">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.session_state.page == "Home": st.markdown('<div class="active-btn">', unsafe_allow_html=True)
        if st.button("🏠\nHome"): st.session_state.page = "Home"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        if st.session_state.page == "Booking": st.markdown('<div class="active-btn">', unsafe_allow_html=True)
        if st.button("📖\nBooking"): st.session_state.page = "Booking"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        if st.button("🔐\nLogout"): st.session_state.logged_in = False; st.rerun()
    with c4:
        if st.button("➕\nRegister"): st.info("Logged In")

    c5, c6, c7 = st.columns(3)
    with c5:
        if st.button("⏲️\nHistory"): st.info("Dashboard")
    with c6:
        if st.button("🛡️\nAdmin"): st.warning("Locked")
    with c7:
        if st.button("📞\nContact"): st.success(f"{CONTACT_NO}")
    st.markdown('</div>', unsafe_allow_html=True)