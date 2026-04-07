import streamlit as st

# १. अ‍ॅप सेटिंग्स
st.set_page_config(page_title="Balaji Logistics", page_icon="🚕", layout="wide")

# २. स्टेट मॅनेजमेंट (भाषा, ऑथेंटिकेशन आणि पेज ट्रॅकिंग)
if "lang" not in st.session_state: st.session_state.lang = "मराठी"
if "is_auth" not in st.session_state: st.session_state.is_auth = False
if "page" not in st.session_state: st.session_state.page = "🏠 Home"
if "user_name" not in st.session_state: st.session_state.user_name = ""

# ३. मल्टी-लँग्वेज डिक्शनरी
texts = {
    "मराठी": {
        "header": "बाळाजी लॉजिस्टिक", "login": "लॉगिन", "reg": "नोंदणी", "name": "पूर्ण नाव",
        "phone": "मोबाईल नंबर", "p_name": "उदा. अमित पाटील", "p_phone": "उदा. 9822xxxxxx",
        "from": "कुठून? (Pickup)", "to": "कुठे? (Drop)", "p_from": "उदा. नाशिक रोड",
        "p_to": "उदा. त्र्यंबकेश्वर", "car": "गाडी निवडा", "km": "अंदाजित किमी", "fare": "एकूण भाडे",
        "pay": "पेमेंट पद्धत", "book_btn": "बुकिंग कन्फर्म करा", "lang_sel": "भाषा निवडा", "logout": "लॉगआउट"
    },
    "English": {
        "header": "Balaji Logistics", "login": "Login", "reg": "Register", "name": "Full Name",
        "phone": "Mobile Number", "p_name": "e.g. Amit Patil", "p_phone": "e.g. 9822xxxxxx",
        "from": "From (Pickup)", "to": "To (Drop)", "p_from": "e.g. Nashik Road",
        "p_to": "e.g. Trimbakeshwar", "car": "Select Car", "km": "Estimated KM", "fare": "Total Fare",
        "pay": "Payment Mode", "book_btn": "Confirm Booking", "lang_sel": "Select Language", "logout": "Logout"
    },
    "Hindi": {
        "header": "बालाजी लॉजिस्टिक", "login": "लॉगिन", "reg": "पंजीकरण", "name": "पूरा नाम",
        "phone": "मोबाइल नंबर", "p_name": "जैसे: अमित पाटिल", "p_phone": "जैसे: 9822xxxxxx",
        "from": "कहाँ से? (Pickup)", "to": "कहाँ तक? (Drop)", "p_from": "जैसे: नाशिक रोड",
        "p_to": "जैसे: त्र्यंबकेश्वर", "car": "गाड़ी चुनें", "km": "अनुमानित किमी", "fare": "कुल किराया",
        "pay": "पेमेंट का तरीका", "book_btn": "बुकिंग कन्फर्म करें", "lang_sel": "भाषा चुनें", "logout": "लॉगआउट"
    }
}

T = texts[st.session_state.lang]
MY_NUMBER = "9767981986"
MY_UPI_ID = "9767981986@ybl"

# ४. प्रोफेशनल CSS
st.markdown(f"""
    <style>
    .stApp {{ background-color: #F8F9FA; }}
    .app-header {{ background-color: black; color: white; padding: 15px; text-align: center; font-size: 22px; font-weight: bold; border-radius: 0 0 15px 15px; margin-bottom: 20px; }}
    .app-card {{ background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #eee; margin-bottom: 15px; }}
    .stButton>button {{ width: 100%; background-color: black; color: white; border-radius: 12px; height: 50px; font-weight: bold; border: none; }}
    .price-box {{ background-color: #E3F2FD; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #90CAF9; color: #1565C0; font-size: 20px; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

# ५. ऑथेंटिकेशन (Login/Register)
if not st.session_state.is_auth:
    st.markdown(f"<div class='app-header'>🚕 {T['header']}</div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs([T['login'], T['reg']])
    
    with tab1:
        st.markdown("<div class='app-card'>", unsafe_allow_html=True)
        l_p = st.text_input(T['phone'], placeholder=T['p_phone'], key="login_p")
        if st.button(T['login']):
            if len(l_p) == 10:
                st.session_state.user_name = "User"; st.session_state.user_phone = l_p
                st.session_state.is_auth = True; st.session_state.page = "🏠 Home"; st.rerun()
            else: st.error("10 digits required!")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<div class='app-card'>", unsafe_allow_html=True)
        r_n = st.text_input(T['name'], placeholder=T['p_name'], key="reg_n")
        r_p = st.text_input(T['phone'], placeholder=T['p_phone'], key="reg_p")
        if st.button(T['reg']):
            if r_n and len(r_p) == 10:
                st.session_state.user_name = r_n; st.session_state.user_phone = r_p
                st.session_state.is_auth = True; st.session_state.page = "🏠 Home"
                # WhatsApp Redirect Logic
                msg = f"👤 *NEW REGISTRATION*\nName: {r_n}\nPhone: {r_p}"
                wa_url = f"https://wa.me/91{MY_NUMBER}?text={msg.replace(' ', '%20')}"
                st.markdown(f'<meta http-equiv="refresh" content="0;URL={wa_url}">', unsafe_allow_html=True)
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ६. मुख्य अ‍ॅप पेजेस (Login नंतर)
st.markdown(f"<div class='app-header'>{T['header']}</div>", unsafe_allow_html=True)

# --- HOME ---
if st.session_state.page == "🏠 Home":
    st.subheader(f"👋 {st.session_state.user_name}")
    st.image("https://images.unsplash.com/photo-1559297434-2d8a1e02a01d?auto=format&fit=crop&w=800", use_container_width=True)
    if st.button("Ride Now ➔"): st.session_state.page = "🚕 Book"; st.rerun()

# --- BOOKING ---
elif st.session_state.page == "🚕 Book":
    st.markdown("<div class='app-card'>", unsafe_allow_html=True)
    p_up = st.text_input(T['from'], placeholder=T['p_from'])
    d_off = st.text_input(T['to'], placeholder=T['p_to'])
    car = st.selectbox(T['car'], ["🚗 Mini (₹11/km)", "🚖 Sedan (₹14/km)", "🚐 SUV (₹17/km)"])
    km = st.number_input(T['km'], min_value=1, value=10)
    
    rate = 11 if "Mini" in car else (14 if "Sedan" in car else 17)
    total = km * rate
    st.markdown(f"<div class='price-box'>{T['fare']}: ₹{total}</div>", unsafe_allow_html=True)
    
    st.write("---")
    pay = st.radio(T['pay'], ["Cash", "PhonePe"], horizontal=True)
    if pay == "PhonePe":
        st.info(f"PhonePe: {MY_NUMBER}")
        upi_url = f"upi://pay?pa={MY_UPI_ID}&pn=BalajiLogistics&am={total}&cu=INR"
        st.markdown(f"### [💸 Pay Now with PhonePe]({upi_url})")

    if st.button(T['book_btn']):
        b_msg = f"🚩 *NEW RIDE*\nName: {st.session_state.user_name}\nFrom: {p_up}\nTo: {d_off}\nCar: {car}\nTotal: ₹{total}\nPay: {pay}"
        st.markdown(f"[📲 Send Booking via WhatsApp](https://wa.me/91{MY_NUMBER}?text={b_msg.replace(' ', '%20').replace('\n', '%0A')})")
    st.markdown("</div>", unsafe_allow_html=True)

# --- SETTINGS ---
elif st.session_state.page == "⚙️ Settings":
    st.markdown("<div class='app-card'>", unsafe_allow_html=True)
    st.subheader(T['lang_sel'])
    new_lang = st.selectbox("", ["मराठी", "English", "Hindi"], index=["मराठी", "English", "Hindi"].index(st.session_state.lang))
    if new_lang != st.session_state.lang:
        st.session_state.lang = new_lang; st.rerun()
    st.write("---")
    if st.button(T['logout']): st.session_state.is_auth = False; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ७. बॉटम नेव्हिगेशन (नेहमी दिसेल)
st.write("<br><br><br><br>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🏠"): st.session_state.page = "🏠 Home"; st.rerun()
with c2:
    if st.button("🚕"): st.session_state.page = "🚕 Book"; st.rerun()
with c3:
    if st.button("⚙️"): st.session_state.page = "⚙️ Settings"; st.rerun() 