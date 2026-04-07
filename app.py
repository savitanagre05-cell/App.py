import streamlit as st
import pandas as pd

# १. अ‍ॅप सेटिंग्स
st.set_page_config(page_title="Balaji Logistics", page_icon="🚕", layout="wide")

# २. प्रीमियम मोबाईल अ‍ॅप स्टाईल CSS
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    /* मोबाईल अ‍ॅप सारखे नेव्हिगेशन बटन्स */
    .nav-container {
        display: flex;
        justify-content: space-around;
        background-color: #000000;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 25px;
    }
    .stButton>button {
        width: 100%;
        background-color: #000000;
        color: white;
        border: 1px solid #333;
        border-radius: 5px;
        padding: 10px;
    }
    .info-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #000;
        margin-bottom: 20px;
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

MY_NUMBER = "9767981986"

# --- ३. टॉप नेव्हिगेशन (Menu Buttons at Top) ---
st.title("🚕 Balaji Logistics")

# तीन कॉलम बनवून त्यात बटणे टाकली आहेत (मोबाईल अ‍ॅप सारखे)
col_nav1, col_nav2, col_nav3 = st.columns(3)

if "page" not in st.session_state:
    st.session_state.page = "🏠 होम"

with col_nav1:
    if st.button("🏠 होम"):
        st.session_state.page = "🏠 होम"
with col_nav2:
    if st.button("🚕 बुकिंग"):
        st.session_state.page = "🚕 बुकिंग"
with col_nav3:
    if st.button("📞 संपर्क"):
        st.session_state.page = "📞 संपर्क"

st.write("---")

# --- ४. पेज नुसार आशय (Content) ---

if st.session_state.page == "🏠 होम":
    st.subheader("तुमचा सुरक्षित प्रवास, आमची जबाबदारी!")
    st.image("https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?auto=format&fit=crop&w=1200", use_container_width=True)
    st.markdown("<div class='info-box'><h4>✅ २४ तास सेवा</h4><p>नाशिकमधील सर्वात विश्वसनीय टॅक्सी सेवा. आता एका क्लिकवर बुकिंग करा!</p></div>", unsafe_allow_html=True)

elif st.session_state.page == "🚕 बुकिंग":
    st.title("📍 राईड बुक करा")
    p_up = st.text_input("पिकअप ठिकाण")
    d_off = st.text_input("ड्रॉप ठिकाण")
    
    car_rates = {"🚗 Mini": 11, "🚖 Sedan": 14, "🚐 SUV": 17}
    selected_car = st.selectbox("गाडी निवडा:", list(car_rates.keys()))
    
    km = st.number_input("अंदाजित किमी", min_value=1, value=50)
    total = km * car_rates[selected_car]
    
    st.markdown(f"### 💰 अंदाजित भाडे: ₹{total}")
    
    u_name = st.text_input("तुमचे नाव")
    u_phone = st.text_input("मोबाईल नंबर")

    if st.button("BOOK ON WHATSAPP"):
        if u_name and u_phone and p_up and d_off:
            msg = f"🚩 *NEW BOOKING*\n👤 नाव: {u_name}\n📞 नंबर: {u_phone}\n📍 पिकअप: {p_up}\n🏁 ड्रॉप: {d_off}\n🚗 गाडी: {selected_car}\n💰 भाडे: ₹{total}"
            url = f"https://wa.me/91{MY_NUMBER}?text={msg.replace(' ', '%20').replace('\n', '%0A')}"
            st.success("व्हॉट्सॲपवर रिडायरेक्ट होत आहे...")
            st.markdown(f"[येथे क्लिक करा]({url})")

elif st.session_state.page == "📞 संपर्क":
    st.title("संपर्क")
    st.markdown(f"<div class='info-box'><h3>📞 हेल्पलाईन: {MY_NUMBER}</h3><p>नाशिक, महाराष्ट्र.</p></div>", unsafe_allow_html=True)

