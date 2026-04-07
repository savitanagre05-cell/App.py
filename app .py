
  
import streamlit as st
import pandas as pd
from datetime import datetime

# १. अ‍ॅपचे नाव आणि पेज सेटिंग (Uber Style)
st.set_page_config(page_title="Balaji Logistics", page_icon="🚕", layout="centered")

# २. Uber Premium CSS (रंग आणि डिझाइन बदलणे)
st.markdown("""
    <style>
    /* पूर्ण बॅकग्राउंड पांढरा */
    .stApp { background-color: #FFFFFF; }
    
    /* टायटल आणि अक्षरे काळी */
    h1, h2, h3, p, label {
        color: #000000 !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* Uber Black Button */
    .stButton>button {
        width: 100%;
        background-color: #000000;
        color: #FFFFFF;
        border: none;
        padding: 18px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 4px;
        transition: 0.3s;
        text-transform: uppercase;
    }
    
    .stButton>button:hover {
        background-color: #333333;
        color: #FFFFFF;
    }

    /* भाड्याचा बॉक्स (Grey Box) */
    .fare-container {
        background-color: #f3f3f3;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #e2e2e2;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# ३. मुख्य टायटल
st.title("🚕 Balaji Logistics")
st.write("तुमचा विश्वसनीय प्रवास सोबती")

# ४. नकाशा (Professional Map View)
df = pd.DataFrame({'lat': [19.9975], 'lon': [73.7898]}) # नाशिकचे लोकेशन
st.map(df)

st.divider()

# ५. प्रवासाची माहिती (Inputs)
st.subheader("📍 राईड बुक करा")
col1, col2 = st.columns(2)
with col1:
    pickup = st.text_input("Pick-up Location", placeholder="उदा. नाशिक")
with col2:
    drop = st.text_input("Drop Location", placeholder="उदा. मुंबई")

# ६. गाडीची निवड आणि वेगवेगळे दर (Rates)
st.write("---")
st.subheader("गाडी निवडा")

car_rates = {
    "🚗 Balaji Go (Mini) - ₹11/km": 11,
    "🚖 Balaji Sedan - ₹14/km": 14,
    "🚐 Balaji SUV (6+1) - ₹17/km": 17
}

selected_car = st.radio("उपलब्ध पर्याय:", list(car_rates.keys()))

# ७. किलोमीटर आणि भाड्याचे गणित
km = st.number_input("अंदाजित अंतर (KM)", min_value=1, value=50)
current_rate = car_rates[selected_car]
total_fare = km * current_rate

# ८. भाड्याचा डिस्प्ले (Uber Style)
st.markdown(f"""
    <div class="fare-container">
        <h2 style='margin:0; color:black;'>₹{total_fare}</h2>
        <p style='margin:0; color:gray;'>अंदाजित भाडे (दर: ₹{current_rate}/किमी)</p>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# ९. कस्टमर डिटेल्स
name = st.text_input("तुमचे नाव")
phone = st.text_input("तुमचा मोबाईल नंबर")

# तुमचा नंबर इथे सेट केला आहे
MY_NUMBER = "9767981986"

if st.button("CONFIRM BOOKING"):
    if name and phone and pickup and drop:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # व्हॉट्सॲप मेसेजचा फॉरमॅट
        msg = (f"🚩 *BALAJI LOGISTICS BOOKING*\n"
               f"--------------------------\n"
               f"👤 नाव: {name}\n"
               f"📞 मोबाईल: {phone}\n"
               f"📍 पिकअप: {pickup}\n"
               f"🏁 ड्रॉप: {drop}\n"
               f"🚗 गाडी: {selected_car.split(' - ')[0]}\n"
               f"🛣️ दर: ₹{current_rate}/km\n"
               f"💰 एकूण भाडे: ₹{total_fare}\n"
               f"⏰ वेळ: {current_time}")
        
        # WhatsApp URL
        whatsapp_url = f"https://wa.me/91{MY_NUMBER}?text={msg.replace(' ', '%20').replace('\n', '%0A')}"
        
        st.balloons()
        st.success("तुमची राईड कन्फर्म झाली आहे! व्हॉट्सॲपवर बुकिंग पाठवा.")
        st.markdown(f"### [👉 येथे क्लिक करा आणि मेसेज पाठवा]({whatsapp_url})")
    else:
        st.error("कृपया सर्व माहिती अचूक भरा!")

# १०. साईडबार सपोर्ट
st.sidebar.markdown(f"### 📞 मदत केंद्र")
st.sidebar.write(f"संपर्क: {MY_NUMBER}")
st.sidebar.info("आमच्या सर्व गाड्या सॅनिटाईझ केलेल्या आणि ड्रायव्हर्स अनुभवी आहेत.")
