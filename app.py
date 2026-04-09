import streamlit as st
import pandas as pd
import os
import urllib.parse
from datetime import datetime

# १. ॲप कॉन्फिगरेशन
st.set_page_config(page_title="Balaji Logistics", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa !important; }
    .main-card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 20px; border: 1px solid #eee; }
    .header-text { text-align: center; color: #00416A; padding: 10px; border-bottom: 2px solid #FFD700; margin-bottom: 20px; }
    .stButton>button { background-color: #00416A !important; color: white !important; font-weight: bold; border-radius: 8px; }
    .wa-btn { background-color: #25D366; color: white !important; padding: 12px; border-radius: 10px; text-align: center; display: block; text-decoration: none; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# २. डेटाबेस फाईल्स
USER_DB = "users_data.csv"
BOOKING_DB = "bookings_data.csv"

for db, cols in [(USER_DB, ["Name", "Mobile", "Password"]), (BOOKING_DB, ["Time", "User", "Mobile", "From", "To", "Vehicle", "KM", "Fare", "Payment", "UTR"])]:
    if not os.path.exists(db):
        pd.DataFrame(columns=cols).to_csv(db, index=False)

# ३. सेशन स्टेट
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'selected_car' not in st.session_state: st.session_state.selected_car = None

st.markdown("<div class='header-text'><h1>🔱 SHREE BALAJI LOGISTICS 🔱</h1></div>", unsafe_allow_html=True)

# --- लॉगिन / रजिस्ट्रेशन ---
if not st.session_state.logged_in:
    auth = st.radio("निवडा:", ["Login", "Register"], horizontal=True)
    with st.container():
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        if auth == "Register":
            name = st.text_input("पूर्ण नाव")
        u_mob = st.text_input("मोबाईल नंबर")
        u_pwd = st.text_input("पासवर्ड", type="password")

        if st.button("प्रवेश करा"):
            df = pd.read_csv(USER_DB)
            if auth == "Register":
                if name and u_mob and u_pwd:
                    if str(u_mob) in df['Mobile'].astype(str).values:
                        st.error("हा नंबर आधीच नोंदणीकृत आहे!")
                    else:
                        pd.DataFrame([[name, u_mob, u_pwd]], columns=["Name", "Mobile", "Password"]).to_csv(USER_DB, mode='a', header=False, index=False)
                        st.success("नोंदणी यशस्वी! आता लॉगिन करा.")
                else: st.warning("सर्व माहिती भरा!")
            else:
                user = df[(df['Mobile'].astype(str) == str(u_mob)) & (df['Password'].astype(str) == str(u_pwd))]
                if not user.empty:
                    st.session_state.logged_in = True
                    st.session_state.u_name = user.iloc[0]['Name']
                    st.session_state.u_mob = u_mob
                    st.rerun()
                else: st.error("नंबर किंवा पासवर्ड चुकीचा आहे!")
        st.markdown('</div>', unsafe_allow_html=True)

# --- मुख्य ॲप ---
else:
    st.sidebar.write(f"नमस्ते, {st.session_state.u_name}")
    menu = st.sidebar.selectbox("मेनू", ["🚕 गाडी बुक करा", "📜 माझी हिस्ट्री", "Logout"])

    if menu == "Logout":
        st.session_state.logged_in = False
        st.rerun()

    elif menu == "📜 माझी हिस्ट्री":
        st.title("📜 हिस्ट्री")
        df_b = pd.read_csv(BOOKING_DB)
        history = df_b[df_b['Mobile'].astype(str) == str(st.session_state.u_mob)]
        st.dataframe(history)

    else:
        if st.session_state.selected_car is None:
            st.title("🚕 गाड्या निवडा")
            # तुझे मूळ फोटो इथे आहेत
            cars = {
                "Swift Dzire": {"rate": 12, "img": "https://imgd.aeplcdn.com/664x374/n/cw/ec/170173/dzire-exterior-right-front-three-quarter-3.jpeg"},
                "Ertiga": {"rate": 15, "img": "https://imgd.aeplcdn.com/664x374/n/cw/ec/44701/ertiga-exterior-right-front-three-quarter-27.jpeg"},
                "Innova Crysta": {"rate": 20, "img": "https://imgd.aeplcdn.com/664x374/n/cw/ec/131131/innova-crysta-exterior-right-front-three-quarter-3.jpeg"}
            }

            for c_name, c_info in cars.items():
                st.markdown('<div class="main-card">', unsafe_allow_html=True)
                st.image(c_info["img"], use_container_width=True)
                st.subheader(c_name)
                st.write(f"दर: ₹{c_info['rate']}/km")
                if st.button(f"{c_name} निवडा", key=c_name):
                    st.session_state.selected_car = c_name
                    st.session_state.car_rate = c_info['rate']
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.button("⬅️ मागे जा", on_click=lambda: st.session_state.update({"selected_car": None}))
            st.markdown('<div class="main-card">', unsafe_allow_html=True)
            st.header(f"बुकिंग: {st.session_state.selected_car}")
            p_up = st.text_input("पिकअप पॉईंट")
            d_off = st.text_input("ड्रॉप पॉईंट")
            km = st.number_input("KM", min_value=1, value=10)
            fare = km * st.session_state.car_rate
            st.info(f"भाडे: ₹{fare}")

            pay = st.radio("पेमेंट:", ["Cash", "Scanner"])
            utr = ""
            if pay == "Scanner":
                st.image("1000327329.png", width=300)
                utr = st.text_input("UTR नंबर")

            if st.button("Confirm ✅"):
                if p_up and d_off:
                    data = [datetime.now().strftime("%Y-%m-%d %H:%M"), st.session_state.u_name, st.session_state.u_mob, p_up, d_off, st.session_state.selected_car, km, fare, pay, utr]
                    pd.DataFrame([data]).to_csv(BOOKING_DB, mode='a', header=False, index=False)
                    msg = f"*बुकिंग*\nनाव: {st.session_state.u_name}\nगाडी: {st.session_state.selected_car}\nPick: {p_up}\nDrop: {d_off}\nभाडे: ₹{fare}"
                    url = f"https://wa.me/919767981986?text={urllib.parse.quote(msg)}"
                    st.success("यशस्वी!")
                    st.markdown(f'<a href="{url}" target="_blank" class="wa-btn">WhatsApp करा</a>', unsafe_allow_html=True)
                else: st.error("माहिती भरा!")
            st.markdown('</div>', unsafe_allow_html=True)