import streamlit as st
import pandas as pd

# १. अ‍ॅप सेटिंग्स
st.set_page_config(page_title="Balaji Logistics Pro", page_icon="🚕", layout="wide")

# २. मास्टर CSS (Professional Mobile App UI)
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; }
    .app-header {
        background-color: black;
        color: white;
        padding: 15px;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        border-radius: 0 0 20px 20px;
        margin-bottom: 10px;
    }
    .app-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        margin-bottom: 20px;
        border: 1px solid #eee;
    }
    .stButton>button {
        width: 100%;
        background-color: black;
        color: white;
        border-radius: 12px;
        height: 55px;
        font-size: 18px;
        font-weight: bold;
        border: none;
    }
    .profile-banner {
        background: linear-gradient(135deg, #000, #444);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

MY_NUMBER = "9767981986"

# ३. स्टेट मॅनेजमेंट
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"

# ४. लॉगिन स्क्रीन
if not st.session_state.is_logged_in:
    st.markdown("<div class='app-header'>🚕 Balaji Logistics</div>", unsafe_allow_html=True)
    st.markdown("<div class='app-card'>", unsafe_allow_html=True)
    st.subheader("नवीन खाते उघडा")
    name = st.text_input("तुमचे पूर्ण नाव")
    phone = st.text_input("मोबाईल नंबर", max_chars=10)
    
    if st.button("Register & Start"):
        if name and len(phone) == 10:
            st.session_state.user_name = name
            st.session_state.user_phone = phone
            st.session_state.is_logged_in = True
            
            reg_msg = f"👤 *NEW USER REGISTERED*\n\nनाम: {name}\nनंबर: {phone}"
            url = f"https://wa.me/91{MY_NUMBER}?text={reg_msg.replace(' ', '%20')}"
            st.success(f"अभिनंदन {name}!")
            st.markdown(f"**[👉 व्हॉट्सॲपवर तुमची माहिती पाठवा]({url})**")
        else:
            st.error("कृपया नाव आणि योग्य नंबर टाका.")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ५. मुख्य अ‍ॅप
st.markdown("<div class='app-header'>Balaji Logistics</div>", unsafe_allow_html=True)

if st.session_state.page == "🏠 Home":
    st.markdown(f"<div class='profile-banner'><h3>नमस्कार, {st.session_state.user_name}! 👋</h3></div>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1559297434-2d8a1e02a01d?auto=format&fit=crop&w=800", use_container_width=True)
    if st.button("आत्ता राईड बुक करा ➔"):
        st.session_state.page = "🚕 Book"
        st.rerun()

elif st.session_state.page == "🚕 Book":
    st.markdown("<div class='app-card'>", unsafe_allow_html=True)
    st.subheader("📍 राईड तपशील")
    trip = st.radio("ट्रिप प्रकार:", ["One Way", "Round Trip"], horizontal=True)
    p_up = st.text_input("पिकअप ठिकाण")
    d_off = st.text_input("ड्रॉप ठिकाण")
    car = st.selectbox("गाडी निवडा", ["🚗 Mini (₹11/km)", "🚖 Sedan (₹14/km)", "🚐 SUV (₹17/km)"])
    km = st.number_input("अंदाजित किमी", min_value=1, value=50)
    rate = 11 if "Mini" in car else (14 if "Sedan" in car else 17)
    total = km * rate * (2 if trip == "Round Trip" else 1)
    st.markdown(f"<h2 style='color:green; text-align:center;'>भाडे: ₹{total}</h2>", unsafe_allow_html=True)
    if st.button("Confirm Booking"):
        msg = f"🚩 *NEW BOOKING*\n👤 ग्राहक: {st.session_state.user_name}\n📞 नंबर: {st.session_state.user_phone}\n🛣️ ट्रिप: {trip}\n📍 पिकअप: {p_up}\n🏁 ड्रॉप: {d_off}\n🚗 गाडी: {car}\n💰 एकूण: ₹{total}"
        st.markdown(f"[👉 व्हॉट्सॲपवर बुकिंग पाठवा](https://wa.me/91{MY_NUMBER}?text={msg.replace(' ', '%20').replace('\n', '%0A')})")
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "👤 Profile":
    st.markdown("<div class='app-card' style='text-align: center;'>", unsafe_allow_html=True)
    st.markdown(f"<h2>{st.session_state.user_name[0].upper()}</h2>", unsafe_allow_html=True)
    st.subheader(st.session_state.user_name)
    st.write(f"📞 {st.session_state.user_phone}")
    if st.button("Logout करा"):
        st.session_state.is_logged_in = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ६. बॉटम नेव्हिगेशन
st.write("<br><br><br>", unsafe_allow_html=True)
nav1, nav2, nav3 = st.columns(3)
with nav1:
    if st.button("🏠\nHome"): st.session_state.page = "🏠 Home"; st.rerun()
with nav2:
    if st.button("🚕\nBook"): st.session_state.page = "🚕 Book"; st.rerun()
with nav3:
    if st.button("👤\nProfile"): st.session_state.page = "👤 Profile"; st.rerun()
