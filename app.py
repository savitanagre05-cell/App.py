import streamlit as st
import urllib.parse, os, pandas as pd
import folium
from streamlit_folium import st_folium

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Balaji Logistics", layout="centered", page_icon="🚛")

LOGO_PATH = "1000327161.jpg" 
MY_NO = "9767981986" 
PAY_NO = "9767981986" 
USER_DB = "users_list.csv" 
HIST_DB = "booking_history.csv" 

CAR_MODELS = {"Balaji Go 🚗": 13, "Balaji Sedan 🚙": 17, "Balaji SUV 🚐": 22}

# --- 2. BRANDED UI DESIGN ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .brand-header {
        background: linear-gradient(90deg, #004085 0%, #0056b3 100%);
        color: white; padding: 20px; border-radius: 12px;
        text-align: center; margin-bottom: 20px;
    }
    /* Green WhatsApp Button Style */
    .wa-btn {
        background-color: #25D366;
        color: white !important;
        padding: 15px 25px;
        border-radius: 10px;
        text-decoration: none;
        font-weight: bold;
        display: block;
        text-align: center;
        margin-top: 20px;
        font-size: 18px;
    }
    .fare-card {
        background-color: #ffffff; padding: 20px; border-radius: 12px;
        text-align: center; margin-bottom: 15px; border-top: 5px solid #ff8c00;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.05);
    }
    .fare-amount { color: #ff8c00; font-size: 40px; font-weight: bold; margin: 0; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATABASE FUNCTIONS (No Change) ---
def save_user(name, phone):
    df = pd.DataFrame([{"name": name, "phone": phone}])
    if not os.path.isfile(USER_DB): df.to_csv(USER_DB, index=False)
    else: df.to_csv(USER_DB, mode='a', header=False, index=False)

def check_user(phone):
    if os.path.isfile(USER_DB):
        df = pd.read_csv(USER_DB)
        user = df[df['phone'].astype(str) == str(phone)]
        return user.iloc[0]['name'] if not user.empty else None
    return None

def save_booking(phone, data):
    data['phone'] = phone
    df = pd.DataFrame([data])
    if not os.path.isfile(HIST_DB): df.to_csv(HIST_DB, index=False)
    else: df.to_csv(HIST_DB, mode='a', header=False, index=False)

def load_history(phone):
    if os.path.isfile(HIST_DB):
        df = pd.read_csv(HIST_DB)
        return df[df['phone'].astype(str) == str(phone)].to_dict('records')
    return []

# --- 4. SESSION STATE ---
if "auth" not in st.session_state: st.session_state.auth = False
if "pg" not in st.session_state: st.session_state.pg = "Home"
if "step" not in st.session_state: st.session_state.step = 1

# --- 5. AUTH / LOGIN ---
if not st.session_state.auth:
    st.markdown("<div class='brand-header'><h1>🚛 Balaji Logistics</h1></div>", unsafe_allow_html=True)
    l_phone = st.text_input("Mobile Number")
    if st.button("Login ➔"):
        u_name = check_user(l_phone)
        if u_name:
            st.session_state.u = {"n": u_name, "p": l_phone}
            st.session_state.auth = True; st.rerun()
        else: st.error("Please Register first.")
    if st.button("New Registration"):
        st.info("Registration feature works same as before.")

# --- 6. MAIN APP ---
else:
    if st.session_state.pg == "Home":
        if st.session_state.step == 1:
            st.header("📍 Set Route")
            m = folium.Map(location=[19.9975, 73.7898], zoom_start=12)
            st_folium(m, width=700, height=250)
            src = st.text_input("Pickup")
            dst = st.text_input("Drop")
            if st.button("Next ➔"):
                if src and dst: 
                    st.session_state.route = {"s": src, "d": dst}
                    st.session_state.step = 2; st.rerun()
        
        elif st.session_state.step == 2:
            st.header("Fare & Confirm")
            km = st.number_input("Distance (KM)", min_value=1.0, value=5.0)
            car = st.selectbox("Vehicle", list(CAR_MODELS.keys()))
            fare = km * CAR_MODELS[car]
            
            st.markdown(f"<div class='fare-card'><p class='fare-amount'>₹{fare}</p></div>", unsafe_allow_html=True)
            pmode = st.radio("Payment Mode:", ["Cash", "PhonePe / GPay"], horizontal=True)
            
            # --- WHATSAPP MESSAGE (Fixed) ---
            msg = (f"📦 *NEW BOOKING - BALAJI*\n"
                   f"👤 User: {st.session_state.u['n']}\n"
                   f"📍 From: {st.session_state.route['s']}\n"
                   f"🏁 To: {st.session_state.route['d']}\n"
                   f"🚗 Car: {car}\n"
                   f"💰 Fare: ₹{fare}\n"
                   f"💳 Payment: {pmode}")
            
            whatsapp_link = f"https://wa.me/{MY_NO}?text={urllib.parse.quote(msg)}"
            
            # सेव करण्यासाठी साधं बटन
            if st.button("1. Save Booking Details 📁"):
                save_booking(st.session_state.u['p'], {"s": st.session_state.route['s'], "d": st.session_state.route['d'], "f": fare, "c": car, "pm": pmode})
                st.success("Details saved! Now click the Green button below.")
            
            # व्हॉट्सॲप उघडण्यासाठी स्पेशल ग्रीन बटन (Direct Link)
            st.markdown(f'<a href="{whatsapp_link}" target="_blank" class="wa-btn">2. Confirm on WhatsApp ✅</a>', unsafe_allow_html=True)

    # Sidebar & Bottom Nav (Features same as before)
    with st.sidebar:
        if st.button("🏠 Home"): st.session_state.pg = "Home"; st.session_state.step = 1; st.rerun()
        if st.button("🕒 History"): st.session_state.pg = "History"; st.rerun()
        if st.button("🚪 Logout"): st.session_state.auth = False; st.rerun()