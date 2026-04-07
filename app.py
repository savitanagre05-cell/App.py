
# १. अ‍ॅप सेटिंग्स
st.set_page_config(page_title="Balaji Logistics", page_icon="🚕", layout="wide")

# २. Uber Premium CSS
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #000000 !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stButton>button {
        width: 100%;
        background-color: #000000;
        color: #FFFFFF;
        padding: 15px;
        border-radius: 8px;
        font-weight: bold;
    }
    .info-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #000;
        margin-bottom: 20px;
    }
    h1, h2, h3 { color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# ३. नेव्हिगेशन
st.sidebar.title("🚕 Balaji Menu")
page = st.sidebar.radio("निवडा:", ["Home", "Booking", "Support"])

MY_NUMBER = "9767981986"

# --- १. HOME PAGE ---
if page == "Home":
    st.title("Balaji Logistics Nashik")
    st.image("https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?auto=format&fit=crop&w=1200", use_container_width=True)
    
    st.markdown("""
    <div class='info-box'>
        <h3>आमच्या सेवा</h3>
        <p>नाशिकमधील सर्वात स्वस्त आणि सुरक्षित टॅक्सी सेवा. २४ तास उपलब्ध!</p>
    </div>
    """, unsafe_allow_html=True)

# --- २. BOOKING PAGE ---
elif page == "Booking":
    st.title("📍 राईड बुक करा")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        p_up = st.text_input("पिकअप (कुठून?)")
        d_off = st.text_input("ड्रॉप (कुठे?)")
        
        car_rates = {"🚗 Mini": 11, "🚖 Sedan": 14, "🚐 SUV": 17}
        car = st.selectbox("गाडी निवडा:", list(car_rates.keys()))
        
        km = st.number_input("अंदाजित किमी", min_value=1, value=50)
        total = km * car_rates[car]
        st.markdown(f"### 💰 भाडे: ₹{total}")

    with col2:
        # नकाशा दाखवण्यासाठी साधा डेटा
        df = pd.DataFrame({'lat': [19.9975], 'lon': [73.7898]})
        st.map(df)

    st.write("---")
    name = st.text_input("तुमचे नाव")
    phone = st.text_input("मोबाईल नंबर")

    if st.button("CONFIRM RIDE"):
        if name and phone and p_up and d_off:
            msg = (f"🚩 *NEW BOOKING*\n"
                   f"👤 नाव: {name}\n"
                   f"📞 नंबर: {phone}\n"
                   f"📍 पिकअप: {p_up}\n"
                   f"🏁 ड्रॉप: {d_off}\n"
                   f"🚗 गाडी: {car}\n"
                   f"💰 भाडे: ₹{total}")
            
            url = f"https://wa.me/91{MY_NUMBER}?text={msg.replace(' ', '%20').replace('\n', '%0A')}"
            st.balloons()
            st.success("बुक झाले! मेसेज पाठवा.")
            st.markdown(f"### [👉 WhatsApp वर पाठवा]({url})")

# --- ३. SUPPORT PAGE ---
elif page == "Support":
    st.title("संपर्क")
    st.write(f"### 📞 फोन: {MY_NUMBER}")
    st.write("२४ तास सेवा उपलब्ध.")
