import streamlit as st
import pandas as pd
from datetime import datetime

# १. अ‍ॅप सेटिंग्स (Uber Black & White Theme)
st.set_page_config(page_title="Balaji Logistics", page_icon="🚕", layout="wide")

# २. प्रीमियम डिझाइन (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #000000 !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stButton>button {
        width: 100%;
        background-color: #000000;
        color: #FFFFFF;
        padding: 18px;
        border-radius: 8px;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover { background-color: #333333; }
    .info-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #000;
        margin-bottom: 20px;
        color: black;
    }
    h1, h2, h3 { color: black !important; font-family: 'Helvetica', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# ३. नेव्हिगेशन मेनू (Tabs)
st.sidebar.title("🚕 Balaji Menu")
page = st.sidebar.radio("निवडा:", ["🏠 होम", "🚕 बुकिंग", "📞 संपर्क"])

MY_NUMBER = "9767981986"

# --- १. होम पेज (HOME) ---
if page == "🏠 होम":
    st.title("Balaji Logistics Nashik")
    st.subheader("तुमचा सुरक्षित प्रवास, आमची जबाबदारी!")
    st.image("https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?auto=format&fit=crop&w=1200", use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='info-box'><h4>✅ आमच्या सेवा</h4><ul><li>एअरपोर्ट ड्रॉप & पिकअप</li><li>स्वच्छ आणि सॅनिटाईझ गाड्या</li><li>अनुभवी ड्रायव्हर्स</li></ul></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='info-box'><h4>💰 बेस्ट रेट्स</h4><p>नाशिकमधील सर्वात किफायतशीर दरात टॅक्सी सेवा उपलब्ध. टोल व पार्किंग सोडून पारदर्शक दर!</p></div>", unsafe_allow_html=True)

# --- २. बुकिंग पेज (BOOKING) ---
elif page == "🚕 बुकिंग":
    st.title("📍 राईड बुक करा")
    col_f, col_m = st.columns([1, 1.2])
    
    with col_f:
        p_up = st.text_input("पिकअप ठिकाण", placeholder="उदा. नाशिक रोड")
        d_off = st.text_input("ड्रॉप ठिकाण", placeholder="उदा. मुंबई एअरपोर्ट")
        
        car_rates = {"🚗 Mini (₹11/km)": 11, "🚖 Sedan (₹14/km)": 14, "🚐 SUV (₹17/km)": 17}
        selected_car = st.selectbox("गाडी निवडा:", list(car_rates.keys()))
        
        km = st.number_input("अंदाजित किमी", min_value=1, value=50)
        total = km * car_rates[selected_car]
        st.markdown(f"<h2 style='color:green;'>भाडे: ₹{total}</h2>", unsafe_allow_html=True)

    with col_m:
        st.markdown("### नकाशा")
        df = pd.DataFrame({'lat': [19.9975], 'lon': [73.7898]})
        st.map(df)

    st.write("---")
    u_name = st.text_input("तुमचे नाव")
    u_phone = st.text_input("मोबाईल नंबर")

    if st.button("CONFIRM RIDE"):
        if u_name and u_phone and p_up and d_off:
            msg = (f"🚩 *NEW BOOKING*\n👤 नाव: {u_name}\n📞 नंबर: {u_phone}\n📍 पिकअप: {p_up}\n🏁 ड्रॉप: {d_off}\n🚗 गाडी: {selected_car}\n💰 भाडे: ₹{total}")
            whatsapp_url = f"https://wa.me/91{MY_NUMBER}?text={msg.replace(' ', '%20').replace('\n', '%0A')}"
            st.balloons()
            st.success("बुकिंग झाले! व्हॉट्सॲपवर मेसेज पाठवा.")
            st.markdown(f"### [👉 येथे क्लिक करा]({whatsapp_url})")
        else:
            st.error("कृपया सर्व माहिती भरा!")

# --- ३. संपर्क (SUPPORT) ---
elif page == "📞 संपर्क":
    st.title("आमच्याशी संपर्क साधा")
    st.markdown(f"<div class='info-box'><h3>📞 हेल्पलाईन: {MY_NUMBER}</h3><p>आम्ही २४/७ उपलब्ध आहोत.</p></div>", unsafe_allow_html=True)
    if st.button("थेट कॉल करा"):
        st.info(f"कृपया डायल करा: {MY_NUMBER}")
