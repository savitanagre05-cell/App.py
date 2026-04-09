import streamlit as st
import pandas as pd
import os
import urllib.parse
from datetime import datetime

# १. ॲप कॉन्फिगरेशन आणि स्टाईलिंग
st.set_page_config(page_title="Balaji Logistics and Tours and Travels", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6 !important; } 
    .main-card { background: white; padding: 25px; border-radius: 20px; box-shadow: 0 5px 15px rgba(0,0,0,0.08); border: 1px solid #e0e0e0; margin-bottom: 25px; }
    .car-card { background: white; padding: 15px; border-radius: 15px; text-align: center; border: 1px solid #eee; margin-bottom: 15px; }
    .stButton>button { background-color: #00416A !important; color: white !important; border-radius: 10px; width: 100%; font-weight: bold; border: none; padding: 10px; height: 45px; }
    label, p, span { color: #333 !important; font-weight: 600; }
    .wa-btn { background-color: #25D366; color: white; padding: 15px; border-radius: 12px; text-align: center; display: block; text-decoration: none; font-weight: bold; font-size: 16px; margin-top: 10px; }
    .car-price { color: #28a745; font-size: 18px; font-weight: bold; margin-bottom: 8px; }
    h3 { margin-bottom: 5px; color: #00416A; font-size: 22px; }
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

def reset_selection():
    st.session_state.selected_car = None

# --- पायरी १: लॉगिन / रजिस्ट्रेशन ---
if not st.session_state.logged_in:
    st.title("🛡️ Balaji Logistics - Welcome")
    auth = st.radio("निवडा:", ["Login", "Register"], horizontal=True)

    with st.container():
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        if auth == "Register":
            name = st.text_input("पूर्ण नाव", placeholder="उदा. राहुल पाटील")

        u_mob = st.text_input("मोबाईल नंबर", placeholder="98XXXXXXXX")
        u_pwd = st.text_input("पासवर्ड", type="password", placeholder="******")

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

# --- पायरी २: मुख्य ॲप ---
else:
    st.sidebar.title(f"👋 नमस्ते, {st.session_state.u_name}")
    menu = st.sidebar.radio("मेनू", ["🚕 गाडी बुक करा", "📜 माझी हिस्ट्री", "🔓 Logout"])

    if menu == "🔓 Logout":
        st.session_state.logged_in = False
        st.session_state.selected_car = None
        st.rerun()

    elif menu == "📜 माझी हिस्ट्री":
        st.title("📜 तुमची जुनी बुकिंग्स")
        df_b = pd.read_csv(BOOKING_DB)
        my_history = df_b[df_b['Mobile'].astype(str) == str(st.session_state.u_mob)]
        if not my_history.empty:
            st.dataframe(my_history.sort_values(by='Time', ascending=False), use_container_width=True)
        else:
            st.info("तुम्ही अजून कोणतीही गाडी बुक केलेली नाही.")

    elif menu == "🚕 गाडी बुक करा":
        if st.session_state.selected_car is None:
            st.title("🚕 उपलब्ध गाड्या")
            
            cars = {
                "Swift Dzire": {"rate": 12, "img": "https://imgd.aeplcdn.com/664x374/n/cw/ec/170173/dzire-exterior-right-front-three-quarter-3.jpeg"},
                "Hyundai Aura": {"rate": 13, "img": "https://imgd.aeplcdn.com/664x374/n/cw/ec/128413/aura-exterior-right-front-three-quarter-51.jpeg"},
                "Maruti Ertiga": {"rate": 15, "img": "https://imgd.aeplcdn.com/664x374/n/cw/ec/44701/ertiga-exterior-right-front-three-quarter-27.jpeg"},
                "Innova Crysta": {"rate": 20, "img": "https://imgd.aeplcdn.com/664x374/n/cw/ec/131131/innova-crysta-exterior-right-front-three-quarter-3.jpeg"},
                "Tempo Traveler": {"rate": 25, "img": "https://5.imimg.com/data5/SELLER/Default/2021/3/XW/QD/TM/124230623/17-seater-luxury-tempo-traveller-500x500.jpg"}
            }

            for c_name, c_info in cars.items():
                st.markdown('<div class="main-card">', unsafe_allow_html=True)
                st.markdown(f"<h3>{c_name}</h3>", unsafe_allow_html=True)
                st.markdown(f'<p class="car-price">दर: ₹{c_info["rate"]}/km</p>', unsafe_allow_html=True)
                st.image(c_info["img"], use_container_width=True)
                if st.button(f"{c_name} बुक करा", key=c_name):
                    st.session_state.selected_car = c_name
                    st.session_state.car_rate = c_info['rate']
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.button("⬅️ गाड्यांच्या यादीवर परत जा", on_click=reset_selection)
            st.header(f"📍 बुकिंग फॉर्म: {st.session_state.selected_car}")

            st.markdown('<div class="main-card">', unsafe_allow_html=True)
            p_up = st.text_input("📍 Pickup Point", placeholder="उदा. नाशिक सिटी")
            d_off = st.text_input("🏁 Drop Point", placeholder="उदा. शिर्डी")
            km = st.number_input("अंदाजे अंतर (KM)", min_value=1, value=10)

            fare = km * st.session_state.car_rate
            st.success(f"### अंदाजे एकूण भाडे: ₹{fare}")

            pay = st.radio("पेमेंट मोड निवडा:", ["Cash", "PhonePe Scanner"], horizontal=True)
            utr = ""
            if pay == "PhonePe Scanner":
                # *** तुझा QR कोड इथे लोड केला आहे ***
                st.markdown("<center><b>Shree Balaji Logistic ला पेमेंट करण्यासाठी स्कॅन करा</b></center>", unsafe_allow_html=True)
                st.image("image_0.png", width=300)
                utr = st.text_input("Transaction ID (UTR) टाका")

            if st.button("Confirm Booking ✅"):
                if p_up and d_off:
                    data = [datetime.now().strftime("%Y-%m-%d %H:%M"), st.session_state.u_name, 
                            st.session_state.u_mob, p_up, d_off, st.session_state.selected_car, 
                            km, fare, pay, utr]
                    pd.DataFrame([data]).to_csv(BOOKING_DB, mode='a', header=False, index=False)

                    # WhatsApp मेसेज (For Admin)
                    msg = (f"*नवीन बुकिंग - Balaji Logistics*\n"
                           f"--------------------------\n"
                           f"नाव: {st.session_state.u_name}\n"
                           f"गाडी: {st.session_state.selected_car}\n"
                           f"Pick: {p_up}\n"
                           f"Drop: {d_off}\n"
                           f"भाडे: ₹{fare}\n"
                           f"पेमेंट: {pay}\n"
                           f"UTR: {utr if utr else 'N/A'}")
                    url = f"https://wa.me/919767981986?text={urllib.parse.quote(msg)}"

                    st.success("बुकिंग यशस्वीरित्या नोंदवली गेली आहे!")
                    st.markdown(f'<a href="{url}" target="_blank" class="wa-btn">📲 मालकाला WhatsApp वर कळवा</a>', unsafe_allow_html=True)
                    st.balloons()
                else:
                    st.error("कृपया सर्व माहिती भरा!")
            st.markdown('</div>', unsafe_allow_html=True)