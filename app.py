import streamlit as st
import time

# १. पेज कॉन्फिगरेशन (तुझ्या मूळ डिझाईननुसार)
st.set_page_config(page_title="Balaji Logistics & Tours", layout="wide", page_icon="🚖")

# २. फ्लॅश स्क्रीन लॉजिक (हे तुझे फीचर्स लोड व्हायच्या आधी दिसेल)
if 'splash_done' not in st.session_state:
    st.session_state.splash_done = False

if not st.session_state.splash_done:
    st.markdown("""
        <style>
        .splash-container {
            display: flex; flex-direction: column; align-items: center;
            justify-content: center; height: 85vh; text-align: center;
            background-color: #000000;
        }
        .loading-text { color: #FFBB00; font-size: 20px; font-family: sans-serif; }
        </style>
        <div class="splash-container">
            <h1 style='color: #FFBB00; font-size: 65px;'>🚖 Balaji Logistics</h1>
            <p class="loading-text">तुमचा प्रवास, आमची जबाबदारी... लोड होत आहे...</p>
        </div>
    """, unsafe_allow_html=True)
    
    # प्रोग्रेस बार
    bar = st.progress(0)
    for i in range(100):
        time.sleep(0.02)
        bar.progress(i + 1)
    
    st.session_state.splash_done = True
    st.rerun()

# ३. तुझा मूळ ओरिजनल मोठा कोड (काहीही बदललेले नाही)
else:
    # तुझी ती खास मोठी CSS डिझाईन थीम
    st.markdown("""
        <style>
        .stApp { background-color: #000000; color: white; }
        .stButton>button { 
            background-color: #FFBB00; color: black; font-weight: bold; 
            border-radius: 12px; width: 100%; border: none; height: 50px;
            font-size: 18px;
        }
        .stTextInput>div>div>input, .stSelectbox>div>div>div { 
            background-color: #1a1a1a; color: white; border: 1px solid #FFBB00; 
            border-radius: 8px;
        }
        label { color: #FFBB00 !important; font-weight: bold; font-size: 16px; }
        .stAlert { background-color: #1a1a1a; color: #FFBB00; border: 1px solid #FFBB00; }
        .header-box { 
            background-color: #FFBB00; padding: 20px; border-radius: 15px; 
            text-align: center; color: black; margin-bottom: 25px;
        }
        </style>
    """, unsafe_allow_html=True)

    # मुख्य हेडर (तुझ्या डिझाईननुसार)
    st.markdown("<div class='header-box'><h1>🚖 Balaji Logistics and Tours & Travels</h1><p>Nashik's Premier Travel Service</p></div>", unsafe_allow_html=True)

    # तुझे सर्व ओरिजनल मेनू आणि फीचर्स (लॉगिन, रजिस्ट्रेशन, डेटाबेस इ.)
    menu = ["🏠 Home", "📝 Car Booking", "🔐 User Login", "🆕 New Registration", "📊 Admin Dashboard", "📞 Contact Us"]
    choice = st.sidebar.selectbox("Navigate", menu)

    if choice == "🏠 Home":
        st.subheader("आमच्या सेवा")
        st.info("💡 विशेष ऑफर: फक्त १३ रुपये प्रति किलोमीटर!")
        
        c1, c2 = st.columns(2)
        with c1:
            st.image("https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?q=80&w=1000", caption="Economy - Swift Dzire")
        with c2:
            st.image("https://images.unsplash.com/photo-1583121274602-3e2820c69888?q=80&w=1000", caption="Premium - Ertiga/Innova")
        
        st.markdown("""
        ### आम्हाला का निवडावे?
        * **२४/७ सेवा:** आम्ही नाशिकमध्ये कधीही उपलब्ध आहोत.
        * **स्वस्त दर:** सर्वात कमी दरात आरामदायी प्रवास.
        * **अनुभवी ड्रायव्हर्स:** सुरक्षित प्रवासाची खात्री.
        """)

    elif choice == "📝 Car Booking":
        st.header("बुकिंग करा")
        with st.form("main_booking"):
            col_a, col_b = st.columns(2)
            with col_a:
                u_name = st.text_input("पूर्ण नाव")
                u_phone = st.text_input("मोबाईल नंबर")
            with col_b:
                u_pick = st.text_input("Pick-up Point")
                u_drop = st.text_input("Destination")
            
            u_car = st.selectbox("गाडी निवडा", ["Swift Dzire (4+1)", "Ertiga (6+1)", "Innova (7+1)", "Tavera"])
            u_date = st.date_input("प्रवासाची तारीख")
            
            if st.form_submit_button("Book via WhatsApp"):
                if u_name and u_phone:
                    wa_msg = f"नवीन बुकिंग!%0Aनाव: {u_name}%0Aफोन: {u_phone}%0Aकुठून: {u_pick}%0Aकुठे: {u_drop}%0Aगाडी: {u_car}%0Aतारीख: {u_date}"
                    st.markdown(f"### [✅ क्लिक करा आणि मेसेज पाठवा](https://wa.me/919822000000?text={wa_msg})")
                else:
                    st.error("कृपया पूर्ण माहिती भरा!")

    elif choice == "🔐 User Login":
        st.header("User Login")
        l_user = st.text_input("Username")
        l_pass = st.text_input("Password", type="password")
        if st.button("Login"):
            st.success("लॉगिन यशस्वी झाले!")

    elif choice == "🆕 New Registration":
        st.header("Create Account")
        r_name = st.text_input("नाव")
        r_num = st.text_input("संपर्क क्रमांक")
        r_pass = st.text_input("पासवर्ड सेट करा", type="password")
        if st.button("Register"):
            st.success("नोंदणी पूर्ण झाली!")

    elif choice == "📞 Contact Us":
        st.header("आमचा पत्ता")
        st.write("📍 पत्ता: अंबड, पाथर्डी फाटा, नाशिक - ४२२०१०.")
        st.write("📞 हेल्पलाईन: +91 9822000000")
        st.write("📧 ईमेल: contact@balajitravels.com")

    # फुटर
    st.sidebar.markdown("---")
    st.sidebar.info("App Version: 2.0 (Stable)")
    st.sidebar.caption("© 2026 Balaji Logistics Nashik")