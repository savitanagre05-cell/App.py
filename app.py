import streamlit as st
import urllib.parse, folium, os, pandas as pd
from streamlit_folium import st_folium

# 1. Main Configuration
st.set_page_config(page_title="Balaji Logistics", layout="centered", page_icon="📦")
MY_NO = "9767981986" # Booking Receive Number
PAY_NO = "9309146504" # PhonePe/UPI Number
USER_DB = "users_list.csv" 
HIST_DB = "booking_history.csv" 

CAR_MODELS = {"Balaji Go 🚗": 13, "Balaji Sedan 🚙": 17, "Balaji SUV 🚐": 22}

# --- 2. Database Functions ---
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

# --- 3. Styling (App Look) ---
st.markdown(f"""
<style>
    .stButton>button {{width: 100%; border-radius: 12px; height: 50px; font-weight: bold; background-color: #000; color: #fff;}}
    .wa-button {{
        display: inline-block; padding: 15px 25px; font-size: 18px; cursor: pointer; text-align: center;
        text-decoration: none; outline: none; color: #fff !important; background-color: #25D366;
        border: none; border-radius: 15px; width: 100%; font-weight: bold; margin-top: 10px;
    }}
    .pay-button {{
        display: inline-block; padding: 15px 25px; font-size: 18px; cursor: pointer; text-align: center;
        text-decoration: none; outline: none; color: #fff !important; background-color: #673ab7;
        border: none; border-radius: 15px; width: 100%; font-weight: bold; margin-top: 10px;
    }}
    .summary-card {{ background: #f8f9fa; padding: 20px; border-radius: 15px; border: 1px solid #ddd; line-height: 1.6; }}
</style>
""", unsafe_allow_html=True)

# --- 4. AUTHENTICATION (Login/Register) ---
if "auth" not in st.session_state: st.session_state.auth = False
if "pg" not in st.session_state: st.session_state.pg = "Home"
if "step" not in st.session_state: st.session_state.step = 1

if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center;'>BALAJI LOGISTICS 📦</h1>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["लॉगिन", "नोंदणी"])
    with tab1:
        l_phone = st.text_input("मोबाईल नंबर", key="l_phone", max_chars=10)
        if st.button("सुरू करा ➔"):
            user_name = check_user(l_phone)
            if user_name:
                st.session_state.u = {"n": user_name, "p": l_phone}
                st.session_state.auth = True; st.rerun()
            else: st.error("नंबर सापडला नाही. आधी नोंदणी करा.")
    with tab2:
        r_name = st.text_input("पूर्ण नाव")
        r_phone = st.text_input("मोबाईल नंबर", key="r_phone", max_chars=10)
        if st.button("रजिस्टर करा"):
            if r_name and len(r_phone) == 10:
                save_user(r_name, r_phone); st.session_state.u = {"n": r_name, "p": r_phone}
                st.session_state.auth = True; st.rerun()
            else: st.error("योग्य माहिती भरा.")

# --- 5. MAIN APP PAGES ---
else:
    if st.session_state.pg == "Home":
        if st.session_state.step == 1:
            st.markdown(f"### नमस्कार, {st.session_state.u['n']}! 👋")
            src = st.text_input("📍 पिकअप पॉईंट")
            dst = st.text_input("🏁 ड्रॉप पॉईंट")
            if st.button("पुढील स्टेप ➔"):
                if src and dst: st.session_state.route = {"s": src, "d": dst}; st.session_state.step = 2; st.rerun()
        
        elif st.session_state.step == 2:
            km = st.number_input("किमी (KM)", min_value=1.0, value=5.0)
            car = st.selectbox("गाडी निवडा", list(CAR_MODELS.keys()))
            fare = km * CAR_MODELS[car]
            st.markdown(f"## भाडे: ₹{fare}")
            pay_mode = st.radio("पेमेंट पद्धत निवडा:", ["Cash (रोख)", "PhonePe / UPI"], horizontal=True)
            
            if st.button("बुकिंग कन्फर्म करा ✅"):
                booking_data = {"s": st.session_state.route['s'], "d": st.session_state.route['d'], "f": fare, "c": car, "pm": pay_mode}
                save_booking(st.session_state.u['p'], booking_data)
                st.session_state.last_booking = booking_data
                st.session_state.step = 3; st.rerun()
        
        elif st.session_state.step == 3:
            b = st.session_state.last_booking
            st.success("✅ बुकिंग यशस्वी झाले!")
            
            st.markdown(f"""<div class="summary-card">
                <h4>📋 बुकिंग समरी</h4>
                <p><b>नाव:</b> {st.session_state.u['n']} | <b>नंबर:</b> {st.session_state.u['p']}</p>
                <p><b>📍 पिकअप:</b> {b['s']} | <b>🏁 ड्रॉप:</b> {b['d']}</p>
                <p><b>🚗 गाडी:</b> {b['c']} | <b>💰 भाडे:</b> ₹{b['f']}</p>
                <p><b>💳 पेमेंट मोड:</b> {b['pm']}</p>
            </div>""", unsafe_allow_html=True)
            
            if b['pm'] == "PhonePe / UPI":
                upi_url = f"upi://pay?pa={PAY_NO}@ybl&pn=Balaji%20Logistics&am={b['f']}&cu=INR"
                st.markdown(f'<a href="{upi_url}" class="pay-button">PhonePe ने ₹{b["f"]} पे करा 📲</a>', unsafe_allow_html=True)
                st.info("💡 पेमेंट झाल्यावर 'Back' दाबून येथे या आणि WhatsApp मेसेज पाठवा.")
            
            msg = (f"📦 *नवीन बुकिंग*\n👤 नाव: {st.session_state.u['n']}\n📞 नंबर: {st.session_state.u['p']}\n📍 पिकअप: {b['s']}\n🏁 ड्रॉप: {b['d']}\n💰 भाडे: ₹{b['f']}\n💳 पेमेंट: {b['pm']}")
            encoded_msg = urllib.parse.quote(msg)
            st.markdown(f'<a href="https://wa.me/{MY_NO}?text={encoded_msg}" target="_blank" class="wa-button">WhatsApp वर डिटेल्स पाठवा 💬</a>', unsafe_allow_html=True)
            if st.button("नवीन बुकिंग करा"): st.session_state.step = 1; st.rerun()

    elif st.session_state.pg == "History":
        st.header("🕒 तुमची हिस्ट्री")
        data = load_history(st.session_state.u['p'])
        if not data: st.info("अजून एकही बुकिंग नाही.")
        for h in reversed(data):
            st.info(f"📍 {h['s']} ➔ {h['d']} | ₹{h['f']} | {h['pm']}")

    elif st.session_state.pg == "Support":
        st.header("📞 सपोर्ट")
        st.write(f"संपर्क: {MY_NO}")
        st.markdown(f'<a href="https://wa.me/{MY_NO}" class="wa-button">WhatsApp Support</a>', unsafe_allow_html=True)

    elif st.session_state.pg == "Profile":
        st.header("👤 माझे प्रोफाइल")
        st.write(f"नाव: **{st.session_state.u['n']}**")
        st.write(f"मोबाईल: **{st.session_state.u['p']}**")
        if st.button("लॉगआउट 🚪"): st.session_state.auth = False; st.rerun()

    # --- 6. BOTTOM NAVIGATION (5-BUTTONS) ---
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    nav = st.columns(5)
    if nav[0].button("🏠\nहोम"): st.session_state.pg = "Home"; st.session_state.step = 1; st.rerun()
    if nav[1].button("🕒\nहिस्ट्री"): st.session_state.pg = "History"; st.rerun()
    if nav[2].button("📞\nसपोर्ट"): st.session_state.pg = "Support"; st.rerun()
    if nav[3].button("👤\nप्रोफाइल"): st.session_state.pg = "Profile"; st.rerun()
    if nav[4].button("🚪\nबाहेर"): st.session_state.auth = False; st.rerun()