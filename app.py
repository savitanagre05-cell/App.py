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

# --- 2. PREMIUM CSS ---
st.markdown("""
    <style>
    /* Main Background */
    .main { background-color: #f8f9fa; }
    
    /* Premium Card Style */
    .stApp { font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
    
    /* Custom Button */
    div.stButton > button:first-child {
        background: linear-gradient(to right, #000000, #434343);
        color: white;
        border-radius: 10px;
        border: none;
        height: 50px;
        width: 100%;
        font-weight: bold;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
    }
    
    /* Input Fields */
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #ddd;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #eee;
    }
    
    /* Payment Box */
    .pay-container {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #673ab7;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATABASE FUNCTIONS ---
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

# --- 5. AUTHENTICATION ---
if not st.session_state.auth:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if os.path.exists(LOGO_PATH): st.image(LOGO_PATH, use_container_width=True)
        st.markdown("<h2 style='text-align: center;'>Welcome to Balaji</h2>", unsafe_allow_html=True)
        
    choice = st.segmented_control("Action", ["Login", "Register"], default="Login")
    
    if choice == "Login":
        l_phone = st.text_input("Mobile Number", placeholder="9922xxxxxx")
        if st.button("Login ➔"):
            u_name = check_user(l_phone)
            if u_name:
                st.session_state.u = {"n": u_name, "p": l_phone}
                st.session_state.auth = True; st.rerun()
            else: st.error("Account not found. Please Register.")
    else:
        r_name = st.text_input("Your Full Name")
        r_phone = st.text_input("Mobile Number")
        if st.button("Create Account"):
            if r_name and len(r_phone) == 10:
                save_user(r_name, r_phone); st.session_state.u = {"n": r_name, "p": r_phone}
                st.session_state.auth = True; st.rerun()

# --- 6. MAIN CONTENT ---
else:
    # Sidebar Navigation
    with st.sidebar:
        if os.path.exists(LOGO_PATH): st.image(LOGO_PATH, width=150)
        st.markdown(f"### Hi, {st.session_state.u['n']}!")
        st.divider()
        if st.button("🏠 Home"): st.session_state.pg = "Home"; st.session_state.step = 1; st.rerun()
        if st.button("🕒 History"): st.session_state.pg = "History"; st.rerun()
        if st.button("📞 Support"): st.session_state.pg = "Support"; st.rerun()
        if st.button("👤 Profile"): st.session_state.pg = "Profile"; st.rerun()
        st.divider()
        if st.button("🚪 Logout"): st.session_state.auth = False; st.rerun()

    if st.session_state.pg == "Home":
        if st.session_state.step == 1:
            st.markdown("### 📍 Set Route")
            m = folium.Map(location=[19.9975, 73.7898], zoom_start=12)
            st_folium(m, width=700, height=300)
            
            src = st.text_input("Pickup Point", placeholder="e.g. Nashik Road")
            dst = st.text_input("Drop Point", placeholder="e.g. College Road")
            if st.button("Continue ➔"):
                if src and dst: 
                    st.session_state.route = {"s": src, "d": dst}
                    st.session_state.step = 2; st.rerun()
        
        elif st.session_state.step == 2:
            st.markdown("### 🚗 Choose Your Ride")
            km = st.number_input("Distance (KM)", min_value=1.0, value=5.0)
            car = st.selectbox("Vehicle Type", list(CAR_MODELS.keys()))
            fare = km * CAR_MODELS[car]
            
            st.markdown(f"""
                <div style='background: #000; color: white; padding: 20px; border-radius: 15px; text-align: center;'>
                    <p style='margin:0;'>Total Fare</p>
                    <h1 style='margin:0; color: #FFD700;'>₹{fare}</h1>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            pmode = st.radio("Payment Method", ["Cash", "PhonePe / GPay"], horizontal=True)
            
            if pmode == "PhonePe / GPay":
                st.markdown(f"""
                    <div class="pay-container">
                        <p style='margin:0; font-weight:bold;'>UPI Payment Number</p>
                        <h3 style='margin:0; color: #673ab7;'>{PAY_NO}</h3>
                    </div>
                """, unsafe_allow_html=True)
                st.text_input("Copy UPI Number:", value=PAY_NO)

            msg = (f"📦 *New Premium Booking*\n👤 User: {st.session_state.u['n']}\n📍 From: {st.session_state.route['s']}\n🏁 To: {st.session_state.route['d']}\n🚗 Car: {car}\n💰 Fare: ₹{fare}\n💳 Payment: {pmode}")
            whatsapp_link = f"https://wa.me/{MY_NO}?text={urllib.parse.quote(msg)}"
            
            if st.button("Confirm Booking ✅"):
                save_booking(st.session_state.u['p'], {"s": st.session_state.route['s'], "d": st.session_state.route['d'], "f": fare, "c": car, "pm": pmode})
                st.markdown(f'<meta http-equiv="refresh" content="0; url={whatsapp_link}">', unsafe_allow_html=True)

    elif st.session_state.pg == "History":
        st.header("Booking History")
        data = load_history(st.session_state.u['p'])
        if not data: st.info("No bookings found yet.")
        for h in reversed(data):
            with st.container():
                st.markdown(f"""
                <div style='border: 1px solid #ddd; padding: 15px; border-radius: 10px; margin-bottom: 10px;'>
                    <b>📍 From:</b> {h['s']} <br> <b>🏁 To:</b> {h['d']} <br> <b>💰 Fare:</b> ₹{h['f']}
                </div>
                """, unsafe_allow_html=True)

    elif st.session_state.pg == "Support":
        st.header("Need Help?")
        st.write("Our team is available 24/7.")
        st.markdown(f"### 📞 {MY_NO}")

    elif st.session_state.pg == "Profile":
        st.header("Your Profile")
        st.write(f"Name: **{st.session_state.u['n']}**")
        st.write(f"Phone: **{st.session_state.u['p']}**")