import streamlit as st
import pandas as pd
import os
import urllib.parse
from datetime import datetime

# १. ॲप कॉन्फिगरेशन आणि नवीन प्रीमियम थीम
st.set_page_config(page_title="Balaji Logistics & Tours", layout="centered")

st.markdown("""
    <style>
    /* मुख्य बॅकग्राउंड */
    .stApp {
        background: linear-gradient(135deg, #00416A 0%, #E4E5E6 100%) !important;
    }
    
    /* प्रीमियम कार्ड डिझाइन */
    .main-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
        margin-bottom: 25px;
        color: #333;
    }

    /* कस्टम लोगो/हेडर */
    .app-header {
        background: #00416A;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: #FFD700; /* Gold Color */
        margin-bottom: 30px;
        border-bottom: 4px solid #FFD700;
    }

    /* बटण स्टाईल */
    .stButton>button {
        background: linear-gradient(to right, #00416A, #E4E5E6) !important;
        color: white !important;
        border-radius: 12px;
        width: 100%;
        font-weight: bold;
        height: 50px;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }

    /* टेक्स्ट स्टाईल */
    h1, h2, h3, label, p {
        font-family: 'Segoe UI', Roboto, sans-serif;
    }
    .car-price {
        color: #1b5e20;
        font-size: 20px;
        font-weight: 800;
    }
    
    /* WhatsApp बटण */
    .wa-btn {
        background-color: #25D366;
        color: white !important;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        display: block;
        text-decoration: none;
        font-weight: bold;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# २. डेटाबेस सेटअप
USER_DB = "users_data.csv"
BOOKING_DB = "bookings_data.csv"

for db, cols in [(USER_DB, ["Name", "Mobile", "Password"]), 
                 (BOOKING_DB, ["Time", "User", "Mobile", "From", "To", "Vehicle", "KM", "Fare", "Payment", "UTR"])]:
    if not os.path.exists(db):
        pd.DataFrame(columns=cols).to_csv(db, index=False)

# ३. सेशन स्टेट
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'selected_car' not in st.session_state: st.session_state.selected_car = None

# --- १. नवीन लोगो आणि हेडर विभाग ---
st.markdown("""
    <div class="app-header">
        <h1 style='margin:0; font-size: 28px;'>🔱 SHREE BALAJI 🔱</h1>
        <p style='margin:0; font-size: 16px; letter-spacing: 2px;'>LOGISTICS & TOURS AND TRAVELS</p>
    </div>
    """, unsafe_allow_html=True)

# --- २. लॉगिन / रजिस्ट्रेशन ---
if not st.session_state.logged_in:
    auth = st.radio("निवडा:", ["Login", "Register"], horizontal=True)

    with st.container():
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        if auth == "Register":
            name = st.text_input("तुमचे पूर्ण नाव")
        u_mob = st.text_input("मोबाईल नंबर", max_chars=10)
        u_pwd = st.text_input("पासवर्ड", type="password")

        if st.button("प्रवेश करा"):
            df = pd.read_csv(USER_DB)
            if auth == "Register":
                if name and u_mob and u_pwd:
                    if str(u_mob) in df['Mobile'].astype(str).values:
                        st.error("हा नंबर आधीच वापरला आहे!")
                    else:
                        pd.DataFrame([[name, u_mob, u_pwd]], columns=["Name", "Mobile", "Password"]).to_csv(USER_DB, mode='a', header=False, index=False)
                        st.success("नोंदणी पूर्ण! आता लॉगिन करा.")
                else: st.warning("सर्व रकाने भरा!")
            else:
                user = df[(df['Mobile'].astype(str) == str(u_mob)) & (df['Password'].astype(str) == str(u_pwd))]
                if not user.empty:
                    st.session_state.logged_in = True
                    st.session_state.u_name = user.iloc[0]['Name']
                    st.session_state.u_mob = u_mob
                    st.rerun()
                else: st.error("चुकीचा नंबर किंवा पासवर्ड!")
        st.markdown('</div>', unsafe_allow_html=True)

# --- ३. मुख्य ॲप ---
else:
    st.sidebar.markdown(f"### स्वागत, {st.session_state.u_name}!")
    menu = st.sidebar.selectbox("मेनू", ["🚕 बुक करा", "📜 हिस्ट्री", "🔓 Logout"])

    if menu == "🔓 Logout":
        st.session_state.logged_in = False
        st.session_state.selected_car = None
        st.rerun()

    elif menu == "📜 हिस्ट्री":
        st.title("📜 जुनी बुकिंग्स")
        df_b = pd.read_csv(BOOKING_DB)
        my_history = df_b[df_b['Mobile'].astype(str) == str(st.session_state.u_mob)]
        st.dataframe(my_history, use_container_width=True)

    elif menu == "🚕 बुक करा":
        if st.session_state.selected_car is None:
            st.markdown("### 🚕 उपलब्ध गाड्या निवडा")
            
            cars = {
                "Swift Dzire": {"rate": 12, "img": "https://imgd.aeplcdn.com/664x374/n/cw/ec/170173/dzire-exterior-right-front-three-quarter-3.jpeg"},
                "Maruti Ertiga (7 Seater)": {"rate": 15, "img": "https://imgd.aeplcdn.com/664x374/n/cw/ec/44701/ertiga-exterior-right-front-three-quarter-27.jpeg"},
                "Innova Crysta": {"rate": 20, "img": "https://imgd.aeplcdn.com/664x374/n/cw/ec/131131/innova-crysta-exterior-right-front-three-quarter-3.jpeg"},
                "Tempo Traveller": {"rate": 25, "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Force_Traveller.jpg/640px-Force_Traveller.jpg"}
            }

            for c_name, c_info in cars.items():
                st.markdown('<div class="main-card">', unsafe_allow_html=True)
                st.image(c_info["img"], use_container_width=True)
                st.markdown(f"<h3>{c_name}</h3>", unsafe_allow_html=True)
                st.markdown(f'<p class="car-price">दर: ₹{c_info["rate"]}/km</p>', unsafe_allow_html=True)
                if st.button(f"{c_name} बुक करा", key=c_name):
                    st.session_state.selected_car = c_name
                    st.session_state.car_rate = c_info['rate']
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.button("⬅️ मागे जा", on_click=lambda: st.session_state.update({"selected_car": None}))
            
            st.markdown('<div class="main-card">', unsafe_allow_html=True)
            st.header(f"बुकिंग: {st.session_state.selected_car}")
            p_up = st.text_input("📍 पिकअप पॉईंट")
            d_off = st.text_input("🏁 ड्रॉप पॉईंट")
            km = st.number_input("अंदाजे अंतर (KM)", min_value=1, value=10)
            fare = km * st.session_state.car_rate
            st.success(f"## अंदाजे भाडे: ₹{fare}")

            pay = st.radio("पेमेंट:", ["Cash", "PhonePe Scanner"], horizontal=True)
            utr = ""
            if pay == "PhonePe Scanner":
                st.image("1000327329.png", width=300, caption="Shree Balaji Logistic ला पेमेंट करा")
                utr = st.text_input("Transaction ID (UTR) टाका")

            if st.button("Confirm Booking ✅"):
                if p_up and d_off:
                    data = [datetime.now().strftime("%Y-%m-%d %H:%M"), st.session_state.u_name, st.session_state.u_mob, p_up, d_off, st.session_state.selected_car, km, fare, pay, utr]
                    pd.DataFrame([data]).to_csv(BOOKING_DB, mode='a', header=False, index=False)
                    
                    msg = f"*नवीन बुकिंग - Balaji Logistics*\nगाडी: {st.session_state.selected_car}\nPick: {p_up}\nDrop: {d_off}\nभाडे: ₹{fare}"
                    url = f"https://wa.me/919767981986?text={urllib.parse.quote(msg)}"
                    st.success("बुकिंग कन्फर्म झाली!")
                    st.markdown(f'<a href="{url}" target="_blank" class="wa-btn">📲 मालकाला कळवा</a>', unsafe_allow_html=True)
                else: st.error("माहिती अपूर्ण आहे!")
            st.markdown('</div>', unsafe_allow_html=True)