import streamlit as st
import random
import time
import urllib.parse
import folium
from streamlit_folium import st_folium

# --- १. अ‍ॅप कॉन्फिगरेशन ---
st.set_page_config(page_title="Balaji Logistics", layout="centered", page_icon="🚕")

# --- २. तुझे अधिकृत डिटेल्स ---
MY_NO = "9767981986"  
PAYMENT_NO = "9309146504"

# --- ३. सेशन स्टेट ---
if "is_auth" not in st.session_state: st.session_state.is_auth = False
if "user_data" not in st.session_state: st.session_state.user_data = {}
if "step" not in st.session_state: st.session_state.step = "search" 
if "history" not in st.session_state: st.session_state.history = []
if "dist_left" not in st.session_state: st.session_state.dist_left = 5.0

# --- ४. प्रीमियम डिझाईन (CSS) ---
st.markdown(f"""
<style>
    .stApp {{ background-color: #ffffff; }}
    .main-header {{ background: #000; color: #fff; padding: 25px; text-align: center; border-radius: 0 0 25px 25px; margin-top: -65px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }}
    .card {{ border: 1px solid #eee; padding: 18px; border-radius: 15px; margin-bottom: 12px; background: #fff; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }}
    .notif-bar {{ background: #f0f2f6; padding: 10px; border-radius: 8px; border-left: 5px solid #000; margin-bottom: 15px; font-size: 14px; animation: flash 2s infinite; }}
    @keyframes flash {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.5; }} 100% {{ opacity: 1; }} }}
    .btn-call {{ display: block; width: 100%; background: black; color: white !important; text-align: center; padding: 12px; border-radius: 10px; text-decoration: none; font-weight: bold; margin-bottom: 10px; }}
    .btn-wa {{ display: block; width: 100%; background: #25D366; color: white !important; text-align: center; padding: 12px; border-radius: 10px; text-decoration: none; font-weight: bold; }}
</style>
""", unsafe_allow_html=True)

# --- ५. लॉगिन / रजिस्ट्रेशन स्क्रीन ---
def show_registration():
    st.markdown('<div class="main-header"><h1>BALAJI</h1><p>Logistics & Rides</p></div>', unsafe_allow_html=True)
    st.markdown("### 📝 तुमचे खाते तयार करा")
    name = st.text_input("पूर्ण नाव", placeholder="उदा. सर्वज्ञ")
    phone = st.text_input("मोबाईल नंबर", max_chars=10, placeholder="98XXXXXXXX")
    if st.button("सुरू करा ➔"):
        if name and len(phone) == 10:
            st.session_state.user_data = {"name": name, "phone": phone, "joined": "April 2026"}
            st.session_state.is_auth = True
            st.rerun()
        else: st.error("नाव आणि १० अंकी नंबर आवश्यक!")
# --- ६. मुख्य होम स्क्रीन ---
def show_main():
    st.markdown(f"#### नमस्कार, {st.session_state.user_data['name']}! 👋")
    st.markdown('<div class="notif-bar">🔔 Balaji Logistics: २४/७ सेवा उपलब्ध!</div>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["🏠 Home", "🕒 Activity", "👤 Account"])
    with tab1:
        st.write("📍 तुमचे लोकेशन:")
        m = folium.Map(location=[19.9975, 73.7898], zoom_start=13)
        folium.Marker([19.9975, 73.7898], icon=folium.Icon(color='black', icon='car', prefix='fa')).add_to(m)
        st_folium(m, height=220, width=700)
        pickup = st.text_input("📍 पिकअप", value="Nashik City")
        drop = st.text_input("🏁 डेस्टिनेशन")
        st.write("🚗 गाडी निवडा:")
        col1, col2 = st.columns(2)
        dist = random.randint(6, 14)
        fare_go, fare_suv = dist * 13, dist * 20
        with col1:
            st.image("https://img.freepik.com/premium-vector/white-sedan-car-isolated-white-background_53876-64415.jpg", width=110)
            go = st.button(f"Book Go\n₹{fare_go}")
        with col2:
            st.image("https://img.freepik.com/premium-vector/black-suv-car-isolated-white-background_53876-64417.jpg", width=110)
            suv = st.button(f"Book SUV\n₹{fare_suv}")
        if (go or suv) and drop:
            v_name = "Balaji Go 🚗" if go else "Balaji SUV 🚐"
            f_val = fare_go if go else fare_suv
            call_u = f"tel:{st.session_state.user_data['phone']}"
            msg = (f"🚕 *नवीन बुकिंग!* \n👤 नाव: {st.session_state.user_data['name']} \n📍 पिकअप: {pickup} \n📍 ड्रॉप: {drop} \n🚗 गाडी: {v_name} \n💰 भाडे: ₹{f_val} \n📞 कॉल: {call_u}")
            st.session_state.wa_link = f"https://wa.me/91{MY_NO}?text={urllib.parse.quote(msg)}"
            st.session_state.current_ride = {"dest": drop, "fare": f_val, "veh": v_name}
            st.session_state.step = "matching"; st.rerun()
    with tab2:
        for r in reversed(st.session_state.history):
            st.markdown(f"<div class='card'><b>{r['dest']}</b><br>₹{r['fare']}</div>", unsafe_allow_html=True)
    with tab3:
        st.write(f"👤 {st.session_state.user_data['name']}"); st.button("Log Out", on_click=lambda: st.session_state.update({"is_auth": False}))

# --- ७. प्रोसेस स्क्रीन्स ---
def show_process():
    if st.session_state.step == "matching":
        st.markdown(f'<a href="{st.session_state.wa_link}" target="_blank" class="btn-wa">WhatsApp वर मेसेज पाठवा 💬</a>', unsafe_allow_html=True)
        if st.button("मेसेज पाठवला आहे ✅"): st.session_state.step = "onride"; st.rerun()
    elif st.session_state.step == "onride":
        st.markdown(f"<div class='card'><h3>🚕 ड्रायव्हर {st.session_state.dist_left:.1f} किमी लांब आहे</h3></div>", unsafe_allow_html=True)
        st.markdown(f'<a href="tel:{MY_NO}" class="btn-call">📞 कॉल ड्रायव्हर</a>', unsafe_allow_html=True)
        if st.session_state.dist_left > 0.5:
            if st.button("अपडेट करा 🔄"): st.session_state.dist_left -= 1.2; st.rerun()
        else:
            st.success("✅ ड्रायव्हर पोहोचला!"); 
            if st.button("पूर्ण 🏁"): 
                st.session_state.history.append(st.session_state.current_ride)
                st.session_state.step = "search"; st.session_state.dist_left = 5.0; st.balloons(); st.rerun()

# --- ८. रन लॉजिक ---
if not st.session_state.is_auth: show_registration()
elif st.session_state.step != "search": show_process()
else: show_main()


