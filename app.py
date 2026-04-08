import streamlit as st
import urllib.parse, folium
from streamlit_folium import st_folium

# १. मुख्य सेटिंग्ज आणि दर (Rates per KM)
st.set_page_config(page_title="Balaji Logistics", layout="centered", page_icon="🚕")
MY_NO = "9767981986"

# कारचे प्रकार आणि त्यांचे दर
CAR_MODELS = {
    "Balaji Go 🚗": 13,
    "Balaji Sedan 🚙": 17,
    "Balaji SUV 🚐": 22
}

# २. मेमरी (Session State) सेट करणे
if "lang" not in st.session_state:
    st.session_state.lang = "Marathi"
if "auth" not in st.session_state:
    st.session_state.auth = False
    st.session_state.pg = "Home"
    st.session_state.hist = []

# ३. शब्दकोश (Marathi & English)
T = {
    "Marathi": {
        "title": "बालाजी लॉजिस्टिक्स", "name": "तुमचे नाव", "num": "मोबाईल नंबर", "start": "सुरू करा",
        "from": "📍 कुठून? (Pick-up)", "to": "🏁 कुठे? (Drop)", "km": "📏 एकूण किलोमीटर",
        "select": "🚗 गाडी निवडा", "pay": "💳 पेमेंट पद्धत निवडा", "book": "बुकिंग कन्फर्म करा",
        "home": "🏠 होम", "act": "🕒 हिस्ट्री", "prof": "👤 प्रोफाइल", "online": "ऑनलाईन (PhonePe/GPay)", "cash": "रोख (Cash)",
        "msg_head": "नवीन बुकिंग माहिती"
    },
    "English": {
        "title": "Balaji Logistics", "name": "Your Name", "num": "Mobile Number", "start": "Get Started",
        "from": "📍 From (Pick-up)", "to": "🏁 To (Drop)", "km": "📏 Total KM",
        "select": "🚗 Select Your Ride", "pay": "💳 Select Payment Mode", "book": "Confirm Booking",
        "home": "🏠 Home", "act": "🕒 Activity", "prof": "👤 Profile", "online": "Online (PhonePe/GPay)", "cash": "Cash to Driver",
        "msg_head": "New Booking Details"
    }
}
L = T[st.session_state.lang]

# ४. डिझाइन (CSS)
st.markdown(f"""
<style>
    .main-header {{background:#000; color:#fff; padding:20px; text-align:center; border-radius:0 0 20px 20px; margin-top:-65px;}}
    .card {{background:#f8f9fa; padding:15px; border-radius:15px; border:1px solid #ddd; margin-bottom:10px;}}
    .btn-wa {{display:block; background:#25D366; color:white !important; text-align:center; padding:12px; border-radius:10px; text-decoration:none; font-weight:bold; margin-bottom:10px;}}
    .btn-pay {{display:block; background:#5A2D82; color:white !important; text-align:center; padding:12px; border-radius:10px; text-decoration:none; font-weight:bold;}}
    .stButton>button {{width:100%; border-radius:10px;}}
</style>
""", unsafe_allow_html=True)

# ५. भाषा निवड (Top Right)
col_l1, col_l2 = st.columns([3, 1])
with col_l2:
    st.session_state.lang = st.selectbox("🌐 Language", ["Marathi", "English"])

# ६. रजिस्ट्रेशन स्क्रीन
if not st.session_state.auth:
    st.markdown(f'<div class="main-header"><h1>{L["title"]}</h1></div>', unsafe_allow_html=True)
    n = st.text_input(L["name"])
    p = st.text_input(L["num"], max_chars=10)
    if st.button(L["start"]):
        if n and len(p) == 10:
            st.session_state.u = {"n": n, "p": p}
            st.session_state.auth = True
            st.rerun()

else:
    # --- होम पेज ---
    if st.session_state.pg == "Home":
        st.markdown(f"#### Hello, {st.session_state.u['n']}! 👋")
        
        # मॅप
        m = folium.Map(location=[19.9975, 73.7898], zoom_start=13)
        st_folium(m, height=200, width=700, key="nashik_map")
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        src = st.text_input(L["from"], placeholder="उदा. सातपूर")
        dst = st.text_input(L["to"], placeholder="उदा. नाशिक रोड स्टेशन")
        km_val = st.number_input(L["km"], min_value=1.0, value=10.0, step=0.5)
        
        st.write(f"### {L['select']}:")
        car_choice = st.radio("Cars", list(CAR_MODELS.keys()), label_visibility="collapsed")
        
        total_price = km_val * CAR_MODELS[car_choice]
        st.subheader(f"Total Fare: ₹{total_price} /-")
        
        pay_choice = st.radio(L["pay"], [L["cash"], L["online"]])
        
        if st.button(L["book"]):
            if src and dst:
                st.session_state.rd = {"s": src, "d": dst, "km": km_val, "f": total_price, "c": car_choice, "pm": pay_choice}
                st.session_state.pg = "Process"; st.rerun()
            else:
                st.error("कृपया दोन्ही ठिकाणे टाका!")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- बुकिंग प्रोसेस (Payment & WhatsApp) ---
    elif st.session_state.pg == "Process":
        r = st.session_state.rd
        st.success("✅ Booking Details Ready!")
        
        # मेसेज तयार करणे
        msg_text = f"🚕 *{L['msg_head']}*\n👤 नाव: {st.session_state.u['n']}\n📍 Pick: {r['s']}\n🏁 Drop: {r['d']}\n📏 अंतर: {r['km']} KM\n🚗 गाडी: {r['c']}\n💰 *एकूण भाडे: ₹{r['f']}*\n💳 पेमेंट: {r['pm']}"
        encoded_msg = urllib.parse.quote(msg_text)
        
        st.markdown(f'<a href="https://wa.me/91{MY_NO}?text={encoded_msg}" target="_blank" class="btn-wa">WhatsApp वर बुकिंग पाठवा 💬</a>', unsafe_allow_html=True)
        
        if r["pm"] in ["Online (PhonePe/GPay)", "ऑनलाईन (PhonePe/GPay)"]:
            upi_link = f"upi://pay?pa={MY_NO}@ybl&pn=Balaji%20Logistics&am={r['f']}&cu=INR"
            st.markdown(f'<a href="{upi_link}" class="btn-pay">PhonePe / GPay ने पैसे भरा 💳</a>', unsafe_allow_html=True)
            st.write(f"Direct No: **{MY_NO}**")

        if st.button("Main Menu"): 
            st.session_state.hist.append(r)
            st.session_state.pg = "Home"; st.rerun()

    # --- हिस्ट्री ---
    elif st.session_state.pg == "Activity":
        st.header(L["act"])
        for h in reversed(st.session_state.hist):
            st.markdown(f"<div class='card'><b>{h['s']} ➔ {h['d']}</b><br>₹{h['f']} | {h['c']}</div>", unsafe_allow_html=True)

    # --- नेव्हिगेशन बार ---
    st.markdown("<br><hr>", unsafe_allow_html=True)
    n1, n2, n3 = st.columns(3)
    if n1.button(L["home"]): st.session_state.pg = "Home"; st.rerun()
    if n2.button(L["act"]): st.session_state.pg = "Activity"; st.rerun()
    if n3.button(L["prof"]): 
        st.write(f"User: {st.session_state.u['n']}")
        if st.button("Logout"): st.session_state.auth = False; st.rerun()