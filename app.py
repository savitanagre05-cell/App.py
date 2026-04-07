import streamlit as st

# १. अ‍ॅप सेटिंग्स (Mobile Optimized)
st.set_page_config(page_title="Balaji Logistics", page_icon="🚕", layout="wide")

# २. स्टेट मॅनेजमेंट (User Session & Language)
if "lang" not in st.session_state: st.session_state.lang = "मराठी"
if "is_auth" not in st.session_state: st.session_state.is_auth = False
if "page" not in st.session_state: st.session_state.page = "🏠 Home"
if "auth_mode" not in st.session_state: st.session_state.auth_mode = "Login"
if "user_name" not in st.session_state: st.session_state.user_name = "Customer"

# ३. शब्दकोश (Multi-language Dictionary)
texts = {
    "मराठी": {
        "login": "Login", "reg": "Register", "name": "पूर्ण नाव",
        "phone": "मोबाईल नंबर", "p_name": "उदा. अमित पाटील", "p_phone": "उदा. 9822xxxxxx",
        "from": "कुठून? (Pickup)", "to": "कुठे? (Drop)", "car": "गाडी निवडा", "km": "अंदाजित किमी", 
        "fare": "एकूण भाडे", "pay": "पेमेंट पद्धत", "book_btn": "Confirm Booking", "logout": "Logout"
    },
    "English": {
        "login": "Login", "reg": "Register", "name": "Full Name",
        "phone": "Mobile Number", "p_name": "e.g. Amit Patil", "p_phone": "e.g. 9822xxxxxx",
        "from": "From (Pickup)", "to": "To (Drop)", "car": "Select Car", "km": "Estimated KM", 
        "fare": "Total Fare", "pay": "Payment Mode", "book_btn": "Confirm Booking", "logout": "Logout"
    },
    "Hindi": {
        "login": "Login", "reg": "Register", "name": "पूरा नाम",
        "phone": "मोबाइल नंबर", "p_name": "जैसे: अमित पाटिल", "p_phone": "जैसे: 9822xxxxxx",
        "from": "कहाँ से?", "to": "कहाँ तक?", "car": "गाड़ी चुनें", "km": "अनुमानित किमी", 
        "fare": "कुल किराया", "pay": "पेमेंट मोड", "book_btn": "Confirm Booking", "logout": "Logout"
    }
}

T = texts[st.session_state.lang]
MY_NUMBER = "9767981986"
MY_UPI_ID = "9767981986@ybl"

# ४. हाय-व्हिजिबिलिटी CSS (Fixes Visibility & Syntax Errors)
css_code = """
<style>
    .stApp { background-color: #FFFFFF !important; }
    .app-header { 
        background-color: #000000; 
        color: #FFFFFF !important; 
        padding: 25px; 
        text-align: center; 
        font-size: 28px; 
        font-weight: bold; 
        border-radius: 0 0 25px 25px; 
        margin-bottom: 20px;
    }
    /* सर्व बटन्ससाठी काळा रंग */
    .stButton>button {
        width: 100%;
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border-radius: 15px !important;
        height: 55px;
        font-weight: bold !important;
        border: none !important;
    }
    /* मजकूर स्पष्ट दिसण्यासाठी */
    label, p, h1, h2, h3, span { color: #000000 !important; font-weight: bold !important; }
    
    /* इनपुट बॉक्सची काळी बॉर्डर */
    div[data-baseweb="input"] { 
        border: 2px solid #000000 !important; 
        border-radius: 12px !important; 
        background-color: #F9F9F9 !important;
    }
    input { color: #000000 !important; }
</style>
"""
st.markdown(css_code, unsafe_allow_html=True)

# ५. ऑथेंटिकेशन (Login & Registration)
if not st.session_state.is_auth:
    st.markdown("<div class='app-header'>🚕 Balaji Logistics</div>", unsafe_allow_html=True)
    
    # टॅब ऐवजी साधे मोठे बटन्स
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"🔑 {T['login']}"): 
            st.session_state.auth_mode = "Login"
            st.rerun()
    with col2:
        if st.button(f"📝 {T['reg']}"): 
            st.session_state.auth_mode = "Register"
            st.rerun()

    st.write("---")

    if st.session_state.auth_mode == "Login":
        st.markdown(f"### {T['login']}")
        l_p = st.text_input(T['phone'], placeholder=T['p_phone'], key="l_phone_in")
        if st.button("🚀 GO"):
            if len(l_p) == 10:
                st.session_state.user_name = "Customer"
                st.session_state.is_auth = True
                st.session_state.page = "🏠 Home"
                st.rerun()
            else: st.error("१० अंकी नंबर टाका.")

    else:
        st.markdown(f"### {T['reg']}")
        r_n = st.text_input(T['name'], placeholder=T['p_name'], key="r_name_in")
        r_p = st.text_input(T['phone'], placeholder=T['p_phone'], key="r_phone_in")
        if st.button("✅ CREATE ACCOUNT"):
            if r_n and len(r_p) == 10:
                st.session_state.user_name = r_n
                st.session_state.is_auth = True
                st.session_state.page = "🏠 Home"
                # WhatsApp Notification
                wa_msg = f"👤 *New Registration*\nName: {r_n}\nPhone: {r_p}"
                wa_url = f"https://wa.me/91{MY_NUMBER}?text={wa_msg.replace(' ', '%20')}"
                st.markdown(f'<meta http-equiv="refresh" content="0;URL={wa_url}">', unsafe_allow_html=True)
                st.rerun()
            else: st.error("सर्व माहिती अचूक भरा.")
    st.stop()

# ६. मुख्य अ‍ॅप (Login नंतर)
st.markdown("<div class='app-header'>Balaji Logistics</div>", unsafe_allow_html=True)

# --- HOME PAGE ---
if st.session_state.page == "🏠 Home":
    st.markdown(f"### नमस्कार, {st.session_state.user_name}! 👋")
    st.image("https://images.unsplash.com/photo-1559297434-2d8a1e02a01d?auto=format&fit=crop&w=800")
    if st.button("Book Ride Now ➔"): 
        st.session_state.page = "🚕 Book"
        st.rerun()

# --- BOOKING PAGE ---
elif st.session_state.page == "🚕 Book":
    st.markdown("### 📍 Book Your Ride")
    p_up = st.text_input(T['from'], placeholder="उदा. नाशिक रोड")
    d_off = st.text_input(T['to'], placeholder="उदा. त्र्यंबकेश्वर")
    car = st.selectbox(T['car'], ["🚗 Mini (₹11/km)", "🚖 Sedan (₹14/km)", "🚐 SUV (₹17/km)"])
    km = st.number_input(T['km'], min_value=1, value=10)
    
    rate = 11 if "Mini" in car else (14 if "Sedan" in car else 17)
    total = km * rate
    st.info(f"💰 {T['fare']}: ₹{total}")
    
    pay = st.radio(T['pay'], ["Cash", "PhonePe"], horizontal=True)
    if pay == "PhonePe":
        upi_link = f"upi://pay?pa={MY_UPI_ID}&pn=BalajiLogistics&am={total}&cu=INR"
        st.markdown(f"#### [💸 Pay ₹{total} via PhonePe]({upi_link})")

    if st.button(T['book_btn']):
        book_msg = f"🚩 *New Booking*\nName: {st.session_state.user_name}\nFrom: {p_up}\nTo: {d_off}\nTotal: ₹{total}"
        st.markdown(f"[📲 Send to WhatsApp](https://wa.me/91{MY_NUMBER}?text={book_msg.replace(' ', '%20')})")

# --- SETTINGS PAGE ---
elif st.session_state.page == "⚙️ Settings":
    st.markdown("### ⚙️ Settings")
    new_lang = st.selectbox("Language", ["मराठी", "English", "Hindi"], index=["मराठी", "English", "Hindi"].index(st.session_state.lang))
    if new_lang != st.session_state.lang:
        st.session_state.lang = new_lang
        st.rerun()
    st.write("---")
    if st.button(T['logout']):
        st.session_state.is_auth = False
        st.rerun()

# ७. बॉटम नेव्हिगेशन (Bottom Navigation Bar)
st.write("<br><br><br>", unsafe_allow_html=True)
n1, n2, n3 = st.columns(3)
with n1:
    if st.button("🏠"): st.session_state.page = "🏠 Home"; st.rerun()
with n2:
    if st.button("🚕"): st.session_state.page = "🚕 Book"; st.rerun()
with n3:
    if st.button("⚙️"): st.session_state.page = "⚙️ Settings"; st.rerun()
