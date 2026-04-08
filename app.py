import streamlit as st
import random, urllib.parse, folium
from streamlit_folium import st_folium

# १. सेटिंग्ज आणि दर
st.set_page_config(page_title="Balaji Logistics", layout="centered", page_icon="🚕")
MY_NO = "9767981986" 
RATE_GO, RATE_SUV = 13, 20 

# २. डेटा व्यवस्थापन
for k, v in {"auth":False, "pg":"Home", "hist":[], "dst":5.0, "rd":{}}.items():
    if k not in st.session_state: st.session_state[k] = v

# ३. नवीन CSS (काळा हेडर आणि प्रीमियम लुक)
st.markdown("<style>.main-header{background:#000;color:#fff;padding:25px;text-align:center;border-radius:0 0 25px 25px;margin-top:-65px;}.card{border:1px solid #eee;padding:15px;border-radius:15px;margin-bottom:12px;box-shadow:0 4px 10px rgba(0,0,0,0.05);}.btn-wa{display:block;background:#25D366;color:white !important;text-align:center;padding:12px;border-radius:10px;text-decoration:none;font-weight:bold;}</style>", unsafe_allow_html=True)

# ४. रजिस्ट्रेशन (पहिले फिचर)
if not st.session_state.auth:
    st.markdown('<div class="main-header"><h1>BALAJI</h1><p>Logistics & Rides</p></div>', unsafe_allow_html=True)
    st.markdown("### 📝 नवीन खाते तयार करा")
    name = st.text_input("पूर्ण नाव", placeholder="उदा. सर्वज्ञ")
    phone = st.text_input("मोबाईल नंबर", max_chars=10, placeholder="98XXXXXXXX")
    if st.button("Register & Start ➔"):
        if name and len(phone) == 10:
            st.session_state.u = {"n": name, "p": phone}
            st.session_state.auth = True
            st.rerun()
        else: st.error("नाव आणि १० अंकी नंबर अचूक भरा.")
else:
    # अ) होम पेज (Real Map + Auto KM Calculation)
    if st.session_state.pg == "Home":
        st.markdown(f"#### नमस्कार, {st.session_state.u['n']}! 👋")
        
        # नाशिकचा नकाशा (Real Map)
        m = folium.Map(location=[19.9975, 73.7898], zoom_start=13)
        folium.Marker([19.9975, 73.7898], icon=folium.Icon(color='black', icon='car', prefix='fa')).add_to(m)
        st_folium(m, height=220, width=700, key="m_nashik")
        
        drop = st.text_input("🏁 डेस्टिनेशन टाका", placeholder="कुठे जायचे आहे?")
        km = random.randint(6, 15) # रँडम किमी हिशोब
        
        st.write(f"📏 अंदाजे अंतर: **{km} किमी**")
        st.write("🚗 **गाडी निवडा (Uber प्रमाणे):**")
        c1, c2 = st.columns(2)
        
        # किलोमीटरनुसार दर (₹१३ आणि ₹२०)
        if c1.button(f"Book Go\n(₹{km*RATE_GO})") and drop:
            st.session_state.rd = {"d":drop, "km":km, "f":km*RATE_GO, "v":"Balaji Go 🚗"}
            st.session_state.pg = "Process"; st.rerun()
            
        if c2.button(f"Book SUV\n(₹{km*RATE_SUV})") and drop:
            st.session_state.rd = {"d":drop, "km":km, "f":km*RATE_SUV, "v":"Balaji SUV 🚐"}
            st.session_state.pg = "Process"; st.rerun()

    # ब) ट्रॅकिंग आणि व्हॉट्सअ‍ॅप
    elif st.session_state.pg == "Process":
        r = st.session_state.rd
        st.info("🔎 ड्रायव्हर शोधत आहोत...")
        msg = urllib.parse.quote(f"🚕 नवीन बुकिंग!\n👤 नाव: {st.session_state.u['n']}\n📍 ड्रॉप: {r['d']}\n📏 अंतर: {r['km']} किमी\n🚗 गाडी: {r['v']}\n💰 भाडे: ₹{r['f']}")
        st.markdown(f'<a href="https://wa.me/91{MY_NO}?text={msg}" target="_blank" class="btn-wa">WhatsApp वर पाठवा 💬</a>', unsafe_allow_html=True)
        
        st.markdown(f"<div class='card'>🚕 ड्रायव्हर **{st.session_state.dst:.1f} किमी** लांब आहे</div>", unsafe_allow_html=True)
        if st.button("अपडेट 🔄"):
            if st.session_state.dst > 0.5: st.session_state.dst -= 1.2; st.rerun()
            else: st.success("✅ ड्रायव्हर पोहोचला!"); st.balloons()

    # क) हिस्ट्री आणि अकाउंट
    elif st.session_state.pg == "Activity":
        st.header("🕒 तुमची हिस्ट्री")
        for h in reversed(st.session_state.hist):
            st.markdown(f"<div class='card'>🏁 {h['d']} | ₹{h['f']}</div>", unsafe_allow_html=True)

    elif st.session_state.pg == "Account":
        st.markdown(f"### 👤 प्रोफाइल: {st.session_state.u['n']}")
        if st.button("Logout"): st.session_state.auth = False; st.rerun()

    # --- खालील बॉटम बटणे (Page Change Fast) ---
    st.markdown("<br><hr>", unsafe_allow_html=True)
    b1, b2, b3 = st.columns(3)
    if b1.button("🏠 Home"): st.session_state.pg = "Home"; st.rerun()
    if b2.button("🕒 Activity"): st.session_state.pg = "Activity"; st.rerun()
    if b3.button("👤 Account"): st.session_state.pg = "Account"; st.rerun()
