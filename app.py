
import streamlit as st
import random
import folium
from streamlit_folium import st_folium

# --- १. अ‍ॅप कॉन्फिगरेशन (नेहमी पहिल्या ओळीवर हवे) ---
st.set_page_config(
    page_title="Balaji Logistics Nashik", 
    layout="centered", 
    page_icon="🚕"
)

# --- २. सेशन स्टेट मॅनेजमेंट (डेटा टिकवण्यासाठी) ---
if "is_auth" not in st.session_state:
    st.session_state.is_auth = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "ride_booked" not in st.session_state:
    st.session_state.ride_booked = False
if "current_fare" not in st.session_state:
    st.session_state.current_fare = 0
if "target_loc" not in st.session_state:
    st.session_state.target_loc = ""

# --- ३. कस्टम CSS (डिझाईनसाठी) ---
st.markdown("""
<style>
    /* मुख्य बॅकग्राउंड */
    .stApp { background-color: #f4f7f6; }
    
    /* हेडर स्टाईल */
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #000000, #333333);
        color: white;
        padding: 20px;
        border-radius: 0px 0px 25px 25px;
        margin-bottom: 25px;
    }
    
    /* कार्ड स्टाईल */
    .info-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    /* बटण स्टाईल */
    .stButton>button {
        width: 100%;
        background-color: #000 !important;
        color: white !important;
        border-radius: 10px;
        height: 48px;
        font-size: 16px;
        font-weight: bold;
        border: none;
    }
    
    .stButton>button:hover {
        background-color: #222 !important;
        border: 1px solid gold;
    }
</style>
""", unsafe_allow_html=True)

# --- ४. लॉगिन / नोंदणी फंक्शन ---
def show_login():
    st.markdown("<div class='main-header'><h1>Balaji Logistics</h1><p>नाशिकची आपली हक्काची टॅक्सी</p></div>", unsafe_allow_html=True)
    
    with st.container():
        st.subheader("प्रवेश करा / नोंदणी करा 🔑")
        name = st.text_input("तुमचे नाव (Full Name)")
        phone = st.text_input("मोबाईल नंबर (10 Digit Mobile)", max_chars=10)
        
        if st.button("सुरू करा ➔"):
            if name and len(phone) == 10 and phone.isdigit():
                st.session_state.user_name = name
                st.session_state.is_auth = True
                st.success(f"स्वागत आहे, {name}!")
                st.rerun()
            else:
                st.error("कृपया वैध नाव आणि १० अंकी नंबर टाका!")

# --- ५. मुख्य होम स्क्रीन फंक्शन ---
def show_home():
    # Sidebar नेव्हिगेशन
    with st.sidebar:
        st.title("🚖 मेनू")
        choice = st.radio("पर्याय निवडा", ["🏠 होम", "📜 प्रवासाचा इतिहास", "👤 प्रोफाइल"])
        st.write("---")
        if st.button("Logout 🚪"):
            st.session_state.is_auth = False
            st.rerun()

    if choice == "🏠 होम":
        st.markdown(f"### नमस्कार, {st.session_state.user_name}! 👋")
        
        # मॅप डिस्प्ले
        st.write("तुमचे लोकेशन (नाशिक):")
        m = folium.Map(location=[20.0022, 73.7898], zoom_start=13)
        folium.Marker([20.0022, 73.7898], popup="You are here", icon=folium.Icon(color='black', icon='home')).add_to(m)
        st_folium(m, width="100%", height=250, key="nashik_map")
        
        # बुकिंग कार्ड
        st.markdown("<div class='info-card'>", unsafe_allow_html=True)
        st.subheader("नवीन राईड बुक करा")
        dest = st.text_input("कुठे जायचे आहे? (Destination)", placeholder="उदा. नाशिक रोड, पंचवटी, सीबीएस")
        car_type = st.selectbox("गाडी निवडा", ["🚗 Mini (₹12/km)", "🚖 Sedan (₹15/km)", "🚐 SUV (₹22/km)"])
        
        # भाडे कॅल्क्युलेशन लॉजिक
        dist_est = random.randint(4, 12)
        base_rates = {"🚗 Mini (₹12/km)": 12, "🚖 Sedan (₹15/km)": 15, "🚐 SUV (₹22/km)": 22}
        total_fare = dist_est * base_rates[car_type]
        
        st.info(f"अंदाजे अंतर: {dist_est} किमी | अंदाजे भाडे: **₹{total_fare}**")
        
        if st.button("बुक करा ✅"):
            if dest:
                st.session_state.ride_booked = True
                st.session_state.target_loc = dest
                st.session_state.current_fare = total_fare
                st.balloons()
            else:
                st.warning("कृपया डेस्टिनेशन टाका!")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # राईड स्टेटस
        if st.session_state.ride_booked:
            st.success(f"✅ राईड कन्फर्म झाली आहे!\n\n🚕 **गाडी:** {car_type}\n📍 **डेस्टिनेशन:** {st.session_state.target_loc}\n💰 **भाडे:** ₹{st.session_state.current_fare}")
            if st.button("प्रवास पूर्ण झाला? 🏁"):
                st.session_state.ride_booked = False
                st.rerun()

    elif choice == "📜 प्रवासाचा इतिहास":
        st.subheader("तुमचे मागील प्रवास 📜")
        history = [
            {"तारीख": "05 एप्रिल", "ठिकाण": "नाशिक रोड ते कॉलेज रोड", "भाडे": "₹180"},
            {"तारीख": "02 एप्रिल", "ठिकाण": "पंचवटी ते सातपूर", "भाडे": "₹220"}
        ]
        st.table(history)

    elif choice == "👤 प्रोफाइल":
        st.subheader("माझे प्रोफाईल 👤")
        st.write(f"**नाव:** {st.session_state.user_name}")
        st.write("**शहर:** नाशिक, महाराष्ट्र")
        st.info("प्रोफाईल अपडेट करण्यासाठी कस्टमर केअरला संपर्क करा.")

# --- ६. मेन रन लॉजिक ---
if not st.session_state.is_auth:
    show_login()
else:
    show_home()