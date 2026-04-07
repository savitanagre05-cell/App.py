import streamlit as st
import random
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import streamlit_js_eval

# १. अ‍ॅप सेटिंग्स (Mobile Optimized)
st.set_page_config(page_title="Balaji Logistics", page_icon="🚕", layout="wide")

# २. युजरचे रिअल GPS लोकेशन मिळवणे
loc = streamlit_js_eval(key='get_location', component_width=0, function_name='getCurrentPosition')

# ३. स्टेट मॅनेजमेंट
if "lang" not in st.session_state: st.session_state.lang = "मराठी"
if "is_auth" not in st.session_state: st.session_state.is_auth = False
if "page" not in st.session_state: st.session_state.page = "🏠 Home"
if "auth_mode" not in st.session_state: st.session_state.auth_mode = "Login"
if "user_name" not in st.session_state: st.session_state.user_name = "Customer"
if "booking_status" not in st.session_state: st.session_state.booking_status = "Search"
if "otp" not in st.session_state: st.session_state.otp = random.randint(1000, 9999)

# ४. शब्दकोश (तुझा ओरिजिनल Dictionary)
texts = {
    "मराठी": {
        "login": "Login", "reg": "Register", "name": "पूर्ण नाव",
        "phone": "मोबाईल नंबर", "p_name": "उदा. अमित पाटील", "p_phone": "उदा. 9822xxxxxx",
        "from": "कुठून? (Pickup)", "to": "कुठे? (Drop)", "car": "गाडी निवडा", "km": "अंदाजित किमी", 
        "fare": "एकूण भाडे", "pay": "पेमेंट पद्धत", "book_btn": "Confirm Booking", "logout": "Logout"
    },
    "English": {
        "login": "Login", "reg": "Register", "name": "Full Name",
        "phone": "Mobile Number", "p_name": "e.g. Amit Patil", "p_phone": "e.g. 9822xxxxxx",
        "from": "From (Pickup)", "to": "To (Drop)", "car": "Select Car", "km": "Estimated KM", 
        "fare": "Total Fare", "pay": "Payment Mode", "book_btn": "Confirm Booking", "logout": "Logout"
    }
}

T = texts[st.session_state.lang]
MY_NUMBER = "9767981986"
MY_UPI_ID = "9767981986@ybl"

# ५. अल्ट्रा प्रीमियम CSS (Black & White Uber Theme)
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF !important; }
    .app-header { background-color: #000; color: #FFF !important; padding: 25px; text-align: center; font-size: 28px; font-weight: bold; border-radius: 0 0 25px 25px; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.2); }
    .stButton>button { width: 100%; background-color: #000 !important; color: #FFF !important; border-radius: 15px !important; height: 55px; font-weight: bold !important; border: none !important; }
    label, p, h1, h2, h3, span { color: #000 !important; font-weight: bold !important; }
    div[data-baseweb="input"] { border: 2px solid #000 !important; border-radius: 12px !important; background-color: #F9F9F9 !important; }
    .driver-card { background: white; border-radius: 20px; padding: 20px; box-shadow: 0 8px 30px rgba(0,0,0,0.15); margin-top: -50px; position: relative; z-index: 99; border: 1px solid #eee; }
    .otp-tag { background: #000; color: #fff; padding: 5px 12px; border-radius: 8px; font-weight: bold; font-size: 20px; }
    
    /* Fixed Bottom Navigation Style */
    .nav-container { position: fixed; bottom: 0; left: 0; width: 100%; background: white; display: flex; justify-content: space-around; padding: 10px 0; border-top: 1px solid #ddd; z-index: 1000; }
</style>
""", unsafe_allow_html=True)

# ६. ऑथेंटिकेशन (Login & Registration)
if not st.session_state.is_auth:
    st.markdown("<div class='app-header'>🚕 Balaji Logistics</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"🔑 {T['login']}"): st.session_state.auth_mode = "Login"; st.rerun()
    with col2:
        if st.button(f"📝 {T['reg']}"): st.session_state.auth_mode = "Register"; st.rerun()

    if st.session_state.auth_mode == "Login":
        l_p = st.text_input(T['phone'], placeholder=T['p_phone'], key="log_p")
        if st.button("🚀 GO"):
            if len(l_p) == 10: st.session_state.is_auth = True; st.rerun()
            else: st.error("१० अंकी नंबर टाका.")
    else:
        r_n = st.text_input(T['name'], placeholder=T['p_name'], key="reg_n")
        r_p = st.text_input(T['phone'], placeholder=T['p_phone'], key="reg_p")
        if st.button("✅ CREATE ACCOUNT"):
            if r_n and len(r_p) == 10:
                st.session_state.user_name = r_n
                st.session_state.is_auth = True; st.rerun()
    st.stop()

# ७. मुख्य अ‍ॅप (Header)
st.markdown("<div class='app-header'>Balaji Logistics</div>", unsafe_allow_html=True)

# --- LIVE RIDE CONFIRMED VIEW (Anil Nagre & MH01BY3960) ---
if st.session_state.booking_status == "Confirmed":
    st.balloons()
    u_lat = loc['coords']['latitude'] if loc else 20.0022
    u_lon = loc['coords']['longitude'] if loc else 73.7898
    
    m = folium.Map(location=[u_lat, u_lon], zoom_start=16, zoom_control=False)
    folium.CircleMarker([u_lat, u_lon], radius=8, color='blue', fill=True).add_to(m)
    folium.Marker([u_lat + 0.001, u_lon + 0.001], icon=folium.Icon(color='black', icon='car', prefix='fa')).add_to(m)
    st_folium(m, width="100%", height=350)
    
    st.markdown(f"""
    <div class="driver-card">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <h2 style="margin:0;">Anil Nagre</h2>
                <p style="color:#E67E22; margin:0; font-size:18px;"><b>MH01BY3960</b></p>
                <p style="color:gray; margin:0; font-size:14px;">White Swift Dzire • ⭐ 4.9</p>
            </div>
            <div style="text-align:center;"><small style="color:gray;">PIN</small><div class="otp-tag">{st.session_state.otp}</div></div>
        </div>
        <div style="margin-top:15px; background:#e8f5e9; padding:10px; border-radius:10px; text-align:center; color:#2e7d32; font-weight:bold;">🚕 ड्रायव्हर पिकअपसाठी येत आहे!</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("❌ Cancel Ride"): st.session_state.booking_status = "Search"; st.rerun()
    st.stop()

# --- नेव्हिगेशन पेजेस ---
if st.session_state.page == "🏠 Home":
    st.markdown(f"### नमस्कार, {st.session_state.user_name}! 👋")
    st.image("https://images.unsplash.com/photo-1559297434-2d8a1e02a01d?auto=format&fit=crop&w=800")
    if st.button("Book Ride Now ➔"): st.session_state.page = "🚕 Book"; st.rerun()

elif st.session_state.page == "🚕 Book":
    p_up = st.text_input(T['from'], value="Current Location" if loc else "")
    d_off = st.text_input(T['to'])
    car = st.selectbox(T['car'], ["🚗 Mini (₹11/km)", "🚖 Sedan (₹14/km)", "🚐 SUV (₹17/km)"])
    km = st.number_input(T['km'], min_value=1, value=10)
    total = km * (11 if "Mini" in car else (14 if "Sedan" in car else 17))
    st.info(f"💰 {T['fare']}: ₹{total}")
    
    pay = st.radio(T['pay'], ["Cash", "PhonePe"], horizontal=True)
    if pay == "PhonePe":
        st.markdown(f"#### [💸 Pay ₹{total} via PhonePe](upi://pay?pa={MY_UPI_ID}&pn=BalajiLogistics&am={total}&cu=INR)")

    if st.button(T['book_btn']):
        msg = f"🚩 *New Booking*\nDriver: Anil Nagre\nVehicle: MH01BY3960\nFrom: {p_up}\nTo: {d_off}\nTotal: ₹{total}\nOTP: {st.session_state.otp}"
        wa_url = f"https://wa.me/91{MY_NUMBER}?text={msg.replace(' ', '%20')}"
        st.markdown(f'<meta http-equiv="refresh" content="0;URL={wa_url}">', unsafe_allow_html=True)
        st.session_state.booking_status = "Confirmed"; st.rerun()

elif st.session_state.page == "⚙️ Settings":
    new_lang = st.selectbox("Language", ["मराठी", "English"], index=0 if st.session_state.lang=="मराठी" else 1)
    if new_lang != st.session_state.lang: st.session_state.lang = new_lang; st.rerun()
    if st.button(T['logout']): st.session_state.is_auth = False; st.rerun()

# ८. बॉटम नेव्हिगेशन बार (Final Mixed Version)
st.write("<br><br><br><br>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🏠 Home"): st.session_state.page = "🏠 Home"; st.rerun()
with c2:
    if st.button("🚕 Ride"): st.session_state.page = "🚕 Book"; st.rerun()
with c3:
    if st.button("👤 Account"): st.session_state.page = "⚙️ Settings"; st.rerun()
