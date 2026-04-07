
import streamlit as st
import pandas as pd
from datetime import datetime

# १. अ‍ॅप कॉन्फिगरेशन (Uber Style)
st.set_page_config(page_title="Balaji Logistics", page_icon="🚕", layout="wide")

# २. Uber Premium CSS (Modern Black & White Theme)
st.markdown("""
    <style>
    /* मुख्य बॅकग्राउंड */
    .stApp { background-color: #FFFFFF; }
    
    /* साईडबार (Navigation) - Uber Black */
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
        color: white !important;
    }
    [data-testid="stSidebar"] * { color: white !important; }
    
    /* प्रीमियम बटण स्टाईल */
    .stButton>button {
        width: 100%;
        background-color: #000000;
        color: #FFFFFF;
        border: none;
        padding: 18px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 8px;
        transition: 0.3s;
        border: 1px solid #333;
    }
    .stButton>button:hover {
        background-color: #333333;
        transform: translateY(-2px);
    }
    
    /* माहिती कार्ड्स */
    .info-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #000;
        margin-bottom: 20px;
        color: black;
    }
    
    h1, h2, h3 { color: #000000; font-family: 'Uber Move', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# ३. नेव्हिगेशन मेनू (Tabs)
st.sidebar.markdown("# 🚕 Balaji Uber")
page = st.sidebar.radio("मेनू निवडा:", ["🏠 होम (Home)", "🚕 राईड बुक करा (Booking)", "📞 सपोर्ट (Support)"])

# तुमचा नंबर
MY_NUMBER = "9767981986"

# --- १. होम पेज (HOME SECTION) ---
if page == "🏠 होम (Home)":
    st.title("Balaji Logistics")
    st.subheader("तुमचा सुरक्षित आणि आरामदायी प्रवास, आमची जबाबदारी!")
    
    st.image("https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?auto=format&fit=crop&w=1200", use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='info-box'>
            <h4>🌟 आमच्या सेवा</h4>
            <ul>
                <li>नाशिक ते मुंबई / पुणे एअरपोर्ट ड्रॉप</li>
                <li>स्वच्छ आणि सॅनिटाईझ केलेल्या गाड्या</li>
                <li>अनुभवी आणि वेळेचे पक्के ड्रायव्हर्स</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='info-box'>
            <h4>💰 स्वस्त दर</h4>
            <p>आम्ही नाशिकमध्ये सर्वात कमी दरात टॅक्सी सेवा देतो. कोणतेही छुपे चार्जेस नाहीत!</p>
        </div>
        """, unsafe_allow_html=True)

    if st.button("आत्ताच राईड बुक करा ➔"):
        st.info("डाव्या बाजूला 'Booking' वर क्लिक करा.")

# --- २. बुकिंग पेज (BOOKING SECTION) ---
elif page == "🚕 राईड बुक करा (Booking)":
    st.title("📍 तुमची राईड निश्चित करा")
    
    col_form, col_map = st.columns([1, 1.2])
    
    with col_form:
        st.markdown("### प्रवासाचा तपशील")
        p_up = st.text_input("पिकअप ठिकाण (उदा. नाशिक)", placeholder="कुठून?")
        d_off = st.text_input("ड्रॉप ठिकाण (उदा. शिर्डी)", placeholder="कुठे?")
        
        st.write("---")
        st.subheader("गाडीचा प्रकार")
        car_rates = {
            "🚗 Balaji Mini (₹11/km)": 11,
            "🚖 Balaji Sedan (₹14/km)": 14,
            "🚐 Balaji SUV (₹17/km)": 17
        }
        selected_car = st.selectbox("गाडी निवडा:", list(car_rates.keys()))
        
        km = st.number_input("अंदाजित किमी (KM)", min_value=1, value=50)
        rate = car_rates[selected_car]
        total = km * rate
        
        st.markdown(f"<h2 style='color:#008000;'>अंदाजित भाडे: ₹{total}</h2>", unsafe_allow_html=True)
        st.caption(f"*टोल आणि पार्किंगचे पैसे वेगळे असतील.")

    with col_map:
        st.markdown("### नकाशावर पहा")
        # नाशिकचे डिफॉल्ट लोकेशन
        df = pd.DataFrame({'lat': [19.9975], 'lon': [73.7898]})
        st.map(df)

    st.write("---")
    st.subheader("तुमची माहिती")
    u_name = st.text_input("तुमचे पूर्ण नाव")
    u_phone = st.text_input("मोबाईल नंबर")
    
    if st.button("CONFIRM BOOKING"):
        if u_name and u_phone and p_up and d_off:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            msg = (f"🚩 *नवीन बुकिंग (BALAJI UBER)*\n"
                   f"━━━━━━━━━━━━━━━━━━━\n"
                   f"👤 नाव: {u_name}\n"
                   f"📞 नंबर: {u_phone}\n"
                   f"📍 पिकअप: {p_up}\n"
                   f"🏁 ड्रॉप: {d_off}\n"
                   f"🚗 गाडी: {selected_car}\n"
                   f"💰 भाडे: ₹{total}\n"
                   f"⏰ वेळ: {now}\n"
                   f"━━━━━━━━━━━━━━━━━━━")
            
            whatsapp_url = f"https://wa.me/91{MY_NUMBER}?text={msg.replace(' ', '%20').replace('\n', '%0A')}"
            st.balloons()
            st.success("बुक झाले! कृपया व्हॉट्सॲपवर माहिती पाठवा.")
            st.markdown(f"### [👉 येथे क्लिक करा आणि मेसेज पाठवा]({whatsapp_url})")
        else:
            st.error("कृपया सर्व माहिती अचूक भरा!")

# --- ३. सपोर्ट पेज (SUPPORT SECTION) ---
elif page == "📞 सपोर्ट (Support)":
    st.title("संपर्क आणि मदत")
    
    st.markdown(f"""
    <div class='info-box'>
        <h3>📞 २४/७ हेल्पलाईन</h3>
        <p>काही शंका असल्यास किंवा तातडीच्या प्रवासासाठी फोन करा:</p>
        <h2 style='color:black;'>{MY_NUMBER}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    
    if st.button("थेट व्हॉट्सॲप चॅट करा"):
        support_url = f"https://wa.me/91{MY_NUMBER}?text=Hello%20Balaji%20Logistics,%20मला%20काही%20मदत%20हवी%20आहे."
        st.markdown(f"[👉 व्हॉट्सॲप उघडा]({support_url})")
