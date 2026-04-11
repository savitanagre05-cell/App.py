import streamlit as st
import time

# १. पेज कॉन्फिगरेशन (हे सर्वात वर हवे)
st.set_page_config(page_title="Balaji Logistics & Tours", layout="centered", page_icon="🚖")

# २. फ्लॅश स्क्रीनचे लॉजिक (Session State वापरून)
if 'splash_done' not in st.session_state:
    st.session_state.splash_done = False

if not st.session_state.splash_done:
    # --- फ्लॅश स्क्रीनचे डिझाईन (CSS वापरून) ---
    st.markdown("""
        <style>
        .splash-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 60vh;
            text-align: center;
            background-color: #f0f2f6;
            border-radius: 20px;
            padding: 20px;
        }
        .main-title {
            font-size: 45px;
            color: #FF4B4B;
            font-weight: bold;
            margin-bottom: 5px;
            font-family: 'Arial';
        }
        .sub-title {
            font-size: 22px;
            color: #31333F;
            margin-bottom: 20px;
        }
        .tagline {
            font-style: italic;
            color: #555;
        }
        </style>
        <div class="splash-container">
            <div class="main-title">🚖 Balaji Logistics</div>
            <div class="sub-title">Tours & Travels</div>
            <p class="tagline">"तुमचा प्रवास, आमची जबाबदारी..."</p>
        </div>
    """, unsafe_allow_html=True)
    
    # प्रोग्रेस बार (लोडिंग दाखवण्यासाठी)
    progress_text = "ॲप लोड होत आहे, कृपया थांबा..."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.02)  # २-३ सेकंदाचा वेळ
        my_bar.progress(percent_complete + 1, text=progress_text)
    
    # फ्लॅश स्क्रीन संपली, आता मुख्य ॲपवर जा
    st.session_state.splash_done = True
    st.rerun()

# ३. मुख्य ॲप कोड (Main App Logic)
else:
    # --- नेव्हिगेशन मेनू ---
    st.sidebar.title("Balaji Menu")
    choice = st.sidebar.radio("पर्याय निवडा", ["Home (मुख्य पान)", "Car Booking (गाडी बुकिंग)", "Register (नोंदणी)", "Login (लॉगिन)"])

    if choice == "Home (मुख्य पान)":
        st.title("🚖 Balaji Logistics and Tours & Travels")
        st.subheader("नाशिकमधील सर्वोत्तम ट्रॅव्हल्स सर्व्हिस!")
        st.image("https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?auto=format&fit=crop&q=80&w=1000", caption="आरामदायी प्रवास")
        
        st.write("""
        आमच्याकडे सर्व प्रकारच्या गाड्या माफक दरात उपलब्ध आहेत:
        * **दर:** १३ रुपये प्रति किलोमीटर
        * **गाड्या:** Swift Dzire, Ertiga, Innova, इत्यादी.
        * **संपर्क:** अंबड, पाथर्डी फाटा, नाशिक.
        """)
        
        if st.button("बुकिंग सुरू करा"):
            st.info("कृपया डाव्या बाजूच्या मेनूमधून 'Car Booking' निवडा.")

    elif choice == "Car Booking (गाडी बुकिंग)":
        st.header("तुमची गाडी बुक करा")
        with st.form("booking_form"):
            name = st.text_input("तुमचे पूर्ण नाव")
            pickup = st.text_input("कुठून (Pickup Location)")
            drop = st.text_input("कुठे (Drop Location)")
            date = st.date_input("प्रवासाची तारीख")
            car_type = st.selectbox("गाडीचा प्रकार", ["Swift Dzire (4+1)", "Ertiga (6+1)", "Innova (7+1)"])
            
            submit = st.form_submit_button("बुकिंग कन्फर्म करा")
            
            if submit:
                if name and pickup and drop:
                    st.success(f"धन्यवाद {name}! तुमचे {car_type} साठीचे बुकिंग स्वीकारले आहे. आम्ही लवकरच संपर्क करू.")
                    st.balloons()
                else:
                    st.error("कृपया सर्व माहिती भरा.")

    elif choice == "Register (नोंदणी)":
        st.header("नवीन खाते उघडा")
        reg_name = st.text_input("नाव")
        reg_phone = st.text_input("मोबाईल नंबर")
        reg_pass = st.text_input("पासवर्ड", type="password")
        if st.button("नोंदणी करा"):
            st.success("तुमची नोंदणी यशस्वी झाली आहे!")

    elif choice == "Login (लॉगिन)":
        st.header("लॉगिन करा")
        user = st.text_input("मोबाईल नंबर किंवा युझरनेम")
        pwd = st.text_input("पासवर्ड", type="password")
        if st.button("प्रवेश करा"):
            if user == "admin" and pwd == "123":
                st.success("लॉगिन यशस्वी!")
            else:
                st.error("चुकीचा युझरनेम किंवा पासवर्ड.")

# फुटर (प्रत्येक पेजवर दिसेल)
if st.session_state.splash_done:
    st.markdown("---")
    st.caption("© 2026 Balaji Logistics Nashik | Powered by Gemini")