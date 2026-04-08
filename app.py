import streamlit as st

# १. पेज कॉन्फिगरेशन (Uber Style Look)
st.set_page_config(page_title="Balaji Logistics", page_icon="🚖", layout="centered")

# २. कस्टम CSS (Colors आणि लूक सुधारण्यासाठी)
st.markdown("""
    <style>
    .stApp {
        background-color: #FFFFFF;
    }
    .main-header {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #000000;
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 0px;
    }
    .uber-card {
        background-color: #F3F3F3;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #000000;
        margin-bottom: 10px;
    }
    div.stButton > button:first-child {
        background-color: #000000;
        color: white;
        width: 100%;
        height: 50px;
        border-radius: 8px;
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)

# ३. लोगो आणि मुख्य नाव (Home Screen)
# टीप: 'logo.png' तुमच्या फोल्डरमध्ये ठेवा किंवा खालील URL बदला
st.image("https://cdn-icons-png.flaticon.com/512/75/75780.png", width=80) # हा एक डमी लोगो आहे
st.markdown('<p class="main-header">Balaji Logistics & Tours</p>', unsafe_allow_html=True)
st.write("---")

# ४. Uber सारखे नेव्हिगेशन (Tabs वापरून - जेणेकरून ते मोबाईल ॲपसारखे वाटेल)
tab1, tab2, tab3 = st.tabs(["🚗 Car Booking", "📦 Parcel", "🔍 Track"])

# --- CAR BOOKING TAB ---
with tab1:
    st.markdown('<div class="uber-card"><b>तुमचा प्रवास निवडा</b></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        pickup = st.text_input("📍 Pickup Location", placeholder="कुठून?")
    with col2:
        drop = st.text_input("🏁 Drop Location", placeholder="कुठे?")
    
    car_type = st.selectbox("Vehicle Type", ["Swift Dzire (Economy)", "Ertiga (Prime)", "Innova (Luxury)", "Tempo (Group)"])
    date = st.date_input("प्रवासाची तारीख")
    
    if st.button("Confirm Booking"):
        if pickup and drop:
            st.success(f"तुमची {car_type} साठी बुकिंग विनंती पाठवली आहे!")
        else:
            st.error("कृपया ठिकाण निवडा!")

# --- PARCEL SERVICE TAB ---
with tab2:
    st.markdown('<div class="uber-card"><b>पार्सल डिलिव्हरी</b></div>', unsafe_allow_html=True)
    
    p_weight = st.number_input("Weight (kg)", min_value=1)
    p_details = st.text_area("पार्सलचे वर्णन", placeholder="उदा. कागदपत्रे, घरगुती सामान इ.")
    sender_addr = st.text_input("Sender Address")
    receiver_addr = st.text_input("Receiver Address")
    
    if st.button("Request Delivery"):
        st.success("डिलिव्हरी रिक्वेस्ट यशस्वी झाली!")

# --- TRACKING TAB ---
with tab3:
    st.markdown('<div class="uber-card"><b>ट्रॅकिंग</b></div>', unsafe_allow_html=True)
    order_id = st.text_input("Booking ID टाका", placeholder="उदा. BL1234")
    
    if st.button("Track Now"):
        st.info("तुमची गाडी सध्या 'In Transit' आहे.")