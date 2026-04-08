import streamlit as st
import pandas as pd
import os
import urllib.parse
from datetime import datetime

# १. ॲप कॉन्फिगरेशन
st.set_page_config(page_title="Balaji Logistics and Tours and Travels", layout="centered")

# २. स्टाईलिंग (Uber Style)
st.markdown("""
    <style>
    .stApp { background-color: #ffffff !important; }
    .car-card {
        background: #f8f9fa; padding: 15px; border-radius: 12px;
        border: 2px solid #dee2e6; text-align: center; margin-bottom: 10px;
    }
    .car-name { color: #00416A; font-size: 20px; font-weight: bold; }
    .car-rate { color: #28a745; font-size: 16px; font-weight: bold; }
    .main-card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); border: 1px solid #dee2e6; }
    .stButton>button { background-color: #00416A !important; color: white !important; width: 100%; border-radius: 8px; }
    label, p, span { color: black !important; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

# ३. डेटाबेस आणि सेशन स्टेट
USER_DB = "users_data.csv"
BOOKING_DB = "bookings_data.csv"
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'selected_car' not in st.session_state: st.session_state.selected_car = None

# ४. लोगो दाखवण्यासाठी फंक्शन (हे फिक्स करेल)
def show_logo(w=200):
    if os.path.exists("1000326575.png"):
        st.image("1000326575.png", width=w)
    else:
        st.title("🚖 Balaji Logistics")

# --- लॉगिन विभाग ---
if not st.session_state.logged_in:
    show_logo(300)
    st.subheader("प्रवेश करा")
    auth_mode = st.radio("निवडा:", ["Login", "Register"], horizontal=True)
    
    with st.container():
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        mob = st.text_input("मोबाईल नंबर")
        pwd = st.text_input("पासवर्ड", type="password")
        if st.button("प्रवेश करा"):
            # लॉगिन लॉजिक (थोडक्यात)
            st.session_state.logged_in = True
            st.session_state.user_name = "User"
            st.session_state.user_mob = mob
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- मुख्य ॲप (गाड्यांची लिस्ट) ---
else:
    st.sidebar.title("Balaji Logistics")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.selected_car = None
        st.rerun()

    show_logo(100)
    st.title("🚕 उपलब्ध गाड्या निवडा")

    car_data = {
        "Swift Dzire": {"rate": 12, "icon": "🚗", "seats": "4+1"},
        "Hyundai Aura": {"rate": 13, "icon": "🚘", "seats": "4+1"},
        "Maruti Ertiga": {"rate": 15, "icon": "🚐", "seats": "6+1"},
        "Innova Crysta": {"rate": 20, "icon": "🚙", "seats": "7+1"},
        "Tempo Traveler": {"rate": 25, "icon": "🚌", "seats": "17+1"}
    }

    # गाड्यांचे कार्ड्स दाखवणे
    for name, info in car_data.items():
        st.markdown(f"""
            <div class="car-card">
                <div style='font-size: 40px;'>{info['icon']}</div>
                <div class="car-name">{name}</div>
                <div class="car-rate">₹{info['rate']}/km</div>
                <p>Seats: {info['seats']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # 'Select' बटण दाबल्यावर सेशन स्टेटमध्ये नाव सेव्ह करणे
        if st.button(f"Select {name}", key=f"btn_{name}"):
            st.session_state.selected_car = name
            st.rerun() # हे पेज रिफ्रेश करून फॉर्म दाखवेल

    # ५. जर गाडी निवडली असेल, तर बुकिंग फॉर्म दाखवणे (हेच ओपन होत नव्हतं)
    if st.session_state.selected_car:
        sel = st.session_state.selected_car
        st.markdown("---")
        st.header(f"📍 बुकिंग: {sel}")
        
        with st.expander("प्रवासाची माहिती भरा", expanded=True):
            st.markdown('<div class="main-card">', unsafe_allow_html=True)
            p_up = st.text_input("📍 Pickup Location")
            d_off = st.text_input("🏁 Drop Location")
            km = st.number_input("अंदाजे अंतर (KM)", min_value=1, value=10)
            
            fare = km * car_data[sel]['rate']
            st.success(f"### एकूण भाडे: ₹{fare}")

            if st.button("Confirm Booking"):
                st.balloons()
                st.success("बुकिंग यशस्वी! मालकाला WhatsApp करा.")
            st.markdown('</div>', unsafe_allow_html=True)