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

# --- 2. PREMIUM LOOK (Look परत आणला) ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .brand-header {
        background: linear-gradient(90deg, #004085 0%, #0056b3 100%);
        color: white; padding: 20px; border-radius: 12px;
        text-align: center; margin-bottom: 20px;
    }
    .fare-card {
        background-color: #ffffff; padding: 20px; border-radius: 12px;
        text-align: center; margin-bottom: 15px; border-top: 5px solid #ff8c00;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
    }
    .fare-amount { color: #ff8c00; font-size: 35px; font-weight: bold; }
    /* WhatsApp Button Style */
    .wa-btn {
        background-color: #25D366; color: white !important;
        padding: 12px; border-radius: 8px; text-decoration: none;
        display: block; text-align: center; font-weight: bold; margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATABASE (No Change) ---
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

# --- 5. LOGIN / REGISTER (Original) ---
if not st.session_state.auth:
    st.markdown("<div class='brand-header'><h1>🚛 Balaji Logistics</h1></div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Login", "Register"])
    with tab1:
        l_phone = st.text_input("Mobile Number", key="lp")
        if st.button("Login ➔"):
            u_name = check_user(l_phone)
            if u_name:
                st.session_state.u = {"n": u_name, "p": l_phone}
                st.session_state.auth = True; st.rerun()
            else: st.error("User not found.")
    with tab2:
        r_name = st.text_input("Full Name")
        r_phone = st.text_input("Mobile Number", key="rp")
        if st.button("Create Account"):
            if r_name and len(r_phone) == 10:
                save_user(r_name, r_phone); st.session_state.u = {"n": r_name, "p": r_phone}
                st.session_state.auth = True; st.rerun()

# --- 6. MAIN CONTENT ---
else:
    with st.sidebar:
        st.write(f"### Welcome, {st.session_state.u['n']}")
        if st.button("🏠 Home"): st.session_state.pg = "Home"; st.session_state.step = 1; st.rerun()
        if st.button("🕒 History"): st.session_state.pg = "History"; st.rerun()
        if st.button("🚪 Logout"): st.session_state.auth = False; st.rerun()

    if st.session_state.pg == "Home":
        if st.session_state.step == 1:
            st.header("Plan Your Trip")
            m = folium.Map(location=[19.9975, 73.7898], zoom_start=12)
            st_folium(m, width=700, height=250)
            src = st.text_input("Pickup")
            dst = st.text_input("Drop")
            if st.button("Next ➔"):
                if src and dst: st.session_state.route = {"s": src, "d": dst}; st.session_state.step = 2; st.rerun()
        
        elif st.session_state.step == 2:
            st.header("Confirm Ride")
            km = st.number_input("Distance (KM)", value=5.0)
            car = st.selectbox("Vehicle", list(CAR_MODELS.keys()))
            fare = km * CAR_MODELS[car]
            
            st.markdown(f"<div class='fare-card'><p class='fare-amount'>₹{fare}</p></div>", unsafe_allow_html=True)
            
            pmode = st.radio("Payment Method:", ["Cash", "PhonePe / GPay"])
            if pmode == "PhonePe / GPay":
                st.info(f"Pay to: {PAY_NO}")
                st.text_input("Copy Number:", value=PAY_NO)

            msg = (f"📦 *New Booking*\n👤 {st.session_state.u['n']}\n📍 {st.session_state.route['s']} to {st.session_state.route['d']}\n🚗 {car}\n💰 ₹{fare}\n💳 {pmode}")
            wa_link = f"https://wa.me/{MY_NO}?text={urllib.parse.quote(msg)}"
            
            if st.button("Confirm & Save Details 📁"):
                save_booking(st.session_state.u['p'], {"s": st.session_state.route['s'], "d": st.session_state.route['d'], "f": fare, "c": car, "pm": pmode})
                st.success("Details Saved!")

            # Direct WhatsApp Link (Look maintain राहून fast काम करेल)
            st.markdown(f'<a href="{wa_link}" target="_blank" class="wa-btn">Send to WhatsApp ✅</a>', unsafe_allow_html=True)

    elif st.session_state.pg == "History":
        st.header("History")
        data = load_history(st.session_state.u['p'])
        for h in reversed(data): st.info(f"📍 {h['s']} ➔ {h['d']} | ₹{h['f']}")

    # Bottom Nav
    st.markdown("---")
    c = st.columns(5)
    if c[0].button("🏠"): st.session_state.pg = "Home"; st.session_state.step = 1; st.rerun()
    if c[1].button("🕒"): st.session_state.pg = "History"; st.rerun()
    if c[4].button("🚪"): st.session_state.auth = False; st.rerun()