Thik aahe, ha ghey **"Login"** ani **Register"** donhi options aslela purna ani final code. Mi hyaat navigation logic agdi vyavasthit lavli aahe, jyamule tula pahije tasa "Next-Next" flow milel.
```python
import streamlit as st
import urllib.parse, folium
from streamlit_folium import st_folium

# १. मुख्य सेटिंग्ज
st.set_page_config(page_title="Balaji Logistics", layout="centered", page_icon="🚕")
MY_NO = "9767981986"

CAR_MODELS = {
    "Balaji Go 🚗": 13,
    "Balaji Sedan 🚙": 17,
    "Balaji SUV 🚐": 22
}

# Session State Initialization
if "lang" not in st.session_state: st.session_state.lang = "Marathi"
if "auth" not in st.session_state: st.session_state.auth = False
if "auth_mode" not in st.session_state: st.session_state.auth_mode = None
if "pg" not in st.session_state: st.session_state.pg = "Home"
if "hist" not in st.session_state: st.session_state.hist = []

# २. शब्दकोश (Marathi & English)
T = {
    "Marathi": {
        "title": "बालाजी लॉजिस्टिक्स", "name": "तुमचे नाव", "num": "मोबाईल नंबर", "start": "सुरू करा",
        "from": "📍 पिक-अप पॉईंट", "to": "🏁 कुठे जायचे?", "km": "📏 एकूण किलोमीटर",
        "select": "🚗 गाडी निवडा", "pay": "💳 पेमेंट पद्धत", "book": "बुकिंग कन्फर्म करा",
        "home": "🏠 होम", "act": "🕒 हिस्ट्री", "prof": "👤 प्रोफाइल", "online": "ऑनलाईन", "cash": "रोख",
        "share_loc": "📍 माझे लाईव्ह लोकेशन पाठवा", "login": "लॉगिन", "reg": "रजिस्ट्रेशन"
    },
    "English": {
        "title": "Balaji Logistics", "name": "Your Name", "num": "Mobile Number", "start": "Start",
        "from": "📍 Pick-up Point", "to": "🏁 Drop Point", "km": "📏 Total KM",
        "select": "🚗 Select Ride", "pay": "💳 Payment Mode", "book": "Confirm Booking",
        "home": "🏠 Home", "act": "🕒 Activity", "prof": "👤 Profile", "online": "Online", "cash": "Cash",
        "share_loc": "📍 Share My Live Location", "login": "Login", "reg": "Registration"
    }
}
L = T[st.session_state.lang]

# ३. स्टाईलिंग (CSS)
st.markdown(f"""
<style>
    .main-header {{background:#000; color:#fff; padding:20px; text-align:center; border-radius:0 0 20px 20px; margin-top:-60px;}}
    .card {{background:#f8f9fa; padding:15px; border-radius:15px; border:1px solid #ddd; margin-bottom:10px;}}
    .btn-wa {{display:block; background:#25D366; color:white !important; text-align:center; padding:12px; border-radius:10px; text-decoration:none; font-weight:bold; margin-bottom:10px;}}
    .btn-pay {{display:block; background:#5A2D82; color:white !important; text-align:center; padding:12px; border-radius:10px; text-decoration:none; font-weight:bold;}}
    .btn-loc {{display:block; background:#4285F4; color:white !important; text-align:center; padding:12px; border-radius:10px; text-decoration:none; font-weight:bold; margin-bottom:10px;}}
    .stButton>button {{width:100%; border-radius:10px;}}
</style>
""", unsafe_allow_html=True)

# ४. टॉप बार (भाषा निवड)
st.session_state.lang = st.selectbox("🌐 Language", ["Marathi", "English"])

# ५. लॉगिन / रजिस्ट्रेशन सेक्शन
if not st.session_state.auth:
    st.markdown(f'<div class="main-header"><h1>{L["title"]}</h1></div><br>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    if col1.button(L["login"] + " 🔑"): st.session_state.auth_mode = "Login"
    if col2.button(L["reg"] + " 📝"): st.session_state.auth_mode = "Register"

    if st.session_state.auth_mode == "Login":
        st.subheader(L["login"])
        p = st.text_input(L["num"], max_chars=10)
        if st.button("➔ Enter"):
            if len(p) == 10:
                st.session_state.u = {"n": "User", "p": p} # इथे नाव डेटाबेसमधून येऊ शकते
                st.session_state.auth = True
                st.rerun()
            else: st.error("Invalid Number")

    elif st.session_state.auth_mode == "Register":
        st.subheader(L["reg"])
        n = st.text_input(L["name"])
        p = st.text_input(L["num"], max_chars=10)
        if st.button(L["start"] + " ➔"):
            if n and len(p) == 10:
                st.session_state.u = {"n": n, "p": p}
                st.session_state.auth = True
                st.rerun()
            else: st.warning("Please fill all details")

else:
    # --- ६. होम पेज (Input) ---
    if st.session_state.pg == "Home":
        st.markdown(f"#### Hello, {st.session_state.u['n']}! 👋")
        
        # नकाशा
        m = folium.Map(location=[19.9975, 73.7898], zoom_start=13)
        st_folium(m, height=180, width=700, key="nashik_map")

        # लाईव्ह लोकेशन शेअर
        loc_msg = urllib.parse.quote(f"नमस्कार, मी {st.session_state.u['n']} बोलतोय ({st.session_state.u['p']}). हे माझे लाईव्ह पिक-अप लोकेशन आहे.")
        st.markdown(f'<a href="https://wa.me/{MY_NO}?text={loc_msg}" class="btn-loc">{L["share_loc"]}</a>', unsafe_allow_html=True)

        # बुकिंग फॉर्म
        src = st.text_input(L["from"])
        dst = st.text_input(L["to"])
        km_val = st.number_input(L["km"], min_value=1.0, value=10.0)
        car_choice = st.radio("Cars", list(CAR_MODELS.keys()), horizontal=True)
        total_fare = km_val * CAR_MODELS[car_choice]
        st.subheader(f"Fare: ₹{total_fare}")
        p_mode = st.radio(L["pay"], [L["cash"], L["online"]])

        if st.button(L["book"]):
            if src and dst:
                st.session_state.rd = {"s": src, "d": dst, "km": km_val, "f": total_fare, "c": car_choice, "pm": p_mode}
                st.session_state.pg = "Process"
                st.rerun()

    # --- ७. प्रोसेस पेज (Confirmation) ---
    elif st.session_state.pg == "Process":
        r = st.session_state.rd
        st.success("✅ Details Saved!")
        
        msg_text = f"🚕 *BALAJI BOOKING*\n👤 नाव: {st.session_state.u['n']}\n📞 नंबर: {st.session_state.u['p']}\n📍 Pick: {r['s']}\n🏁 Drop: {r['d']}\n📏 {r['km']} KM\n🚗 {r['c']}\n💰 *भाडे: ₹{r['f']}*\n💳 {r['pm']}"
        encoded_msg = urllib.parse.quote(msg_text)

        st.markdown(f'<a href="https://wa.me/{MY_NO}?text={encoded_msg}" class="btn-wa">WhatsApp मेसेज पाठवा 💬</a>', unsafe_allow_html=True)

        if r["pm"] in ["Online", "ऑनलाईन"]:
            upi_url = f"upi://pay?pa={MY_NO}@ybl&pn=Balaji&am={r['f']}&cu=INR"
            st.markdown(f'<a href="{upi_url}" class="btn-pay">PhonePe / GPay ने पैसे भरा 💳</a>', unsafe_allow_html=True)

        if st.button("Back to Main Menu"): 
            st.session_state.hist.append(r)
            st.session_state.pg = "Home"
            st.rerun()

    # --- ८. हिस्ट्री पेज ---
    elif st.session_state.pg == "Activity":
        st.header(L["act"])
        for h in reversed(st.session_state.hist):
            st.markdown(f'<div class="card">{h["s"]} ➔ {h["d"]}<br><b>₹{h["f"]}</b> | {h["c"]}</div>', unsafe_allow_html=True)

    # --- ९. नेव्हिगेशन बार ---
    st.markdown("<br><hr>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button(L["home"]): st.session_state.pg = "Home"; st.rerun()
    if c2.button(L["act"]): st.session_state.pg = "Activity"; st.rerun()
    if c3.button("Logout"): 
        st.session_state.auth = False
        st.session_state.auth_mode = None
        st.rerun()

```
