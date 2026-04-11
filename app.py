import streamlit as st
import time
from streamlit_option_menu import option_menu

# १. पेज कॉन्फिगरेशन
st.set_page_config(page_title="Balaji Logistics & Tours", layout="wide", page_icon="🚖")

# २. फ्लॅश स्क्रीन लॉजिक
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
        </style>
        <div class="splash-container">
            <h1 style='color: #FFBB00; font-size: 60px;'>🚖 Balaji Logistics</h1>
            <p style='color: white; font-size: 20px;'>लोड होत आहे...</p>
        </div>
    """, unsafe_allow_html=True)
    
    bar = st.progress(0)
    for i in range(100):
        time.sleep(0.02)
        bar.progress(i + 1)
    
    st.session_state.splash_done = True
    st.rerun()

# ३. मुख्य ॲप
else:
    # तुझी काळी-पिवळी थीम आणि बॉटम मेनूसाठी CSS
    st.markdown("""
        <style>
        .stApp { background-color: #000000; color: white; margin-bottom: 80px; }
        .stButton>button { background-color: #FFBB00; color: black; font-weight: bold; border-radius: 12px; }
        
        /* हा कोड मेनूला खालच्या बाजूला फिक्स करेल */
        div[data-testid="stVerticalBlock"] > div:has(div.nav-link) {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #1a1a1a;
            z-index: 999;
            border-top: 2px solid #FFBB00;
            padding: 5px 0px;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- फीचर्स लॉजिक (कंटेंट आधी दाखवणे कारण मेनू खाली आहे) ---
    # इथे आपण 'container' वापरू जेणेकरून मेनू खाली गेल्यावर कंटेंट दिसेल
    main_container = st.container()

    with main_container:
        # आपण खाली निवडलेला 'selected' व्हेरिएबल इथे वापरणार आहोत
        # (आधी मेनू कोड लिहून मग डिस्प्ले करू)
        pass

    # --- बॉटम आडवा मेनू (Bottom Horizontal Menu) ---
    selected = option_menu(
        menu_title=None, 
        options=["Home", "Booking", "Login", "Register", "Dashboard", "Admin", "Contact"],
        icons=["house", "book", "person-lock", "person-plus", "speedometer2", "shield-lock", "telephone"],
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#1a1a1a"},
            "icon": {"color": "#FFBB00", "font-size": "16px"}, 
            "nav-link": {"font-size": "12px", "text-align": "center", "margin": "0px", "color": "white"},
            "nav-link-selected": {"background-color": "#FFBB00", "color": "black"},
        }
    )

    # निवडलेल्या पर्यायानुसार कंटेंट दाखवणे
    with main_container:
        if selected == "Home":
            st.title("🚖 Balaji Logistics Nashik")
            st.info("💰 दर: १३ रुपये प्रति किलोमीटर")
            st.image("https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?q=80&w=1000", caption="Swift Dzire")
            st.write("अंबड आणि पाथर्डी फाटा परिसरात २४ तास सेवा.")

        elif selected == "Booking":
            st.header("गाडी बुकिंग")
            with st.form("book"):
                st.text_input("तुमचे नाव")
                st.selectbox("गाडी", ["Swift Dzire", "Ertiga", "Innova"])
                st.form_submit_button("Book Now")

        elif selected == "Login":
            st.header("युझर लॉगिन")
            st.text_input("Username")
            st.text_input("Password", type="password")
            st.button("Login")

        elif selected == "Register":
            st.header("नवीन नोंदणी")
            st.text_input("पूर्ण नाव")
            st.button("Register")

        elif selected == "Dashboard":
            st.header("डॅशबोर्ड")
            st.write("तुमचा बुकिंग इतिहास इथे दिसेल.")

        elif selected == "Admin":
            st.header("अॅडमिन")
            st.text_input("पासवर्ड", type="password")

        elif selected == "Contact":
            st.header("संपर्क")
            st.write("📍 नाशिक - अंबड, पाथर्डी फाटा.")

    # रिकामी जागा सोडणे जेणेकरून मेनूमुळे कंटेंट झाकला जाणार नाही
    st.write("<br><br><br>", unsafe_allow_html=True)