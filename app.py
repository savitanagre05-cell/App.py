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
        "fare": "Total Fare", "pay": "Payment Mode", "book_btn": "Confirm Booking", "logout