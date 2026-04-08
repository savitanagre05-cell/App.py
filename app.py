import streamlit as st
import urllib.parse, os, pandas as pd
import folium
from streamlit_folium import st_folium

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Balaji Logistics", layout="centered", page_icon="📦")
MY_NO = "9767981986" # Booking Receive Number
PAY_NO = "9309146504" # Payment Number
USER_DB = "users_list.csv" 
HIST_DB = "booking_history.csv" 

# Car Options & Rates
CAR_MODELS = {"Balaji Go 🚗": 13, "Balaji Sedan 🚙": 17, "Balaji SUV 🚐": 22}

# --- 2. DATABASE FUNCTIONS ---
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

# --- 3. STYLING ---
st.markdown(f"""
<style>
    .stButton>button {{width: 100%; border-radius: 12px; height: 50px; font-weight: bold; background-color: #000; color: #fff;}}
    .wa-button {{
        display: inline-block; padding: 15px 25px; font-size: 18px; cursor: pointer; text-align: center;
        text-decoration: none; outline: none; color: #fff !important; background-color: #25D366;
        border: none; border-radius: 15px; width: 100%; font-weight: bold; margin-top: 10px;
    }}
    .pay-box {{
        background: #f0eaff; padding: 20px; border-radius: 15px; border: 2px solid #673ab7; text-align: center; margin-bottom: 15px;
    }}
    .summary-card {{ background: #f8f9fa; padding: 20px; border-radius: 15px; border: 1px solid #ddd; line-height: 1.6; margin-bottom: 15px; }}
</style>
""", unsafe_allow_html=True)

# --- 4. SESSION STATE ---
if "auth" not in st.session_state: st.session_state.auth = False
if "pg" not in st.session_state: st.session_state.pg = "Home"
if "step" not in st.session_state: st.session_state.step = 1

# --- 5. AUTHENTICATION ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center;'>BALAJI LOGISTICS 📦</h1>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["लॉगिन", "नोंदणी"])
    with tab1:
        l_phone = st.text_input("मोबाईल नंबर", key="l_phone", max_chars=10)
        if st.button("सुरू करा ➔"):
            u_name = check_user(l_phone)
            if u_name:
                st.session_state.u = {"n": u_name, "p": l_phone}
                st.session_state.auth = True; st.rerun()
            else: st.error("नंबर सापडला नाही. आधी नोंदणी करा.")
    with tab2:
        r_name = st.text_input("पूर्ण नाव")
        r_phone = st.text_input("मोबाईल नंबर", key="r_phone", max_chars=10)
        if st.button("रजिस्टर करा"):
            if r_name and len(r_phone) == 10:
                save_user(r_name, r_phone); st.session_state.u = {"n": r_name, "p": r_phone}
                st.session_state.auth = True; st.rerun()
            else: st.error("सर्व माहिती अचूक भरा.")

# --- 6. MAIN CONTENT ---
else:
    if st.session_state.pg == "Home":
        if st.session_state.step == 1:
            st.markdown(f"### नमस्कार, {st.session_state.u['n']}! 👋")
            # Map
            m = folium.Map(location=[19.9975, 73.7898], zoom_start=12)
            st_folium(m, width=700, height=250)
            src = st.text_input("📍 पिकअप पॉईंट")
            dst = st.text_input("🏁 ड्रॉप पॉईंट")
            if st.button("पुढील स्टेप ➔"):
                if src and dst: 
                    st.session_state.route = {"s": src, "d": dst}
                    st.session_state.step = 2; st.rerun()
        
        elif st.session_state.step == 2:
            st.markdown("### 🚗 गाडी आणि अंतर निवडा")
            km = st.number_input("प्रवासाचे अंतर (KM)", min_value=1.0, value=5.0)
            car = st.selectbox("तुमची गाडी निवडा", list(CAR_MODELS.keys()))
            fare = km * CAR_MODELS[car]
            st.markdown(f"## एकूण भाडे: ₹{fare}")
            pmode = st.radio("पेमेंट कसे करणार?", ["Cash (रोख)", "PhonePe / GPay"], horizontal=True)
            if st.button("बुकिंग कन्फर्म करा ✅"):
                bdata = {"s": st.session_state.route['s'], "d": st.session_state.route['d'], "f": fare, "c": car, "pm": pmode}
                save_booking(st.session_state.u['p'], bdata)
                st.session_state.last_b = bdata
                st.session_state.step = 3; st.rerun()
        
        elif st.session_state.step == 3:
            lb = st.session_state.last_b
            st.success("✅ बुकिंग यशस्वी झाले!")
            st.markdown(f"""<div class="summary-card">
                <h4>📋 बुकिंग तपशील</h4>
                <p><b>ग्राहक:</b> {st.session_state.u['n']} | <b>नंबर:</b> {st.session_state.u['p']}</p>
                <hr>
                <p><b>📍 पिकअप:</b> {lb['s']} | <b>🏁 ड्रॉप:</b> {lb['d']}</p>
                <p><b>🚗 गाडी:</b> {lb['c']} | <b>💰 भाडे:</b> ₹{lb['f']}</p>
                <p><b>💳 पेमेंट:</b> {lb['pm']}</p>
            </div>""", unsafe_allow_html=True)
            
            if lb['pm'] == "PhonePe / GPay":
                st.markdown(f"""<div class="pay-box">
                    <h3 style="color: #673ab7;">📲 पेमेंट नंबर</h3>
                    <h2 style="letter-spacing: 2px;">{PAY_NO}</h2>
                    <p>हा नंबर कॉपी करा आणि पेमेंट ॲपमध्ये ₹{lb['f']} पाठवा.</p>
                </div>""", unsafe_allow_html=True)
                st.text_input("कॉपी करण्यासाठी नंबर:", value=PAY_NO)
            
            msg = (f"📦 *नवीन बुकिंग - BALAJI*\n👤 नाव: {st.session_state.u['n']}\n📞 नंबर: {st.session_state.u['p']}\n📍 पिकअप: {lb['s']}\n🏁 ड्रॉप: {lb['d']}\n🚗 गाडी: {lb['c']}\n💰 भाडे: ₹{lb['f']}\n💳 पेमेंट: {lb['pm']}")
            st.markdown(f'<a href="https://wa.me/{MY_NO}?text={urllib.parse.quote(msg)}" target="_blank" class="wa-button">WhatsApp वर तपशील पाठवा 💬</a>', unsafe_allow_html=True)
            if st.button("नवीन बुकिंग करा"): st.session_state.step = 1; st.rerun()

    elif st.session_state.pg == "History":
        st.header("🕒 हिस्ट्री")
        hist = load_history(st.session_state.u['p'])
        if not hist: st.info("हिस्ट्री रिकामी आहे.")
        for h in reversed(hist): st.info(f"📍 {h['s']} ➔ {h['d']} | ₹{h['f']} | {h['pm']}")

    elif st.session_state.pg == "Support":
        st.header("📞 सपोर्ट")
        st.write(f"संपर्क: {MY_NO}")
        st.markdown(f'<a href="https://wa.me/{MY_NO}" class="wa-button">WhatsApp Support</a>', unsafe_allow_html=True)

    elif st.session_state.pg == "Profile":
        st.header("👤 प्रोफाइल")
        st.write(f"नाव: **{st.session_state.u['n']}**")
        st.write(f"मोबाईल: **{st.session_state.u['p']}**")
        if st.button("लॉगआउट 🚪"): st.session_state.auth = False; st.rerun()

    # --- 7. NAVIGATION BAR ---
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    nav = st.columns(5)
    if nav[0].button("🏠\nहोम"): st.session_state.pg = "Home"; st.session_state.step = 1; st.rerun()
    if nav[1].button("🕒\nहिस्ट्री"): st.session_state.pg = "History"; st.rerun()
    if nav[2].button("📞\nसपोर्ट"): st.session_state.pg = "Support"; st.rerun()
    if nav[3].button("👤\nप्रोफाइल"): st.session_state.pg = "Profile"; st.rerun()
    if nav[4].button("🚪\nबाहेर"): st.session_state.auth = False; st.rerun()