import streamlit as st
import pandas as pd
import os
import urllib.parse
from datetime import datetime

# १. ॲप कॉन्फिगरेशन आणि स्टाईलिंग
st.set_page_config(page_title="Balaji Logistics & Tours", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .main-card {
        background: white; padding: 25px; border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-top: 8px solid #0A3D62;
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #0A3D62; color: white; width: 100%;
        border-radius: 10px; height: 50px; font-weight: bold; font-size: 18px;
    }
    .wa-button {
        background-color: #25D366; color: white; padding: 15px;
        border-radius: 12px; text-align: center; font-weight: bold;
        display: block; text-decoration: none; font-size: 18px;
    }
    .fare-box {
        background-color: #fff3cd; padding: 15px; border-radius: 10px;
        text-align: center; border: 1px solid #ffc107; color: #856404; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# २. डेटाबेस फाईल्स (Users आणि Bookings)
USER_DB = "users_data.csv"
BOOKING_DB = "bookings_data.csv"

for db, cols in [(USER_DB, ["Name", "Mobile", "Password"]), 
                 (BOOKING_DB, ["Time", "User", "Mobile", "From", "To", "Vehicle", "KM", "Fare", "Payment", "UTR"])]:
    if not os.path.exists(db):
        pd.DataFrame(columns=cols).to_csv(db, index=False)

# ३. सेशन स्टेट (लॉगिन चेक)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- पायरी १: लॉगिन आणि रजिस्ट्रेशन विभाग ---
if not st.session_state.logged_in:
    if os.path.exists("1000326575.png"):
        st.image("1000326575.png", width=250)
    st.title("Balaji Logistics - Welcome")
    
    auth_mode = st.radio("निवडा:", ["Login", "Register"], horizontal=True)

    with st.form("auth_form"):
        name = st.text_input("पूर्ण नाव") if auth_mode == "Register" else ""
        mob = st.text_input("मोबाईल नंबर")
        pwd = st.text_input("पासवर्ड", type="password")
        
        if st.form_submit_button("प्रवेश करा"):
            if auth_mode == "Register":
                df = pd.read_csv(USER_DB)
                if str(mob) in df['Mobile'].astype(str).values:
                    st.error("हा नंबर आधीच नोंदणीकृत आहे!")
                else:
                    pd.DataFrame([[name, mob, pwd]], columns=["Name", "Mobile", "Password"]).to_csv(USER_DB, mode='a', header=False, index=False)
                    st.success("नोंदणी यशस्वी! आता लॉगिन करा.")
            else:
                df = pd.read_csv(USER_DB)
                user = df[(df['Mobile'].astype(str) == str(mob)) & (df['Password'].astype(str) == str(pwd))]
                if not user.empty:
                    st.session_state.logged_in = True
                    st.session_state.user_name = user.iloc[0]['Name']
                    st.session_state.user_mob = mob
                    st.rerun()
                else:
                    st.error("नंबर किंवा पासवर्ड चुकीचा आहे!")

# --- पायरी २: मुख्य ॲप इंटरफेस (लॉगिन झाल्यावर) ---
else:
    # डाव्या बाजूचा मेनू (Sidebar)
    st.sidebar.title(f"नमस्ते, {st.session_state.user_name}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # Admin Panel (फक्त मालकासाठी)
    if st.sidebar.checkbox("🔒 Admin Panel"):
        admin_pass = st.sidebar.text_input("Admin Password", type="password")
        if admin_pass == "balaji123":
            st.subheader("📊 सर्व डेटा")
            st.write("**सर्व युजर्स:**")
            st.dataframe(pd.read_csv(USER_DB))
            st.write("**सर्व बुकिंग्स:**")
            st.dataframe(pd.read_csv(BOOKING_DB))

    # मुख्य स्क्रीन
    if os.path.exists("1000326575.png"):
        st.image("1000326575.png", width=120)
    st.title("🚖 Book Your Ride")

    tab1, tab2 = st.tabs(["📍 बुकिंग तपशील", "💳 पेमेंट"])

    with tab1:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        p_up = st.text_input("कुठून (Pickup Location)")
        d_off = st.text_input("कुठे (Drop Location)")
        
        # गाड्या आणि किलोमीटर कॅल्क्युलेटर
        car_rates = {
            "Hyundai Aura": 13,
            "Maruti Ertiga": 15,
            "Swift Dzire": 12,
            "Innova Crysta": 20,
            "Tempo Traveler": 25
        }
        selected_car = st.selectbox("गाडी निवडा:", list(car_rates.keys()))
        distance = st.number_input("अंदाजे अंतर (KM)", min_value=1, value=10)
        
        total_price = distance * car_rates[selected_car]
        
        st.markdown(f"""
            <div class="fare-box">
                अंदाजे भाडे: ₹{total_price} <br>
                <small>({distance} KM × ₹{car_rates[selected_car]}/km)</small>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        pay_method = st.radio("पेमेंट निवडा:", ["💵 Cash (प्रवासानंतर)", "📱 PhonePe Scanner"], horizontal=True)
        utr_no = ""

        if pay_method == "📱 PhonePe Scanner":
            if os.path.exists("1000327329.png"):
                st.image("1000327329.png", width=250, caption="Shree Balaji Logistic")
            utr_no = st.text_input("UTR / Transaction ID टाका")
        
        if st.button("Confirm Booking ✅"):
            if p_up and d_off:
                # डेटा सेव्ह करणे
                new_entry = [datetime.now(), st.session_state.user_name, st.session_state.user_mob, 
                             p_up, d_off, selected_car, distance, total_price, pay_method, utr_no]
                pd.DataFrame([new_entry]).to_csv(BOOKING_DB, mode='a', header=False, index=False)
                
                # WhatsApp Notification (तुमच्या नंबरवर मेसेज जाईल)
                wa_msg = f"*नवीन बुकिंग - Balaji Logistics*\n👤 नाव: {st.session_state.user_name}\n📞 मोबा: {st.session_state.user_mob}\n📍 Pickup: {p_up}\n🏁 Drop: {d_off}\n🚗 गाडी: {selected_car}\n📏 अंतर: {distance} KM\n💰 भाडे: ₹{total_price}\n💳 पेमेंट: {pay_method}\n🔢 UTR: {utr_no if utr_no else 'N/A'}"
                wa_url = f"https://wa.me/919767981986?text={urllib.parse.quote(wa_msg)}"
                
                st.success("✅ तुमची बुकिंग नोंदवली गेली आहे!")
                st.markdown(f'<a href="{wa_url}" target="_blank" class="wa-button">📲 WhatsApp वर मालकाला कळवा</a>', unsafe_allow_html=True)
                st.balloons()
            else:
                st.error("कृपया पिकअप आणि ड्रॉप लोकेशन भरा!")
        st.markdown('</div>', unsafe_allow_html=True)