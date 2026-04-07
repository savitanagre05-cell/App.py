

   import streamlit as st
import random
import folium
from streamlit_folium import st_folium

# १. पेज सेटिंग (हे सर्वात वर हवे)
st.set_page_config(page_title="Balaji Logistics", layout="centered")

# २. मेमरी व्यवस्थापन (Session State)
if "is_auth" not in st.session_state:
    st.session_state.is_auth = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "ride_booked" not in st.session_state:
    st.session_state.ride_booked = False

# ३. अ‍ॅपची डिझाइन (CSS)
st.markdown("""
<style>
    .main { background-color: #f5f5f5; }
    .stButton>button { width: 100%; background-color: #000 !important; color: white !important; border-radius: 10px; height: 50px; font-weight: bold; }
    .login-card { padding: 30px; background: white; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
    .header-box { background: #000; color: #fff; padding: 20px; text-align: center; border-radius: 0 0 20px 20px; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# ४. रजिस्ट्रेशन आणि लॉगिन फंक्शन
def show_login():
    st.markdown("<div class='header-box'><h1>Balaji Logistics</h1></div>", unsafe_allow_html=True)
    with st.container():
        st.subheader("पहिले रजिस्ट्रेशन करा 🚕")
        name = st.text_input("तुमचे नाव (Full Name)")
        phone = st.text_input("मोबाईल नंबर (10 Digit Mobile)")
        
        if st.button("Register & Start ➔"):
            if name and len(phone) == 10:
                st.session_state.user_name = name
                st.session_state.is_auth = True
                st.success(f"स्वागत आहे, {name}!")
                st.rerun()
            else:
                st.error("कृपया नाव आणि योग्य मोबाईल नंबर टाका!")

# ५. मुख्य अ‍ॅप (लॉगिन झाल्यावर)
def show_main_app():
    # नेव्हिगेशन मेनू
    menu = st.sidebar.radio("Menu", ["🏠 Home", "📜 History", "👤 Profile"])
    
    if menu == "🏠 Home":
        st.markdown(f"### नमस्कार, {st.session_state.user_name}! 👋")
        
        # मॅप डिस्प्ले (Nashik Center)
        st.write("तुमचे सध्याचे लोकेशन:")
        m = folium.Map(location=[20.0022, 73.7898], zoom_start=14, zoom_control=False)
        folium.Marker([20.0022, 73.7898], popup="You", icon=folium.Icon(color='blue')).add_to(m)
        st_folium(m, width="100%", height=250, key="home_map")
        
        # बुकिंग फॉर्म
        st.subheader("कुठे जायचे आहे?")
        drop = st.text_input("Drop Location", placeholder="उदा. नाशिक रोड स्टेशन")
        car = st.selectbox("गाडी निवडा", ["🚗 Mini (₹11/km)", "🚖 Sedan (₹14/km)", "🚐 SUV (₹18/km)"])
        
        if st.button("Confirm Ride ✅"):
            if drop:
                st.session_state.ride_booked = True
                st.session_state.target = drop
                st.success(f"तुमची राईड {drop} साठी बुक झाली आहे!")
            else:
                st.warning("कृपया जाण्याचे ठिकाण टाका.")

        # राईड ॲक्टिव्ह असेल तर स्टेटस दाखवणे
        if st.session_state.ride_booked:
            st.info(f"🚕 ड्रायव्हर अनिल नागरे येत आहेत | डेस्टिनेशन: {st.session_state.target}")
            if st.button("Finish Trip 🏁"):
                st.session_state.ride_booked = False
                st.balloons()
                st.rerun()

    elif menu == "📜 History":
        st.title("History 📜")
        st.write("१. कॉलेज रोड ते पंचवटी - १० एप्रिल")
        st.write("२. सीबीएस ते नाशिक रोड - ८ एप्रिल")

    elif menu == "👤 Profile":
        st.title("My Profile 👤")
        st.write(f"👤 **नाव:** {st.session_state.user_name}")
        st.write("📞 **नंबर:** verified")
        if st.button("Logout 🚪"):
            st.session_state.is_auth = False
            st.session_state.ride_booked = False
            st.rerun()

# ६. अ‍ॅप रन लॉजिक
if not st.session_state.is_auth:
    show_login()
else:
    show_main_app()
 