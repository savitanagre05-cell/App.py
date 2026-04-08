import streamlit as st
import urllib.parse, folium
from streamlit_folium import st_folium

# १. मुख्य सेटिंग्ज आणि तुझा नंबर
st.set_page_config(page_title="Balaji Logistics", layout="centered", page_icon="📦")
MY_NO = "9767981986"

CAR_MODELS = {
    "Balaji Go 🚗": 13,
    "Balaji Sedan 🚙": 17,
    "Balaji SUV 🚐": 22
}

# --- २. मल्टिपल लँग्वेज डिक्शनरी ---
T = {
    "English": {
        "title": "BALAJI LOGISTICS 📦", "name": "Full Name", "num": "Mobile Number", "start": "Get Started",
        "from": "📍 Pick-up Point", "to": "🏁 Drop Point", "km": "📏 Total KM",
        "select": "🚗 Select Ride", "pay": "💳 Payment Mode", "book": "Confirm Booking",
        "home": "🏠 Home", "act": "🕒 Activity", "prof": "👤 Profile", "online": "Online", "cash": "Cash",
        "share_loc": "📍 Share My Live Location", "login": "Login", "reg": "Register", "lang_sel": "Choose Language"
    },
    "Marathi": {
        "title": "बालाजी लॉजिस्टिक्स 📦", "name": "तुमचे पूर्ण नाव", "num": "मोबाईल नंबर", "start": "सुरू करा",
        "from": "📍 पिक-अप पॉईंट", "to": "🏁 कुठे जायचे?", "km": "📏 एकूण किलोमीटर",
        "select": "🚗 गाडी निवडा", "pay": "💳 पेमेंट पद्धत", "book": "बुकिंग कन्फर्म करा",
        "home": "🏠 होम", "act": "🕒 हिस्ट्री", "prof": "👤 प्रोफाइल", "online": "ऑनलाईन", "cash": "रोख",
        "share_loc": "📍 माझे लाईव्ह लोकेशन पाठवा", "login": "लॉगिन", "reg": "नोंदणी", "lang_sel": "भाषा निवडा"
    },
    "Hindi": {
        "title": "बालाजी लॉजिस्टिक्स 📦", "name": "आपका नाम", "num": "मोबाइल नंबर", "start": "शुरू करें",
        "from": "📍 पिक-अप पॉइंट", "to": "🏁 कहाँ जाना है?", "km": "📏 कुल किलोमीटर",
        "select": "🚗 गाड़ी चुनें", "pay": "💳 पेमेंट का तरीका", "book": "बुकिंग कन्फर्म करें",
        "home": "🏠 होम", "act": "🕒 हिस्ट्री", "prof": "👤 प्रोफाइल", "online": "ऑनलाइन", "cash": "नकद",
        "share_loc": "📍 मेरा लाइव लोकेशन भेजें", "login": "लॉगिन", "reg": "रजिस्ट्रेशन", "lang_sel": "भाषा चुनें"
    }
}

# Session States
if "lang" not in st.session_state: st.session_state.lang = "English"
if "auth" not in st.session_state: st.session_state.auth = False
if "pg" not in st.session_state: st.session_state.pg = "Home"
if "hist" not in st.session_state: st.session_state.hist = []

L = T[st.session_state.lang]

# ३. स्टाईलिंग (Professional Black & Gold Theme)
st.markdown(f"""
<style>
.main-header {{background: linear-gradient(90deg, #000 0%, #333 100%); color:#FFD700; padding:25px; text-align:center; border-radius:0 0 25px 25px; margin-top:-60px; font-family: 'Arial Black'; box-shadow: 0px 4px 10px rgba(0,0,0,0.3);}}
.card {{background:#ffffff; padding:15px; border-radius:15px; border:1px solid #eee; margin-bottom:10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.05);}}
.btn-wa {{display:block; background:#25D366; color:white !important; text-align:center; padding:12px; border-radius:10px; text-decoration:none; font-weight:bold; margin-bottom:10px;}}
.btn-pay {{display:block; background:#5A2D82; color:white !important; text-align:center; padding:12px; border-radius:10px; text-decoration:none; font-weight:bold;}}
.btn-loc {{display:block; background:#4285F4; color:white !important; text-align:center; padding:12px; border-radius:10px; text-decoration:none; font-weight:bold; margin-bottom:10px;}}
.stButton>button {{width:100%; border-radius:10px; background-color: #000; color: #fff; height: 45px;}}
</style>
""", unsafe_allow_html=True)

# ४. भाषा निवड (Starting Option)
if not st.session_state.auth:
    st.session_state.lang = st.selectbox(f"🌐 {L['lang_sel']}", list(T.keys()))
    L = T[st.session_state.lang] # Update dictionary instantly

# ५. लॉगिन / रजिस्ट्रेशन
if not st.session_state.auth:
    st.markdown(f'<div class="main-header"><h1>{L["title"]}</h1></div><br>', unsafe_allow_html=True)
    
    auth_choice = st.radio("Option", [L["reg"], L["login"]], horizontal=True)

    if auth_choice == L["reg"]:
        n = st.text_input(L["name"], key="reg_name")
        p = st.text_input(L["num"], max_chars=10, key="reg_num")
        if st.button(L["start"]):
            if n and len(p) == 10: 
                st.session_state.u = {"n": n, "p": p}
                st.session_state.auth = True
                st.rerun()
    else:
        p_login = st.text_input(L["num"], max_chars=10, key="login_num")
        if st.button(L["login"] + " ➔"):
            if len(p_login) == 10:
                st.session_state.u = {"n": "User", "p": p_login}
                st.session_state.auth = True
                st.rerun()

else:
    # --- ६. होम पेज ---
    if st.session_state.pg == "Home":
        st.markdown(f"#### Welcome, {st.session_state.u['n']}! 👋")
        
        # Map
        m = folium.Map(location=[19.9975, 73.7898], zoom_start=13)
        st_folium(m, height=180, width=700, key="nashik_map")

        # Live Location
        loc_msg = urllib.parse.quote(f"Hi, I am {st.session_state.u['n']} ({st.session_state.u['p']}). This is my live pick-up location.")
        st.markdown(f'<a href="https://wa.me/{MY_NO}?text={loc_msg}" class="btn-loc">{L["share_loc"]}</a>', unsafe_allow_html=True)

        # Booking Form
        src = st.text_input(L["from"])
        dst = st.text_input(L["to"])
        km_val = st.number_input(L["km"], min_value=1.0, value=10.0)
        car_choice = st.radio("Fleet", list(CAR_MODELS.keys()), horizontal=True)
        total_fare = km_val * CAR_MODELS[car_choice]
        st.subheader(f"Estimated Fare: ₹{total_fare}")
        p_mode = st.radio(L["pay"], [L["cash"], L["online"]])

        if st.button(L["book"]):
            if src and dst:
                st.session_state.rd = {"s": src, "d": dst, "km": km_val, "f": total_fare, "c": car_choice, "pm": p_mode}
                st.session_state.pg = "Process"
                st.rerun()

    # --- ७. प्रोसेस पेज ---
    elif st.session_state.pg == "Process":
        r = st.session_state.rd
        st.success("✅ Order Details Saved!")
        
        msg_text = f"🚕 *BALAJI LOGISTICS BOOKING*\n👤 Name: {st.session_state.u['n']}\n📞 Contact: {st.session_state.u['p']}\n📍 Pick: {r['s']}\n🏁 Drop: {r['d']}\n📏 {r['km']} KM\n🚗 {r['c']}\n💰 *Fare: ₹{r['f']}*\n💳 Payment: {r['pm']}"
        encoded_msg = urllib.parse.quote(msg_text)

        st.markdown(f'<a href="https://wa.me/{MY_NO}?text={encoded_msg}" class="btn-wa">Send WhatsApp Request 💬</a>', unsafe_allow_html=True)

        if r["pm"] in ["Online", "ऑनलाईन", "ऑनलाइन"]:
            upi_url = f"upi://pay?pa={MY_NO}@ybl&pn=Balaji&am={r['f']}&cu=INR"
            st.markdown(f'<a href="{upi_url}" class="btn-pay">Pay via UPI (PhonePe/GPay) 💳</a>', unsafe_allow_html=True)

        if st.button("Main Menu"): 
            st.session_state.hist.append(r)
            st.session_state.pg = "Home"
            st.rerun()

    # --- ८. हिस्ट्री ---
    elif st.session_state.pg == "Activity":
        st.header(L["act"])
        for h in reversed(st.session_state.hist):
            st.markdown(f'<div class="card"><b>{h["s"]} ➔ {h["d"]}</b><br>Fare: ₹{h["f"]} | Vehicle: {h["c"]}</div>', unsafe_allow_html=True)

    # नेव्हिगेशन बार
    st.markdown("<br><hr>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button(L["home"]): st.session_state.pg = "Home"; st.rerun()
    if c2.button(L["act"]): st.session_state.pg = "Activity"; st.rerun()
    if c3.button("Logout"): 
        st.session_state.auth = False
        st.rerun()