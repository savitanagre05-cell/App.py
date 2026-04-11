import streamlit as st
import time
import pandas as pd
import os
from datetime import datetime
import hashlib

# १. कॉन्फिगरेशन
CONTACT_NO = "9763158022"    
PAYMENT_NO = "9309146504"    
WA_LINK_NO = "919763158022"  
USER_DB = "users_data.csv"   
BOOKING_DB = "balaji_bookings.csv"

st.set_page_config(page_title="Balaji Logistics", layout="wide", page_icon="🚖")

# --- २. फ्लॅश स्क्रीन (Splash Screen) लॉजिक ---
if 'flash_done' not in st.session_state:
    st.session_state.flash_done = False

if not st.session_state.flash_done:
    # ही स्क्रीन ३ सेकंद दिसेल
    st.markdown("""
        <div style="height: 80vh; display: flex; flex-direction: column; align-items: center; justify-content: center; background-color: #000;">
            <h1 style="color: #FFBB00; font-size: 50px; font-family: Arial; margin-bottom: 10px;">🚖 BALAJI LOGISTICS</h1>
            <p style="color: white; font-size: 20px;">Loading your premium ride...</p>
            <div style="border: 4px solid #f3f3f3; border-top: 4px solid #FFBB00; border-radius: 50%; width: 40px; height: 40px; animation: spin 2s linear infinite;"></div>
            <style>
                @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            </style>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(3) # ३ सेकंदाचा वेट
    st.session_state.flash_done = True
    st.rerun()

# --- ३. बाकीचा कोड (सुरक्षा आणि डेटाबेस) ---
def make_hashes(password): return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password, hashed_text): return make_hashes(password) == hashed_text

def save_user(username, password):
    df = pd.DataFrame([[username, make_hashes(password)]], columns=['username', 'password'])
    df.to_csv(USER_DB, mode='a', index=False, header=not os.path.isfile(USER_DB))

def save_booking(data):
    df = pd.DataFrame([data])
    df.to_csv(BOOKING_DB, mode='a', index=False, header=not os.path.isfile(BOOKING_DB))

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "🏠 Home"
if 'user' not in st.session_state: st.session_state.user = ""

# ४. CSS (Black & Gold)
st.markdown(f"""
    <style>
    .stApp {{ background-color: #000; color: white; }}
    .stButton>button {{ background-color: #FFBB00; color: #000; font-weight: bold; border-radius: 10px; }}
    .price-card {{ background-color: #111; padding: 20px; border: 2px solid #FFBB00; border-radius: 12px; text-align: center; }}
    .bottom-nav {{ position: fixed; bottom: 0; left: 0; width: 100%; background-color: #111; padding: 10px 0; border-top: 2px solid #FFBB00; z-index: 999; display: flex; justify-content: space-around; }}
    </style>
""", unsafe_allow_html=True)

# ५. लॉगिन / नोंदणी
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; color:#FFBB00; margin-top:30px;'>🚖 BALAJI LOGISTICS</h1>", unsafe_allow_html=True)
    auth_tab = st.tabs(["Login", "Register"])
    with auth_tab[0]:
        u_name = st.text_input("Username")
        u_pw = st.text_input("Password", type='password')
        if st.button("Login"):
            if os.path.isfile(USER_DB):
                users = pd.read_csv(USER_DB)
                if u_name in users['username'].values:
                    if check_hashes(u_pw, users[users['username'] == u_name]['password'].values[0]):
                        st.session_state.logged_in = True
                        st.session_state.user = u_name
                        st.rerun()
                else: st.error("User not found!")

    with auth_tab[1]:
        n_user = st.text_input("New Username")
        n_pw = st.text_input("New Password", type='password')
        if st.button("Register"):
            save_user(n_user, n_pw)
            st.success("Registration Done!")

# ६. मुख्य ॲप
else:
    if st.session_state.page == "🏠 Home":
        st.markdown(f"<h1 style='text-align:center; color:#FFBB00;'>BALAJI LOGISTICS</h1>", unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?q=80&w=1000")
        st.write(f"### Welcome, {st.session_state.user}!")
        st.markdown(f"<a href='tel:{CONTACT_NO}' style='display:block; padding:15px; background-color:#FFBB00; color:black; text-align:center; font-weight:bold; text-decoration:none; border-radius:10px;'>📞 Call: {CONTACT_NO}</a>", unsafe_allow_html=True)

    elif st.session_state.page == "📝 Book":
        with st.form("booking"):
            phone = st.text_input("Mobile")
            pick = st.text_input("Pickup")
            drop = st.text_input("Destination")
            cars = {"Swift Dzire": 13, "Ertiga": 18, "Innova": 24, "Tempo": 35}
            sel_car = st.selectbox("Car", list(cars.keys()))
            km = st.slider("KM", 10, 1000, 100)
            total = cars[sel_car] * km
            if st.radio("Pay", ["Cash", "PhonePe"]) == "PhonePe":
                st.info(f"📱 PhonePe: {PAYMENT_NO}")
            st.markdown(f"<div class='price-card'><h3>Fare: ₹{total}/-</h3></div>", unsafe_allow_html=True)
            if st.form_submit_button("Confirm ✅"):
                save_booking({"User": st.session_state.user, "Phone": phone, "Route": f"{pick}-{drop}", "Car": sel_car, "Fare": total, "Date": datetime.now().strftime("%d-%m")})
                msg = f"🚀 *NEW BOOKING*%0A👤 {st.session_state.user}%0A💰 ₹{total}/-"
                st.markdown(f"### [✅ WhatsApp](https://wa.me/{WA_LINK_NO}?text={msg})")

    elif st.session_state.page == "📊 History":
        if os.path.isfile(BOOKING_DB):
            df = pd.read_csv(BOOKING_DB)
            st.dataframe(df[df['User'] == st.session_state.user], use_container_width=True)

    elif st.session_state.page == "🚪 Out":
        st.session_state.logged_in = False
        st.rerun()

    # --- ७. खालचा 'BOTTOM MENU' ---
    st.write("<br><br><br><br>", unsafe_allow_html=True)
    st.markdown('<div class="bottom-nav">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("🏠 Home"): st.session_state.page = "🏠 Home"; st.rerun()
    if c2.button("📝 Book"): st.session_state.page = "📝 Book"; st.rerun()
    if c3.button("📊 History"): st.session_state.page = "📊 History"; st.rerun()
    if c4.button("🚪 Out"): st.session_state.page = "🚪 Out"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)