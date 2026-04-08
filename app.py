import streamlit as st
import pandas as pd
import os
import urllib.parse
from datetime import datetime

# १. ॲप कॉन्फिगरेशन आणि स्टाईलिंग
st.set_page_config(page_title="Balaji Logistics and Tours and Travels", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff !important; }
    .main-card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); border: 1px solid #dee2e6; margin-bottom: 20px; }
    .car-card { background: #f1f3f5; padding: 15px; border-radius: 12px; border: 2px solid #dee2e6; text-align: center; margin-bottom: 10px; }
    .stButton>button { background-color: #00416A !important; color: white !important; border-radius: 8px; width: 100%; font-weight: bold; }
    label, p, span { color: black !important; font-weight: 600; }
    .wa-btn { background-color: #25D366; color: white; padding: 12px; border-radius: 10px; text-align: center; display: block; text-decoration: none; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# २. डेटाबेस सेटअप (CSV फाईल्स)
USER_DB = "users_data.csv"
BOOKING_DB = "bookings_data.csv"

for db, cols in [(USER_DB, ["Name", "Mobile", "Password"]), 
                 (BOOKING_DB, ["Time", "User", "Mobile", "From", "To", "Vehicle", "KM", "Fare", "Payment", "UTR"])]:
    if not os.path.exists(db):
        pd.DataFrame(columns=cols).to_csv(db, index=False)

# ३. सेशन स्टेट मॅनेजमेंट
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'selected_car' not in st.session_state: st.session_state.selected_car = None

def reset_selection():
    st.session_state.selected_car = None
    st.rerun()

# --- पायरी १: लॉगिन / रजिस्ट्रेशन विभाग ---
if not st.session_state.logged_in:
    if os.path.exists("1000326575.png"):
        st.image("1000326575.png", use_container_width=True) #
    
    st.title("Balaji Logistics - Welcome")
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

# --- पायरी २: मुख्य ॲप (लॉगिन नंतर) ---
else:
    st.sidebar.title(f"नमस्ते, {st.session_state.u_name}")
    menu = st.sidebar.radio("मेनू", ["🚕 गाडी बुक करा", "📜 माझी हिस्ट्री", "🔓 Logout"])

    if menu == "🔓 Logout":
        st.session_state.logged_in = False
        st.session_state.selected_car = None
        st.rerun()

    elif menu == "📜 माझी हिस्ट्री": #
        st.title("तुमची जुनी बुकिंग्स")
        df_b = pd.read_csv(BOOKING_DB)
        my_history = df_b[df_b['Mobile'].astype(str) == str(st.session_state.u_mob)]
        if not my_history.empty:
            st.dataframe(my_history.sort_values(by='Time', ascending=False))
        else:
            st.info("तुम्ही अजून कोणतीही गाडी बुक केलेली नाही.")

    elif menu == "🚕 गाडी बुक करा":
        if st.session_state.selected_car is None:
            st.title("🚕 उपलब्ध गाड्या निवडा")
            # Uber Style Car Cards
            cars = {
                "Swift Dzire": {"rate": 12, "icon": "🚗"},
                "Hyundai Aura": {"rate": 13, "icon": "🚘"},
                "Maruti Ertiga": {"rate": 15, "icon": "🚐"},
                "Innova Crysta": {"rate": 20, "icon": "🚙"},
                "Tempo Traveler": {"rate": 25, "icon": "🚌"}
            }

            for c_name, c_info in cars.items():
                st.markdown(f"""
                    <div class="car-card">
                        <div style='font-size: 35px;'>{c_info['icon']}</div>
                        <h3>{c_name}</h3>
                        <p style='color: #28a745;'>दर: ₹{c_info['rate']}/km</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"{c_name} निवडा", key=c_name):
                    st.session_state.selected_car = c_name
                    st.session_state.car_rate = c_info['rate']
                    st.rerun()
        else:
            # बुकिंग फॉर्म (Next Page)
            st.button("⬅️ गाड्यांच्या यादीवर परत जा", on_click=reset_selection)
            st.header(f"📍 बुकिंग फॉर्म: {st.session_state.selected_car}")
            
            st.markdown('<div class="main-card">', unsafe_allow_html=True)
            p_up = st.text_input("📍 Pickup Point")
            d_off = st.text_input("🏁 Drop Point")
            km = st.number_input("अंदाजे अंतर (KM)", min_value=1, value=10)
            
            fare = km * st.session_state.car_rate
            st.success(f"### अंदाजे एकूण भाडे: ₹{fare}")

            # पेमेंट ऑप्शन्स
            pay = st.radio("पेमेंट मोड निवडा:", ["Cash", "PhonePe Scanner"], horizontal=True)
            utr = ""
            if pay == "PhonePe Scanner":
                if os.path.exists("1000327329.png"):
                    st.image("1000327329.png", width=250, caption="Scan & Pay to Balaji Logistics") #
                utr = st.text_input("Transaction ID (UTR) टाका")

            if st.button("Confirm Booking ✅"):
                if p_up and d_off:
                    # १. CSV मध्ये डेटा सेव्ह करणे
                    data = [datetime.now().strftime("%Y-%m-%d %H:%M"), st.session_state.u_name, 
                            st.session_state.u_mob, p_up, d_off, st.session_state.selected_car, 
                            km, fare, pay, utr]
                    pd.DataFrame([data]).to_csv(BOOKING_DB, mode='a', header=False, index=False)
                    
                    # २. WhatsApp मेसेज तयार करणे (9767981986 वर)
                    msg = (f"*नवीन बुकिंग - Balaji Logistics*\n"
                           f"नाव: {st.session_state.u_name}\n"
                           f"मोबाईल: {st.session_state.u_mob}\n"
                           f"गाडी: {st.session_state.selected_car}\n"
                           f"Pickup: {p_up}\n"
                           f"Drop: {d_off}\n"
                           f"भाडे: ₹{fare}\n"
                           f"पेमेंट: {pay}\n"
                           f"UTR: {utr if utr else 'N/A'}")
                    url = f"https://wa.me/919767981986?text={urllib.parse.quote(msg)}"
                    
                    st.success("बुकिंग यशस्वीरित्या नोंदवली गेली आहे!")
                    st.markdown(f'<a href="{url}" target="_blank" class="wa-btn">📲 मालकाला WhatsApp वर कळवा</a>', unsafe_allow_html=True)
                    st.balloons()
                else:
                    st.error("कृपया पिकअप आणि ड्रॉप लोकेशन भरा!")
            st.markdown('</div>', unsafe_allow_html=True)