 
import streamlit as st
import urllib.parse, folium
from streamlit_folium import st_folium

# १. सेटिंग्ज आणि तुझा नंबर/UPI आयडी
st.set_page_config(page_title="Balaji Logistics", layout="centered", page_icon="🚕")
MY_NO = "9767981986" 

# २. सेशन स्टेट (मेमरी) मॅनेजमेंट
if "v_final_all" not in st.session_state:
    st.session_state.clear()
    st.session_state.v_final_all = "1.0"
    st.session_state.auth = False
    st.session_state.pg = "Home"
    st.session_state.hist = []

# ३. प्रीमियम सीएसएस (डिझाइन)
st.markdown("""
<style>
    .main-header {background:#000; color:#fff; padding:25px; text-align:center; border-radius:0 0 25px 25px; margin-top:-65px;}
    .card {background:#f8f9fa; padding:15px; border-radius:15px; border:1px solid #ddd; margin-bottom:10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);}
    .btn-wa {display:block; background:#25D366; color:white !important; text-align:center; padding:12px; border-radius:10px; text-decoration:none; font-weight:bold; margin-bottom:10px;}
    .btn-pay {display:block; background:#5A2D82; color:white !important; text-align:center; padding:12px; border-radius:10px; text-decoration:none; font-weight:bold;}
    .stButton>button {width:100%; border-radius:10px;}
</style>
""", unsafe_allow_html=True)

# ४. लॉगिन / रजिस्ट्रेशन स्क्रीन
if not st.session_state.auth:
    st.markdown('<div class="main-header"><h1>BALAJI</h1><p>Logistics & Rides</p></div>', unsafe_allow_html=True)
    st.markdown("### 📝 लॉगिन करा")
    name = st.text_input("तुमचे पूर्ण नाव")
    phone = st.text_input("मोबाईल नंबर", max_chars=10)
    if st.button("सुरू करा ➔"):
        if name and len(phone) == 10:
            st.session_state.u = {"n": name, "p": phone}
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("कृपया नाव आणि योग्य नंबर टाका.")

else:
    # अ) होम पेज - बुकिंग आणि कॅल्क्युलेटर
    if st.session_state.pg == "Home":
        st.markdown(f"#### नमस्कार, {st.session_state.u['n']}! 👋")
        
        # नाशिक मॅप (Visual Feature)
        m = folium.Map(location=[19.9975, 73.7898], zoom_start=13)
        folium.Marker([19.9975, 73.7898], popup="Balaji Office").add_to(m)
        st_folium(m, height=220, width=700, key="nashik_map_final")
        
        st.markdown("### 💰 भाडे हिशोब (Manual Input)")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        drop_loc = st.text_input("🏁 कुठे जायचे आहे?", placeholder="उदा. सातपूर, नाशिक")
        
        col1, col2 = st.columns(2)
        with col1:
            km_in = st.number_input("📏 किलोमीटर", min_value=1.0, step=0.5, value=10.0)
        with col2:
            rate_in = st.number_input("💵 दर (₹/KM)", min_value=1, step=1, value=13)
        
        total_fare = km_in * rate_in
        st.subheader(f"एकूण भाडे: ₹{total_fare} /-")
        
        p_mode = st.radio("💳 पेमेंटची पद्धत निवडा:", ["रोख (Cash)", "ऑनलाईन (PhonePe/GPay)"])
        
        if st.button("बुकिंग कन्फर्म करा ➔"):
            if drop_loc:
                st.session_state.rd = {"d": drop_loc, "km": km_in, "f": total_fare, "r": rate_in, "pm": p_mode}
                st.session_state.pg = "Process"
                st.rerun()
