import streamlit as st
import pandas as pd
import os
import urllib.parse
from datetime import datetime

# १. ॲप कॉन्फिगरेशन
st.set_page_config(page_title="Balaji Logistics", layout="centered")

# २. CSS डिझाइन
st.markdown("""
    <style>
    .header-container { text-align: center; padding: 10px; margin-bottom: 20px; border-bottom: 3px solid #FFD700; }
    .main-title { color: #00416A; font-size: 30px; font-weight: bold; text-transform: uppercase; margin-bottom: 0px; }
    .sub-title { color: #00416A; font-size: 16px; font-weight: bold; letter-spacing: 2px; }
    .main-card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); border: 1px solid #eee; margin-bottom: 80px; }
    .category-label { background: #00416A; color: white; padding: 5px 15px; border-radius: 5px; margin: 15px 0; font-weight: bold; }
    .stButton>button { background-color: #00416A !important; color: white !important; width: 100%; font-weight: bold; border-radius: 8px; }
    .wa-btn { background-color: #25D366; color: white !important; padding: 12px; border-radius: 8px; text-align: center; display: block; text-decoration: none; font-weight: bold; margin-top: 10px; }
    .notice-box { background-color: #fff3cd; padding: 12px; border-left: 5px solid #ffa000; border-radius: 5px; margin: 10px 0; font-size: 14px; color: #856404; }
    </style>
    """, unsafe_allow_html=True)

# ३. लोगो विभाग
st.markdown("""
    <div class="header-container">
        <h1 class="main-title">SHREE BALAJI</h1>
        <p class="sub-title">LOGISTICS</p>
    </div>
    """, unsafe_allow_html=True)

# ४. डेटाबेस सेटअप
USER_DB = "users_data.csv"
BOOKING_DB = "bookings_data.csv"

for db, cols in [(USER_DB, ["Name", "Mobile", "Password"]), (BOOKING_DB, ["Time", "User", "Mobile", "From", "To", "Vehicle", "KM", "Fare", "Payment", "UTR"])]:
    if not os.path.exists(db):
        pd.DataFrame(columns=cols).to_csv(db, index=False)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "Home"
if 'selected_car' not in st.session_state: st.session_state.selected_car = None

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
                        st.success("नोंदणी यशस्वी! लॉगिन करा.")
                else: st.warning("सर्व माहिती भरा!")
            else:
                user = df[(df['Mobile'].astype(str) == str(u_mob)) & (df['Password'].astype(str) == str(u_pwd))]
                if not user.empty:
                    st.session_state.logged_in = True
                    st.session_state.u_name = user.iloc[0]['Name']
                    st.session_state.u_mob = u_mob
                    st.rerun()
                else: st.error("नंबर किंवा पासवर्ड चुकीचा!")
        st.markdown('</div>', unsafe_allow_html=True)

# --- मुख्य ॲप ---
else:
    if st.session_state.page == "Home":
        st.markdown(f"<h2>नमस्ते, {st.session_state.u_name}! 👋</h2>", unsafe_allow_html=True)
        st.markdown('<div class="main-card"><h3>Shree Balaji Logistics</h3><p>नाशिकमधील सर्वात उत्तम ट्रॅव्हल्स सर्व्हिस.</p></div>', unsafe_allow_html=True)

    elif st.session_state.page == "History":
        st.subheader("📜 तुमची हिस्ट्री")
        df_b = pd.read_csv(BOOKING_DB)
        history = df_b[df_b['Mobile'].astype(str) == str(st.session_state.u_mob)]
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        if history.empty: st.info("हिस्ट्री रिकामी आहे.")
        else: st.dataframe(history, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.page == "Profile":
        st.subheader("👤 प्रोफाइल")
        df_b = pd.read_csv(BOOKING_DB)
        count = len(df_b[df_b['Mobile'].astype(str) == str(st.session_state.u_mob)])
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.write(f"**नाव:** {st.session_state.u_name}")
        st.write(f"**मोबाईल:** {st.session_state.u_mob}")
        st.write(f"**एकूण बुकिंग्स:** {count}")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.page == "Book":
        if st.session_state.selected_car is None:
            car_categories = {
                "🚗 Mini": {
                    "WagonR": {"rate": 11, "seats": "4+1", "img": "https://imgd.aeplcdn.com/664x374/n/cw/ec/140591/wagon-r-exterior-right-front-three-quarter-5.jpeg"},
                    "Alto K10": {"rate": 10, "seats": "4+1", "img": "https://imgd.aeplcdn.com/664x374/n/cw/ec/127583/alto-k10-exterior-right-front-three-quarter-58.jpeg"}
                },
                "🚕 Sedan": {
                    "Swift Dzire": {"rate": 12, "seats": "4+1", "img": "https://imgd.aeplcdn.com/664x374/n/cw/ec/170173/dzire-exterior-right-front-three-quarter-3.jpeg"},
                    "Aura": {"rate": 12, "seats": "4+1", "img": "https://imgd.aeplcdn.com/664x374/n/cw/ec/141125/aura-exterior-right-front-three-quarter-7.jpeg"}
                },
                "🚙 SUV/Prime": {
                    "Ertiga": {"rate": 15, "seats": "6+1", "img": "https://imgd.aeplcdn.com/664x374/n/cw/ec/44701/ertiga-exterior-right-front-three-quarter-27.jpeg"},
                    "Innova Crysta": {"rate": 20, "seats": "7+1", "img": "https://imgd.aeplcdn.com/664x374/n/cw/ec/34468/innova-crysta-exterior-right-front-three-quarter-2.jpeg"},
                    "Marazzo": {"rate": 16, "seats": "7+1", "img": "https://imgd.aeplcdn.com/664x374/n/cw/ec/26551/marazzo-exterior-right-front-three-quarter.jpeg"}
                },
                "🚌 Groups": {
                    "Tempo Traveller": {"rate": 25, "seats": "17+1", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Force_Traveller.jpg/640px-Force_Traveller.jpg"},
                    "Urbania": {"rate": 30, "seats": "13+1", "img": "https://imgd.aeplcdn.com/664x374/n/cw/ec/133033/urbania-exterior-right-front-three-quarter.jpeg"}
                }
            }
            for cat, car_list in car_categories.items():
                st.markdown(f'<div class="category-label">{cat}</div>', unsafe_allow_html=True)
                for c_name, c_info in car_list.items():
                    st.markdown('<div class="main-card">', unsafe_allow_html=True)
                    st.image(c_info["img"], use_container_width=True)
                    st.subheader(f"{c_name}")
                    st.write(f"दर: ₹{c_info['rate']}/km | सीट: {c_info['seats']}")
                    if st.button(f"{c_name} निवडा", key=c_name):
                        st.session_state.selected_car, st.session_state.car_rate = c_name, c_info['rate']
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.button("⬅️ मागे", on_click=lambda: st.session_state.update({"selected_car": None}))
            st.markdown('<div class="main-card">', unsafe_allow_html=True)
            st.header(f"बुकिंग: {st.session_state.selected_car}")
            p_up, d_off = st.text_input("पिकअप"), st.text_input("ड्रॉप")
            km = st.number_input("अंदाजित KM", min_value=1, value=100)
            fare = km * st.session_state.car_rate
            
            st.info(f"💰 अंदाजित भाडे: ₹{fare}")
            
            # --- टोल आणि चार्जेसची सूचना ---
            st.markdown("""
                <div class="notice-box">
                    <strong>⚠️ महत्त्वाच्या अटी:</strong><br>
                    • टोल, पार्किंग आणि बॉर्डर टॅक्स ग्राहकाने स्वतंत्रपणे द्यायचे आहेत.<br>
                    • हे चार्जेस वरील भाड्यात समाविष्ट नाहीत.<br>
                    • ड्रायव्हर भत्ता (रात्रीसाठी) लागू असल्यास तो अतिरिक्त असेल.
                </div>
                """, unsafe_allow_html=True)
            
            pay = st.radio("पेमेंट मोड:", ["Cash", "PhonePe"], horizontal=True)
            utr = st.text_input("UTR (PhonePe असल्यास)") if pay == "PhonePe" else "N/A"
                
            if st.button("Confirm Booking ✅"):
                if p_up and d_off:
                    data = [datetime.now().strftime("%Y-%m-%d %H:%M"), st.session_state.u_name, st.session_state.u_mob, p_up, d_off, st.session_state.selected_car, km, fare, pay, utr]
                    pd.DataFrame([data]).to_csv(BOOKING_DB, mode='a', header=False, index=False)
                    
                    # WhatsApp मेसेज मधे स्पष्ट उल्लेख
                    msg = f"🚩 *नवीन बुकिंग - Shree Balaji Logistics* 🚩\n\n" \
                          f"👤 *नाव:* {st.session_state.u_name}\n" \
                          f"📞 *मोबाईल:* {st.session_state.u_mob}\n" \
                          f"🚗 *गाडी:* {st.session_state.selected_car}\n" \
                          f"📍 *पिकअप:* {p_up}\n" \
                          f"🏁 *ड्रॉप:* {d_off}\n" \
                          f"🛣️ *KM:* {km}\n" \
                          f"💰 *भाडे:* ₹{fare}\n" \
                          f"💳 *पेमेंट:* {pay}\n" \
                          f"\n⚠️ *नोंद:* टोल, पार्किंग आणि टॅक्स ग्राहकाकडून (Customer) देय असतील."
                    
                    encoded_msg = urllib.parse.quote(msg)
                    wa_url = f"https://wa.me/919767981986?text={encoded_msg}"
                    
                    st.success("बुकिंग यशस्वी!"); 
                    st.markdown(f'<a href="{wa_url}" target="_blank" class="wa-btn">WhatsApp वर डिटेल्स पाठवा 💬</a>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # ५. Bottom Navigation
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        if st.button("🏠 Home"): st.session_state.page = "Home"; st.rerun()
    with col_b:
        if st.button("🚕 Book"): st.session_state.page = "Book"; st.rerun()
    with col_c:
        if st.button("📜 Hist"): st.session_state.page = "History"; st.rerun()
    with col_d:
        if st.button("👤 Prof"): st.session_state.page = "Profile"; st.rerun()