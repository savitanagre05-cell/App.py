import streamlit as st
import urllib.parse, os, pandas as pd
import folium
from streamlit_folium import st_folium

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Balaji Logistics", layout="centered", page_icon="📦")

LOGO_PATH = "1000327161.jpg" 
MY_NO = "9767981986" 
PAY_NO = "9767981986" 
USER_DB = "users_list.csv" 
HIST_DB = "booking_history.csv" 

CAR_MODELS = {"Balaji Go 🚗": 13, "Balaji Sedan 🚙": 17, "Balaji SUV 🚐": 22}

# --- 2. PREMIUM CSS (Style only, no feature change) ---
st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; }
    div.stButton > button:first-child {
        background: #000000;
        color: white;
        border-radius: 8px;
        height: 45px;
        font-weight: bold;
        width: 100%;
    }
    .status-card {
        background: #000;
        color: #FFD700;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATABASE FUNCTIONS (Old Features) ---
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

# --- 5. LOGIN / REGISTRATION (English - As requested) ---
if not st.session_state.auth:
    if os.path.exists(LOGO_PATH): st.image(LOGO_PATH, width=150)
    st.title("Balaji Logistics")
    choice = st.radio("Choose:", ["Login", "Register"], horizontal=True)
    if choice == "Login":
        l_phone = st.text_input("Mobile Number")
        if st.button("Login ➔"):
            u_name = check_user(l_phone)
            if u_name:
                st.session_state.u = {"n": u_name, "p": l_phone}
                st.session_state.auth = True; st.rerun()
            else: st.error("Not registered.")
    else:
        r_name = st.text_input("Full Name")
        r_phone = st.text_input("Mobile Number")
        if st.button("Register"):
            if r_name and len(r_phone) == 10:
                save_user(r_name, r_phone); st.session_state.u = {"n": r_name, "p": r_phone}
                st.session_state.auth = True; st.rerun()

# --- 6. MAIN CONTENT (All Old Features Included) ---
else:
    # Sidebar with All Old Features
    with st.sidebar:
        if os.path.exists(LOGO_PATH): st.image(LOGO_PATH, width=120)
        st.write(f"### Hello, {st.session_state.u['n']}")
        if st.button("🏠 Home"): st.session_state.pg = "Home"; st.session_state.step = 1; st.rerun()
        if st.button("🕒 History"): st.session_state.pg = "History"; st.rerun()
        if st.button("📞 Support"): st.session_state.pg = "Support"; st.rerun()
        if st.button("👤 Profile"): st.session_state.pg = "Profile"; st.rerun()
        if st.button("🚪 Logout"): st.session_state.auth = False; st.rerun()

    # --- Page Content ---
    if st.session_state.pg == "Home":
        if st.session_state.step == 1:
            st.header("Book a Ride")
            m = folium.Map(location=[19.9975, 73.7898], zoom_start=12)
            st_folium(m, width=700, height=250)
            src = st.text_input("📍 Pickup")
            dst = st.text_input("🏁 Drop")
            if st.button("Continue ➔"):
                if src and dst: 
                    st.session_state.route = {"s": src, "d": dst}
                    st.session_state.step = 2; st.rerun()
        
        elif st.session_state.step == 2:
            st.header("Booking Details")
            km = st.number_input("Distance (KM)", min_value=1.0, value=5.0)
            car = st.selectbox("Vehicle", list(CAR_MODELS.keys()))
            fare = km * CAR_MODELS[car]
            
            st.markdown(f"<div class='status-card'><h1>₹{fare}</h1><p>Estimated Fare</p></div>", unsafe_allow_html=True)
            
            pmode = st.radio("Payment:", ["Cash", "PhonePe / GPay"], horizontal=True)
            if pmode == "PhonePe / GPay":
                st.info(f"Pay to: {PAY_NO}")
                st.text_input("Copy Number:", value=PAY_NO)

            msg = (f"📦 *New Booking*\n👤 User: {st.session_state.u['n']}\n📞 No: {st.session_state.u['p']}\n📍 From: {st.session_state.route['s']}\n🏁 To: {st.session_state.route['d']}\n🚗 Car: {car}\n💰 Fare: ₹{fare}\n💳 Payment: {pmode}")
            whatsapp_link = f"https://wa.me/{MY_NO}?text={urllib.parse.quote(msg)}"
            
            if st.button("Confirm & Send WhatsApp ✅"):
                save_booking(st.session_state.u['p'], {"s": st.session_state.route['s'], "d": st.session_state.route['d'], "f": fare, "c": car, "pm": pmode})
                st.markdown(f'<meta http-equiv="refresh" content="0; url={whatsapp_link}">', unsafe_allow_html=True)

    elif st.session_state.pg == "History":
        st.header("Booking History")
        data = load_history(st.session_state.u['p'])
        if not data: st.info("No history.")
        for h in reversed(data):
            st.write(f"📍 {h['s']} ➔ {h['d']} | ₹{h['f']} | {h['pm']}")

    elif st.session_state.pg == "Support":
        st.header("Support")
        st.write(f"Contact us: {MY_NO}")
        st.markdown(f'<a href="https://wa.me/{MY_NO}">Chat on WhatsApp</a>', unsafe_allow_html=True)

    elif st.session_state.pg == "Profile":
        st.header("Profile")
        st.write(f"Name: {st.session_state.u['n']}")
        st.write(f"Phone: {st.session_state.u['p']}")

    # --- 7. BOTTOM NAVIGATION (Old Feature) ---
    st.markdown("---")
    nav = st.columns(5)
    if nav[0].button("🏠"): st.session_state.pg = "Home"; st.session_state.step = 1; st.rerun()
    if nav[1].button("🕒"): st.session_state.pg = "History"; st.rerun()
    if nav[2].button("📞"): st.session_state.pg = "Support"; st.rerun()
    if nav[3].button("👤"): st.session_state.pg = "Profile"; st.rerun()
    if nav[4].button("🚪"): st.session_state.auth = False; st.rerun()