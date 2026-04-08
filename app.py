import streamlit as st
import pandas as pd
import os
import urllib.parse
from datetime import datetime

# १. ॲप कॉन्फिगरेशन
st.set_page_config(page_title="Balaji Logistics and Tours and Travels", layout="centered")

# २. थीम आणि स्टाईलिंग (रंगांचे प्रॉब्लेम फिक्स केले आहेत)
st.markdown("""
    <style>
    .stApp { background-color: #ffffff !important; }
    input { color: #000000 !important; background-color: #f8f9fa !important; border: 1px solid #0A3D62 !important; }
    label, p, span, .stMarkdown { color: #000000 !important; font-weight: 600; }
    .main-card { background: #ffffff; padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); border: 1px solid #dee2e6; margin-bottom: 20px; }
    .stButton>button { background-color: #0A3D62 !important; color: white !important; border-radius: 8px; height: 48px; width: 100%; font-weight: bold; }
    .fare-box { background-color: #e3f2fd; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #0A3D62; color: #0A3D62; font-size: 20px; font-weight: bold; }
    .wa-button { background-color: #25D366; color: white; padding: 15px; border-radius: 12px; text-align: center; font-weight: bold; display: block; text-decoration: none; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# ३. डेटाबेस सेटअप
USER_DB = "users_data.csv"
BOOKING_DB = "bookings_data.csv"
for db, cols in [(USER_DB, ["Name", "Mobile", "Password"]), (BOOKING_DB, ["Time", "User", "Mobile", "From", "To", "Vehicle", "KM", "Fare", "Payment", "UTR"])]:
    if not os.path.exists(db): pd.DataFrame(columns=cols).to_csv(db, index=False)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- पायरी १: लॉगिन / रजिस्ट्रेशन ---
if not st.session_state.logged_in:
    if os.path.exists("1000326575.png"): st.image("1000326575.png", use_container_width=True)
    st.title("Balaji Logistics and Tours and Travels")
    auth_mode = st.radio("निवडा:", ["Login", "Register"], horizontal=True)
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    if auth_mode == "Register":
        name = st.text_input("तुमचे पूर्ण नाव", key="reg_name")
    mob = st.text_input("मोबाईल नंबर", key="auth_mob")
    pwd = st.text_input("पासवर्ड", type="password", key="auth_pwd")
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
            else: st.error("चुकीचा नंबर किंवा पासवर्ड!")
    st.markdown('</div>', unsafe_allow_html=True)

# --- पायरी २: लॉगिन नंतरचे फीचर्स (आता हे ओपन होईल) ---
else:
    st.sidebar.title("Balaji Logistics")
    st.sidebar.write(f"नमस्ते, **{st.session_state.user_name}**")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # Admin Panel
    if st.sidebar.checkbox("🔒 Admin Panel"):
        if st.sidebar.text_input("Password", type="password") == "balaji123":
            st.subheader("📊 बुकिंग डेटा")
            st.dataframe(pd.read_csv(BOOKING_DB))

    st.title("🚖 तुमची गाडी बुक करा")
    tab1, tab2 = st.tabs(["🚗 प्रवासाची माहिती", "💳 पेमेंट"])

    with tab1:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        p_up = st.text_input("📍 कुठून (Pickup Location)")
        d_off = st.text_input("🏁 कुठे (Drop Location)")
        
        rates = {"Hyundai Aura": 13, "Maruti Ertiga": 15, "Swift Dzire": 12, "Innova Crysta": 20, "Tempo Traveler": 25}
        car = st.selectbox("गाडी निवडा:", list(rates.keys()))
        km = st.number_input("अंदाजे अंतर (KM)", min_value=1, value=10)
        
        fare = km * rates[car]
        st.markdown(f'<div class="fare-box">अंदाजे भाडे: ₹{fare}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        pmode = st.radio("पेमेंट मोड:", ["💵 Cash", "📱 PhonePe Scanner"], horizontal=True)
        utr = ""
        if pmode == "📱 PhonePe Scanner":
            if os.path.exists("1000327329.png"): st.image("1000327329.png", width=250)
            utr = st.text_input("UTR / Transaction ID टाका")
        
        if st.button("Confirm Booking ✅"):
            if p_up and d_off:
                new_b = [datetime.now(), st.session_state.user_name, st.session_state.user_mob, p_up, d_off, car, km, fare, pmode, utr]
                pd.DataFrame([new_b]).to_csv(BOOKING_DB, mode='a', header=False, index=False)
                
                wa_msg = f"*नवीन बुकिंग - Balaji Logistics*\nनाव: {st.session_state.user_name}\nमोबा: {st.session_state.user_mob}\nPickup: {p_up}\nDrop: {d_off}\nगाडी: {car}\nभाडे: ₹{fare}"
                wa_url = f"https://wa.me/919767981986?text={urllib.parse.quote(wa_msg)}"
                
                st.success("बुकिंग यशस्वी!")
                st.markdown(f'<a href="{wa_url}" target="_blank" class="wa-button">📲 WhatsApp वर मालकाला कळवा</a>', unsafe_allow_html=True)
                st.balloons()
            else: st.error("पिकअप आणि ड्रॉप लोकेशन भरा!")
        st.markdown('</div>', unsafe_allow_html=True)