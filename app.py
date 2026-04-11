import streamlit as st
import time
import pandas as pd
import os
from datetime import datetime
import hashlib

# १. कॉन्फिगरेशन (तुझ्या सांगण्याप्रमाणे ९७ आणि ९३ चे नंबर्स)
CONTACT_NO = "9763158022"    # Calling आणि WhatsApp साठी
PAYMENT_NO = "9309146504"    # फक्त PhonePe पेमेंटसाठी
WA_LINK_NO = "919763158022"  # WhatsApp API साठी (91 सह)
USER_DB = "users_data.csv"   
BOOKING_DB = "balaji_bookings.csv"

st.set_page_config(page_title="Balaji Logistics & Travels", layout="wide", page_icon="🚖")

# २. सुरक्षा आणि डेटा सेव्हिंग फंक्शन्स
def make_hashes(password): return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password, hashed_text): return make_hashes(password) == hashed_text

def save_user(username, password):
    df = pd.DataFrame([[username, make_hashes(password)]], columns=['username', 'password'])
    df.to_csv(USER_DB, mode='a', index=False, header=not os.path.isfile(USER_DB))

def save_booking(data):
    df = pd.DataFrame([data])
    df.to_csv(BOOKING_DB, mode='a', index=False, header=not os.path.isfile(BOOKING_DB))

# ३. सेशन स्टेट (नेव्हिगेशन आणि लॉगिनसाठी)
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "🏠 Home"
if 'user' not in st.session_state: st.session_state.user = ""

# ४. प्रीमियम CSS थीम (Black & Gold + Bottom Nav)
st.markdown(f"""
    <style>
    .stApp {{ background-color: #000; color: white; }}
    .stButton>button {{ background-color: #FFBB00; color: #000; font-weight: bold; border-radius: 10px; width: 100%; }}
    .price-card {{ background-color: #111; padding: 20px; border: 2px solid #FFBB00; border-radius: 12px; text-align: center; }}
    .call-btn {{ display: block; width: 100%; padding: 15px; background-color: #FFBB00; color: black; text-align: center; font-weight: bold; text-decoration: none; border-radius: 10px; margin: 10px 0; }}
    
    /* खालचा फिक्स मेनू बार (Bottom Navigation) */
    .bottom-nav {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #111;
        padding: 10px 0;
        border-top: 2px solid #FFBB00;
        z-index: 999;
        display: flex;
        justify-content: space-around;
    }}
    </style>
""", unsafe_allow_html=True)

# ५. लॉगिन आणि नोंदणी विभाग (Authentic Login/Register)
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; color:#FFBB00; margin-top:30px;'>🚖 BALAJI LOGISTICS</h1>", unsafe_allow_html=True)
    st.write("<p style='text-align:center;'>सर्वोत्तम टूर्स अँड ट्रॅव्हल्स सर्व्हिस</p>", unsafe_allow_html=True)
    
    auth_tab = st.tabs(["लॉगिन (Login)", "नोंदणी (Register)"])
    
    with auth_tab[0]: # LOGIN
        u_name = st.text_input("युझरनेम (Username)")
        u_pw = st.text_input("पासवर्ड (Password)", type='password')
        if st.button("प्रवेश करा / Login"):
            if os.path.isfile(USER_DB):
                users = pd.read_csv(USER_DB)
                if u_name in users['username'].values:
                    hashed = users[users['username'] == u_name]['password'].values[0]
                    if check_hashes(u_pw, hashed):
                        st.session_state.logged_in = True
                        st.session_state.user = u_name
                        st.rerun()
                else: st.error("युझर सापडला नाही!")
            else: st.error("आधी नोंदणी करा.")

    with auth_tab[1]: # REGISTER
        n_user = st.text_input("नवीन युझरनेम")
        n_pw = st.text_input("नवीन पासवर्ड", type='password')
        if st.button("नोंदणी करा / Register"):
            if n_user and n_pw:
                save_user(n_user, n_pw)
                st.success("नोंदणी झाली! आता लॉगिन करा.")
            else: st.warning("सर्व माहिती भरा.")

# ६. मुख्य ॲप (लॉगिन झाल्यावरच दिसेल)
else:
    # --- पेज लॉजिक ---
    if st.session_state.page == "🏠 Home":
        st.markdown(f"<h1 style='text-align:center; color:#FFBB00;'>बालाजी लॉजिस्टिक</h1>", unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?q=80&w=1000")
        st.write(f"### स्वागत आहे, {st.session_state.user}! 👋")
        st.write("तुमच्या प्रवासासाठी सर्वोत्तम गाड्यांचे बुकिंग करा.")
        st.markdown(f"<a href='tel:{CONTACT_NO}' class='call-btn'>📞 आत्ताच कॉल करा: {CONTACT_NO}</a>", unsafe_allow_html=True)

    elif st.session_state.page == "📝 Book":
        st.subheader("📝 नवीन बुकिंग")
        with st.form("booking_form"):
            phone = st.text_input("मोबाईल नंबर")
            pick = st.text_input("कुठून (Pickup)")
            drop = st.text_input("कुठे (Destination)")
            
            cars = {"Swift Dzire": 13, "Ertiga (6+1)": 18, "Innova Crysta": 24, "Tempo Traveller": 35}
            car_choice = st.selectbox("गाडी निवडा", list(cars.keys()))
            km = st.slider("अंतर (KM)", 10, 1000, 100)
            total_fare = cars[car_choice] * km
            
            pay = st.radio("पेमेंट मोड", ["Cash", "PhonePe"])
            if pay == "PhonePe":
                st.info(f"📱 PhonePe Number: {PAYMENT_NO}")
            
            st.markdown(f"<div class='price-card'><h3>भाडे: ₹{total_fare}/-</h3></div>", unsafe_allow_html=True)
            st.write("*(Note: Toll & Parking Extra)*")
            
            if st.form_submit_button("बुकिंग कन्फर्म करा ✅"):
                if phone and pick and drop:
                    # डेटा सेव्ह
                    b_data = {"User": st.session_state.user, "Phone": phone, "Route": f"{pick}-{drop}", "Car": car_choice, "Fare": total_fare, "Date": datetime.now().strftime("%d-%m-%y")}
                    save_booking(b_data)
                    # WhatsApp मेसेज
                    msg = f"🚀 *NEW BOOKING*%0A👤 {st.session_state.user}%0A📞 {phone}%0A📍 {pick} to {drop}%0A🚗 {car_choice}%0A💰 ₹{total_fare}/-"
                    st.markdown(f"### [✅ WhatsApp वर पाठवा](https://wa.me/{WA_LINK_NO}?text={msg})")
                else: st.error("माहिती अपूर्ण आहे!")

    elif st.session_state.page == "📊 History":
        st.subheader("📊 तुमची बुकिंग हिस्ट्री")
        if os.path.isfile(BOOKING_DB):
            df = pd.read_csv(BOOKING_DB)
            st.dataframe(df[df['User'] == st.session_state.user], use_container_width=True)
        else: st.info("हिस्ट्री उपलब्ध नाही.")

    elif st.session_state.page == "🚪 Out":
        st.session_state.logged_in = False
        st.rerun()

    # --- ७. खालचा 'BOTTOM MENU BAR' ---
    st.write("<br><br><br><br>", unsafe_allow_html=True)
    st.markdown('<div class="bottom-nav">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("🏠 Home"): st.session_state.page = "🏠 Home"; st.rerun()
    if c2.button("📝 Book"): st.session_state.page = "📝 Book"; st.rerun()
    if c3.button("📊 History"): st.session_state.page = "📊 History"; st.rerun()
    if c4.button("🚪 Out"): st.session_state.page = "🚪 Out"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)