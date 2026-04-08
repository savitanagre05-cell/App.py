import streamlit as st
import urllib.parse, folium, os, pandas as pd
from streamlit_folium import st_folium

# 1. Main Configuration
st.set_page_config(page_title="Balaji Logistics", layout="centered", page_icon="📦")
MY_NO = "9767981986"
USER_DB = "users_list.csv" # Users chi mahiti
HIST_DB = "booking_history.csv" # Bookings chi mahiti

CAR_MODELS = {"Balaji Go 🚗": 13, "Balaji Sedan 🚙": 17, "Balaji SUV 🚐": 22}

# --- 2. Database Functions ---
def save_user(name, phone):
    df = pd.DataFrame([{"name": name, "phone": phone}])
    if not os.path.isfile(USER_DB):
        df.to_csv(USER_DB, index=False)
    else:
        df.to_csv(USER_DB, mode='a', header=False, index=False)

def check_user(phone):
    if os.path.isfile(USER_DB):
        df = pd.read_csv(USER_DB)
        user = df[df['phone'].astype(str) == str(phone)]
        return user.iloc[0]['name'] if not user.empty else None
    return None

def save_booking(phone, data):
    data['phone'] = phone
    df = pd.DataFrame([data])
    if not os.path.isfile(HIST_DB):
        df.to_csv(HIST_DB, index=False)
    else:
        df.to_csv(HIST_DB, mode='a', header=False, index=False)

def load_history(phone):
    if os.path.isfile(HIST_DB):
        df = pd.read_csv(HIST_DB)
        return df[df['phone'].astype(str) == str(phone)].to_dict('records')
    return []

# --- 3. Language Selection ---
T = {
    "English": {"home": "Home", "act": "History", "supp": "Support", "logout": "Logout", "reg": "Register", "log": "Login"},
    "Marathi": {"home": "होम", "act": "हिस्ट्री", "supp": "सपोर्ट", "logout": "लॉगआउट", "reg": "नोंदणी", "log": "लॉगिन"}
}

if "auth" not in st.session_state: st.session_state.auth = False
if "pg" not in st.session_state: st.session_state.pg = "Home"
if "step" not in st.session_state: st.session_state.step = 1

# --- 4. Styling ---
st.markdown("""
<style>
    .stButton>button {width: 100%; border-radius: 12px; height: 50px; font-weight: bold; background-color: #000; color: #fff;}
    .nav-btn {font-size: 12px !important;}
</style>
""", unsafe_allow_html=True)

# --- 5. AUTHENTICATION PAGE (Login/Register) ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center;'>BALAJI LOGISTICS 📦</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        l_phone = st.text_input("Mobile Number", key="l_phone", max_chars=10)
        if st.button("Login ➔"):
            user_name = check_user(l_phone)
            if user_name:
                st.session_state.u = {"n": user_name, "p": l_phone}
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Number not found. Please Register first.")
                
    with tab2:
        r_name = st.text_input("Full Name")
        r_phone = st.text_input("Mobile Number", key="r_phone", max_chars=10)
        if st.button("Register & Start"):
            if r_name and len(r_phone) == 10:
                if check_user(r_phone):
                    st.warning("Number already registered. Please Login.")
                else:
                    save_user(r_name, r_phone)
                    st.session_state.u = {"n": r_name, "p": r_phone}
                    st.session_state.auth = True
                    st.rerun()
            else:
                st.error("Please enter correct details.")

# --- 6. MAIN APP CONTENT ---
else:
    L = T["Marathi"] # Default to Marathi or add language toggle back
    
    if st.session_state.pg == "Home":
        st.markdown(f"### Welcome, {st.session_state.u['n']}! 👋")
        if st.session_state.step == 1:
            src = st.text_input("📍 Pick-up Point")
            dst = st.text_input("🏁 Drop Point")
            if st.button("Next ➔"):
                if src and dst:
                    st.session_state.route = {"s": src, "d": dst}
                    st.session_state.step = 2; st.rerun()
        else:
            km = st.number_input("KM", min_value=1.0, value=5.0)
            car = st.selectbox("Select Car", list(CAR_MODELS.keys()))
            fare = km * CAR_MODELS[car]
            st.markdown(f"## Fare: ₹{fare}")
            if st.button("Confirm Booking ✅"):
                save_booking(st.session_state.u['p'], {"s": st.session_state.route['s'], "d": st.session_state.route['d'], "f": fare, "c": car})
                st.success("Booking Saved!")
                st.session_state.step = 1; st.rerun()

    elif st.session_state.pg == "History":
        st.header("Booking History")
        data = load_history(st.session_state.u['p'])
        if not data: st.write("No history.")
        for h in reversed(data):
            st.info(f"📍 {h['s']} ➔ {h['d']} | ₹{h['f']} ({h['c']})")

    elif st.session_state.pg == "Support":
        st.header("Support")
        st.write(f"Call: {MY_NO}")
        st.markdown(f'<a href="https://wa.me/{MY_NO}"><button style="width:100%; background:#25D366; color:white; border:none; padding:10px; border-radius:10px;">WhatsApp Support</button></a>', unsafe_allow_html=True)

    # --- 7. HORIZONTAL BOTTOM NAVIGATION ---
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    nav = st.columns(4)
    
    if nav[0].button(f"🏠\nHome"):
        st.session_state.pg = "Home"; st.session_state.step = 1; st.rerun()
    if nav[1].button(f"🕒\nHistory"):
        st.session_state.pg = "History"; st.rerun()
    if nav[2].button(f"📞\nSupport"):
        st.session_state.pg = "Support"; st.rerun()
    if nav[3].button(f"🚪\nLogout"):
        st.session_state.auth = False; st.rerun()