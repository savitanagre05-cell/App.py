import streamlit as st
import urllib.parse, os, pandas as pd
import folium
from streamlit_folium import st_folium

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Balaji Logistics", layout="centered", page_icon="🚛")

LOGO_PATH = "1000327161.jpg" 
MY_NO = "9767981986" # WhatsApp Booking Number
PAY_NO = "9767981986" # PhonePe Number
USER_DB = "users_list.csv" 
HIST_DB = "booking_history.csv" 

# Car Rates (As per your original features)
CAR_MODELS = {"Balaji Go 🚗": 13, "Balaji Sedan 🚙": 17, "Balaji SUV 🚐": 22}

# --- 2. BRANDED UI DESIGN (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    
    .brand-header {
        background: linear-gradient(90deg, #004085 0%, #0056b3 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }
    
    div.stButton > button:first-child {
        background-color: #0056b3;
        color: white;
        border-radius: 8px;
        height: 48px;
        font-weight: bold;
        width: 100%;
        border: none;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #004085;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }
    
    .fare-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 15px;
        border-top: 5px solid #ff8c00;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.05);
    }
    .fare-amount { color: #ff8c00; font-size: 40px; font-weight: bold; margin: 0; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATABASE FUNCTIONS (No Feature Changes) ---
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

# --- 5. LOGIN / REGISTRATION ---
if not st.session_state.auth:
    if os.path.exists(LOGO_PATH):
        col1, col2, col3 = st.columns([1,1,1])
        with col2: st.image(LOGO_PATH, width=150)
    
    st.markdown("""
        <div class="brand-header">
            <h1 style='margin:0;'>🚛 Balaji Logistics 📦</h1>
            <p style='margin:0; font-size:14px;'>Fast • Reliable • Safe</p>
        </div>
    """, unsafe_allow_html=True)
    
    choice = st.radio("Access Your Account:", ["Login", "Register"], horizontal=True)
    
    if choice == "Login":
        l_phone = st.text_input("Mobile Number")
        if st.button("Login ➔"):
            u_name = check_user(l_phone)
            if u_name:
                st.session_state.u = {"n": u_name, "p": l_phone}
                st.session_state.auth = True; st.rerun()
            else: st.error("Number not found. Please Register.")
    else:
        r_name = st.text_input("Full Name")
        r_phone = st.text_input("Mobile Number")
        if st.button("Register Now"):
            if r_name and len(r_phone) == 10:
                save_user(r_name, r_phone); st.session_state.u = {"n": r_name, "p": r_phone}
                st.session_state.auth = True; st.rerun()

# --- 6. MAIN CONTENT (All Original Features) ---
else:
    with st.sidebar:
        if os.path.exists(LOGO_PATH): st.image(LOGO_PATH, width=120)
        st.markdown(f"### Hello, {st.session_state.u['n']}!")
        st.divider()
        if st.button("🏠 Home"): st.session_state.pg = "Home"; st.session_state.step = 1; st.rerun()
        if st.button("🕒 History"): st.session_state.pg = "History"; st.rerun()
        if st.button("📞 Support"): st.session_state.pg = "Support"; st.rerun()
        if st.button("👤 Profile"): st.session_state.pg = "Profile"; st.rerun()
        st.divider()
        if st.button("🚪 Logout"): st.session_state.auth = False; st.rerun()

    if st.session_state.pg == "Home":
        if st.session_state.step == 1:
            st.header("Book Your Journey")
            m = folium.Map(location=[19.9975, 73.7898], zoom_start=12) # Nashik
            st_folium(m, width=700, height=250)
            src = st.text_input("📍 Pickup Location")
            dst = st.text_input("🏁 Drop Location")
            if st.button("Select Vehicle ➔"):
                if src and dst: 
                    st.session_state.route = {"s": src, "d": dst}
                    st.session_state.step = 2; st.rerun()
        
        elif st.session_state.step == 2:
            st.header("Ride & Payment")
            km = st.number_input("Distance (KM)", min_value=1.0, value=5.0)
            car = st.selectbox("Choose Car", list(CAR_MODELS.keys()))
            fare = km * CAR_MODELS[car]
            
            st.markdown(f"<div class='fare-card'><p class='fare-amount'>₹{fare}</p><p style='margin:0; color:#666;'>Estimated Fare</p></div>", unsafe_allow_html=True)
            
            pmode = st.radio("Payment Mode:", ["Cash", "PhonePe / GPay"], horizontal=True)
            if pmode == "PhonePe / GPay":
                st.info(f"Pay to: {PAY_NO}")
                st.text_input("Copy UPI Number:", value=PAY_NO)

            msg = (f"📦 *New Booking - Balaji Logistics*\n👤 User: {st.session_state.u['n']}\n📍 From: {st.session_state.route['s']}\n🏁 To: {st.session_state.route['d']}\n🚗 Car: {car}\n💰 Fare: ₹{fare}\n💳 Payment: {pmode}")
            whatsapp_link = f"https://wa.me/{MY_NO}?text={urllib.parse.quote(msg)}"
            
            if st.button("Confirm Booking & Send WhatsApp ✅"):
                save_booking(st.session_state.u['p'], {"s": st.session_state.route['s'], "d": st.session_state.route['d'], "f": fare, "c": car, "pm": pmode})
                st.markdown(f'<meta http-equiv="refresh" content="0; url={whatsapp_link}">', unsafe_allow_html=True)

    elif st.session_state.pg == "History":
        st.header("🕒 Booking History")
        data = load_history(st.session_state.u['p'])
        for h in reversed(data):
            st.info(f"📍 {h['s']} ➔ {h['d']} | ₹{h['f']}")

    elif st.session_state.pg == "Support":
        st.header("📞 Support")
        st.write(f"Contact us: {MY_NO}")
        st.markdown(f'<a href="https://wa.me/{MY_NO}" style="color:green;">Chat on WhatsApp</a>', unsafe_allow_html=True)

    elif st.session_state.pg == "Profile":
        st.header("👤 Profile")
        st.write(f"Name: {st.session_state.u['n']}")
        st.write(f"Phone: {st.session_state.u['p']}")

    # --- 7. BOTTOM NAVIGATION ---
    st.markdown("---")
    nav = st.columns(5)
    if nav[0].button("🏠"): st.session_state.pg = "Home"; st.session_state.step = 1; st.rerun()
    if nav[1].button("🕒"): st.session_state.pg = "History"; st.rerun()
    if nav[2].button("📞"): st.session_state.pg = "Support"; st.rerun()
    if nav[3].button("👤"): st.session_state.pg = "Profile"; st.rerun()
    if nav[4].button("🚪"): st.session_state.auth = False; st.rerun()