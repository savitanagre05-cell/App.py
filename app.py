import streamlit as st

# १. अ‍ॅप सेटिंग्स (Mobile Friendly)
st.set_page_config(page_title="Balaji Logistics", page_icon="🚕", layout="wide")

# २. स्टेट मॅनेजमेंट (User Session)
if "lang" not in st.session_state: st.session_state.lang = "मराठी"
if "is_auth" not in st.session_state: st.session_state.is_auth = False
if "page" not in st.session_state: st.session_state.page = "🏠 Home"
if "auth_mode" not in st.session_state: st.session_state.auth_mode = "Login"

# ३. शब्दकोश (Multi-language Support)
texts = {
    "मराठी": {
        "login": "Login", "reg": "Register", "name": "पूर्ण नाव",
        "phone": "मोबाईल नंबर", "p_name": "उदा. अमित पाटील", "p_phone": "उदा. 9822xxxxxx",
        "from": "कुठून? (Pickup)", "to": "कुठे? (Drop)", "car": "गाडी निवडा", "km": "अंदाजित किमी", 
        "fare": "एकूण भाडे", "pay": "पेमेंट पद्धत", "book_btn": "Confirm Booking"
    },
    "English": {
        "login": "Login", "reg": "Register", "name": "Full Name",
        "phone": "Mobile Number", "p_name": "e.g. Amit Patil", "p_phone": "e.g. 9822xxxxxx",
        "from": "From (Pickup)", "to": "To (Drop)", "car": "Select Car", "km": "Estimated KM", 
        "fare": "Total Fare", "pay": "Payment Mode", "book_btn": "Confirm Booking"
    },
    "Hindi": {
        "login": "Login", "reg": "Register", "name": "पूरा नाम",
        "phone": "मोबाइल नंबर", "p_name": "जैसे: अमित पाटिल", "p_phone": "जैसे: 9822xxxxxx",
        "from": "कहाँ से?", "to": "कहाँ तक?", "car": "गाड़ी चुनें", "km": "अनुमानित किमी", 
        "fare": "कुल किराया", "pay": "पेमेंट मोड", "book_btn": "Confirm Booking"
    }
}

T = texts[st.session_state.lang]
MY_NUMBER = "9767981986"
MY_UPI_ID = "9767981986@ybl"

# ४. प्रोफेशनल डार्क & व्हाईट CSS (High Visibility)
st.markdown(f"""
    <style>
    .stApp {{ background-color: #FFFFFF !important; }}
    .app-header {{ 
        background-color: #000000; 
        color: #FFFFFF !important; 
        padding: 25px; 
        text-align: center; 
        font-size: 28px; 
        font-weight: bold; 
        border-radius: 0 0 25px 25px; 
        margin-bottom: 20px;
        letter-spacing: 1px;
    }}
    /* बटन्स स्टाईल */
    .stButton>button {{
        width: 100%;
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border
