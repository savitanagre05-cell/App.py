import streamlit as st
import pandas as pd
import os
import urllib.parse
from datetime import datetime

# १. ॲप कॉन्फिगरेशन आणि स्टाईलिंग
st.set_page_config(page_title="Balaji Logistics and Tours and Travels", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff !important; }
    .car-card {
        background: #f8f9fa; padding: 15px; border-radius: 12px;
        border: 2px solid #dee2e6; text-align: center; margin-bottom: 10px;
        transition: 0.3s;
    }
    .car-card:hover { border-color: #0A3D62; background: #e3f2fd; }
    .car-name { color: #0A3D62; font-size: 20px; font-weight: bold; margin-bottom: 5px; }
    .car-rate { color: #28a745; font-size: 16px; font-weight: bold; }
    .main-card { 
        background: #ffffff; padding: 20px; border-radius: 15px; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.1); border: 1px solid #dee2e6; 
    }
    .stButton>button { 
        background-color: #0A3D62 !important; color: white !important; 
        border-radius: 8px; font-weight: bold; 
    }
    label, p, .stMarkdown { color: #000000 !important; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

# २. डेटाबेस सेटअप
USER_DB = "users_data.csv"
BOOKING_DB = "bookings_data.csv"
for db, cols in [(USER_DB, ["Name", "Mobile", "Password"]), (BOOKING_DB, ["Time", "User", "Mobile", "From", "To", "Vehicle", "KM", "Fare", "Payment", "UTR"])]:
    if not os.path.exists(db): pd.DataFrame(columns=cols).to_csv(db, index=False)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'selected_car' not in st.session_state: st.session_state.selected_car = None

# --- लॉगिन विभाग ---
if not st.session_state.logged_in:
    if os.path.exists("1000326575.png"): st.image("1000326575.png", use_container_width=True)
    st.title("Balaji Logistics and Tours and Travels")
    auth_mode = st.radio("निवडा:", ["Login", "Register"], horizontal=True)
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    name = st.text_input("पूर्ण नाव") if auth_mode == "Register" else ""
    mob = st.text_input("मोबाईल नंबर")
    pwd = st.text_input("पासवर्ड", type="password")
    if st.button("प्रवेश करा"):
        df = pd.read_csv(USER_DB)
        if auth_mode == "Register":
            if name and mob and pwd:
                pd.DataFrame([[name, mob, pwd]], columns=["Name", "Mobile", "Password"]).to_csv(USER_DB, mode='a', header=False, index=False)
                st.success("नोंदणी झाली! आता Login करा.")
            else: st.warning("माहिती भरा!")
        else:
            user = df[(df['Mobile'].astype(str) == str(mob)) & (df['Password'].astype(str) == str(pwd))]
            if not user.empty:
                st.session_state.logged_in = True
                st.session_state.user_name = user.iloc[0]['Name']
                st.session_state.user_mob = mob
                st.rerun()
            else: st.error("चुकीची माहिती!")
    st.markdown('</div>', unsafe_allow_html=True)

# --- मुख्य ॲप (Uber Style) ---
else:
    st.sidebar.title("Balaji Logistics")
    st.sidebar.write(f"नमस्ते, **{st.session_state.user_name}**")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.selected_car = None
        st.rerun()

    st.title("🚕 उपलब्ध गाड्या निवडा")

    # १. गाड्यांची लिस्ट (Uber सारखे कार्ड्स)
    car_data = {
        "Swift Dzire": {"rate": 12, "icon": "🚗", "seats": "4+1"},
        "Hyundai Aura": {"rate": 13, "icon": "🚘", "seats": "4+1"},
        "Maruti Ertiga": {"rate": 15, "icon": "🚐", "seats": "6+1"},
        "Innova Crysta": {"rate": 20, "icon": "🚙", "seats": "7+1"},
        "Tempo Traveler": {"rate": 25, "icon": "🚌", "seats": "17+1"}
    }

    cols = st.columns(2)
    for i, (name, info) in enumerate(car_data.items()):
        with cols[i % 2]:
            st.markdown(f"""
                <div class="car-card">
                    <div style='font-size: 40px;'>{info['icon']}</div>
                    <div class="car-name">{name}</div>
                    <div class="car-rate">₹{info['rate']}/km</div>
                    <p style='font-size: 12px; color: gray;'>Seats: {info['seats']}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Select {name}", key=name):
                st.session_state.selected_car = name

    # २. गाडी निवडल्यावर बुकिंग फॉर्म उघडेल
    if st.session_state.selected_car:
        sel = st.session_state.selected_car
        st.markdown("---")
        st.subheader(f"✅ तुम्ही निवडली आहे: {sel}")
        
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["📍 मार्ग", "💳 पेमेंट"])

        with tab1:
            p_up = st.text_input("📍 Pickup Point")
            d_off = st.text_input("🏁 Drop Point")
            km = st.number_input("अंदाजे अंतर (KM)", min_value=1, value=10)
            fare = km * car_data[sel]['rate']
            st.markdown(f"<h3 style='text-align:center;'>एकूण भाडे: ₹{fare}</h3>", unsafe_allow_html=True)

        with tab2:
            pmode = st.radio("पेमेंट:", ["💵 Cash", "📱 PhonePe Scanner"], horizontal=True)
            utr = ""
            if pmode == "📱 PhonePe Scanner":
                if os.path.exists("1000327329.png"): st.image("1000327329.png", width=250)
                utr = st.text_input("Transaction ID (UTR)")
            
            if st.button("Confirm Booking ✅"):
                if p_up and d_off:
                    new_b = [datetime.now(), st.session_state.user_name, st.session_state.user_mob, p_up, d_off, sel, km, fare, pmode, utr]
                    pd.DataFrame([new_b]).to_csv(BOOKING_DB, mode='a', header=False, index=False)
                    
                    wa_msg = f"*नवीन बुकिंग - Balaji Logistics*\nगाडी: {sel}\nनाव: {st.session_state.user_name}\nPickup: {p_up}\nDrop: {d_off}\nभाडे: ₹{fare}"
                    wa_url = f"https://wa.me/919767981986?text={urllib.parse.quote(wa_msg)}"
                    
                    st.success("बुकिंग यशस्वी!")
                    st.markdown(f'<a href="{wa_url}" target="_blank" style="background-color:#25D366; color:white; padding:15px; border-radius:10px; display:block; text-align:center; text-decoration:none;">📲 WhatsApp वर कळवा</a>', unsafe_allow_html=True)
                    st.balloons()
                else: st.error("माहिती अपूर्ण आहे!")
        st.markdown('</div>', unsafe_allow_html=True)