import streamlit as st
import urllib.parse, folium
from streamlit_folium import st_folium

# १. मुख्य सेटिंग्ज आणि तुझा नंबर
st.set_page_config(page_title="Balaji Logistics", layout="centered", page_icon="🚕")
MY_NO = "9767981986"

CAR_MODELS = {
    "Balaji Go 🚗": 13,
    "Balaji Sedan 🚙": 17,
    "Balaji SUV 🚐": 22
}

if "lang" not in st.session_state: st.session_state.lang = "Marathi"
if "auth" not in st.session_state:
    st.session_state.auth = False
    st.session_state.pg = "Home"
    st.session_state.hist = []

# २. शब्दकोश
T = {
    "Marathi": {
        "title": "BALAJI LOGISTICS", "name": "तुमचे नाव", "num": "मोबाईल नंबर", "start": "सुरू करा",
        "from": "📍 पिक-अप पॉईंट", "to": "🏁 कुठे जायचे?", "km": "📏 एकूण किलोमीटर",
        "select": "🚗 गाडी निवडा", "pay": "💳 पेमेंट पद्धत", "book": "बुकिंग कन्फर्म करा",
        "home": "🏠 होम", "act": "🕒 हिस्ट्री", "prof": "👤 प्रोफाइल", "online": "ऑनलाईन", "cash": "रोख",
        "share_loc": "📍 माझे लाईव्ह लोकेशन पाठवा", "logout": "लॉगआउट"
    },
    "English": {
        "title": "BALAJI LOGISTICS", "name": "Your Name", "num": "Mobile Number", "start": "Start",
        "from": "📍 Pick-up Point", "to": "🏁 Drop Point", "km": "📏 Total KM",
        "select": "🚗 Select Ride", "pay": "💳 Payment Mode", "book": "Confirm Booking",
        "home": "🏠 Home", "act": "🕒 Activity", "prof": "👤 Profile", "online": "Online", "cash": "Cash",
        "share_loc": "📍 Share My Live Location", "logout": "Logout"
    }
}
L = T[st.session_state.lang]

# ३. प्रीमियम स्टाईलिंग (Logo & UI)
st.markdown(f"""
<style>
    /* प्रीमियम लोगो डिझाइन (Gold & Black Theme) */
    .main-header {{
        background: linear-gradient(135deg, #000000 0%, #2c3e50 100%);
        color: #FFD700; /* Gold */
        padding: 40px; 
        text-align: center; 
        border-radius: 0 0 35px 35px; 
        margin-top: -65px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.4);
        border-bottom: 4px solid #FFD700;
    }}
    .main-title {{
        font-family: 'Georgia', serif; 
        letter-spacing: 3px; 
        font-weight: bold; 
        margin-bottom: 0; 
        font-size: 36px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }}
    .main-subtitle {{
        color: #fff; 
        font-size: 16px; 
        margin-top: 5px; 
        letter-spacing: 1px;
    }}
    .stApp {{
        background-color: #f4f7f6;
    }}
    .card {{background:#fff; padding:20px; border-radius:18px; border:1px solid #eee; margin-bottom:15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);}}
    .btn-wa {{display:block; background:#25D366; color:white !important; text-align:center; padding:14px; border-radius:12px; text-decoration:none; font-weight:bold; margin-bottom:12px; font-size: 16px;}}
    .btn-pay {{display:block; background:#5A2D82; color:white !important; text-align:center; padding:14px; border-radius:12px; text-decoration:none; font-weight:bold; font-size: 16px;}}
    .btn-loc {{display:block; background:#4285F4; color:white !important; text-align:center; padding:14px; border-radius:12px; text-decoration:none; font-weight:bold; margin-bottom:12px; font-size: 16px;}}
    .stButton>button {{width:100%; border-radius:12px; padding: 12px; font-weight:bold; font-size: 16px;}}
</style>
""", unsafe_allow_html=True)

# ४. भाषा निवड
st.session_state.lang = st.selectbox("🌐 Language", ["Marathi", "English"])

# ५. लॉगिन / रजिस्ट्रेशन (Updated Logo Only)
if not st.session_state.auth:
    st.markdown(f'''
    <div class="main-header">
        <div style="font-size:50px; margin-bottom: 10px;">🚕</div>
        <h1 class="main-title">{L["title"]}</h1>
        <p class="main-subtitle">Premium Travels & Express Rides</p>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    n = st.text_input(L["name"])
    p = st.text_input(L["num"], max_chars=10)
    if st.button(L["start"]):
        if n and len(p) == 10: st.session_state.u = {"n": n, "p": p}; st.session_state.auth = True; st.rerun()
else:
    # --- होम पेज ---
    if st.session_state.pg == "Home":
        st.markdown(f"#### Hello, {st.session_state.u['n']}! 👋")
        m = folium.Map(location=[19.9975, 73.7898], zoom_start=13)
        st_folium(m, height=180, width=700, key="nashik_map_super")
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        # लाईव्ह लोकेशन शेअर
        loc_msg = urllib.parse.quote(f"नमस्कार, मी {st.session_state.u['n']} बोलतोय ({st.session_state.u['p']}). माझे पिक-अप लोकेशन: http://googleusercontent.com/maps.google.com/3")
        st.markdown(f'<a href="https://wa.me/91{MY_NO}?text={loc_msg}" class="btn-loc">{L["share_loc"]}</a>', unsafe_allow_html=True)
        
        src = st.text_input(L["from"]); dst = st.text_input(L["to"])
        km_val = st.number_input(L["km"], min_value=1.0, value=10.0)
        car = st.radio("Cars", list(CAR_MODELS.keys()), horizontal=True)
        total = km_val * CAR_MODELS[car]
        st.subheader(f"Fare: ₹{total}"); mode = st.radio(L["pay"], [L["cash"], L["online"]])
        
        if st.button(L["book"]):
            if src and dst: st.session_state.rd = {"s":src,"d":dst,"km":km_val,"f":total,"c":car,"pm":mode}; st.session_state.pg="Process"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # --- बुकिंग प्रोसेस ---
    elif st.session_state.pg == "Process":
        r = st.session_state.rd
        st.success("✅ Booking Prepared!")
        msg = urllib.parse.quote(f"🚕 *BALAJI BOOKING*\n👤 नाव: {st.session_state.u['n']}\n📞 नंबर: {st.session_state.u['p']}\n📍 Pick: {r['s']}\n🏁 Drop: {r['d']}\n📏 {r['km']} KM\n🚗 {r['c']}\n💰 *भाडे: ₹{r['f']}*\n💳 {r['pm']}")
        st.markdown(f'<a href="https://wa.me/91{MY_NO}?text={msg}" target="_blank" class="btn-wa">WhatsApp मेसेज पाठवा 💬</a>', unsafe_allow_html=True)
        if r["pm"] in ["Online", "ऑनलाईन"]:
            upi = f"upi://pay?pa={MY_NO}@ybl&pn=Balaji&am={r['f']}&cu=INR"
            st.markdown(f'<a href="{upi}" class="btn-pay">PhonePe / GPay ने पैसे भरा 💳</a>', unsafe_allow_html=True)
        if st.button("Back to Home"): st.session_state.hist.append(r); st.session_state.pg="Home"; st.rerun()

    # --- हिस्ट्री ---
    elif st.session_state.pg == "Activity":
        st.header(L["act"])
        if not st.session_state.hist: st.write("No history.")
        for h in reversed(st.session_state.hist):
            st.markdown(f"<div class='card'><b>{h['s']} ➔ {h['d']}</b><br>₹{h['f']} | {h['c']}</div>", unsafe_allow_html=True)

    # --- प्रोफाइल ---
    elif st.session_state.pg == "Profile":
        st.header(L["prof"])
        st.write(f"👤 Name: **{st.session_state.u['n']}**")
        st.write(f"📞 Phone: **{st.session_state.u['p']}**")
        if st.button(L["logout"]): st.session_state.auth = False; st.rerun()

    # नेव्हिगेशन बार
    st.markdown("<br><hr>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button(L["home"]): st.session_state.pg="Home"; st.rerun()
    if c2.button(L["act"]): st.session_state.pg="Activity"; st.rerun()
    if c3.button(L["prof"]): st.session_state.pg="Profile"; st.rerun()