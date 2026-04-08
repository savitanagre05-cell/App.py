import streamlit as st

# १. पेज सेटिंग्ज आणि डिझाइन (Look and Colors)
st.set_page_config(page_title="Balaji Logistics", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #f5f7f9;
    }
    .main-title {
        color: #1E3A8A;
        text-align: center;
        font-size: 40px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# २. जुने सर्व फीचर्सSidebar मध्ये मॅनेज करणे
st.sidebar.title("🚖 Balaji Navigation")
menu = ["Home", "Car Booking", "Parcel Service", "Track Order", "Admin Login"]
choice = st.sidebar.selectbox("पर्याय निवडा", menu)

# ३. मुख्य टायटल (जसे आधी होते)
st.markdown('<p class="main-title">Balaji Logistics and Tours and Travels</p>', unsafe_allow_html=True)

# ४. मूळ फिचर्स लोड करणे (Logic as per your previous code)

if choice == "Home":
    st.write("### स्वागत आहे!")
    st.info("आमच्या सर्व सेवा खालील प्रमाणे आहेत. कृपया डाव्या बाजूच्या मेनूचा वापर करा.")
    # तुमचे आधीचे होम पेजचे टेक्स्ट इथे येईल

elif choice == "Car Booking":
    st.subheader("🚗 Car Booking System")
    # तुमचे आधीचे सर्व इनपुट इथे:
    name = st.text_input("Customer Name")
    car_type = st.selectbox("Vehicle Type", ["Swift Dzire", "Ertiga", "Innova", "Tempo Traveler"])
    source = st.text_input("Pickup Point")
    dest = st.text_input("Destination")
    date = st.date_input("Travel Date")
    
    if st.button("Confirm Booking"):
        st.success(f"Booking confirmed for {name}!")

elif choice == "Parcel Service":
    st.subheader("📦 Parcel Delivery Service")
    weight = st.number_input("Weight (kg)")
    p_type = st.text_input("Item Description")
    sender = st.text_input("Sender Name")
    receiver = st.text_input("Receiver Address")
    
    if st.button("Submit Parcel Details"):
        st.success("Parcel details saved successfully.")

elif choice == "Track Order":
    st.subheader("🔍 Track Your Status")
    order_id = st.text_input("Enter Order/Booking ID")
    if st.button("Check Status"):
        st.warning("Tracking feature loading... (Database connection needed)")

elif choice == "Admin Login":
    st.subheader("🔐 Admin Access")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if user == "admin" and pwd == "balaji123":
            st.success("Welcome, Admin!")
        else:
            st.error("Invalid Credentials")