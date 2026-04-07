import streamlit as st
import random
import folium
import time
from streamlit_folium import st_folium
from streamlit_js_eval import streamlit_js_eval

# १. अ‍ॅप सेटिंग्स (Mobile Optimized)
st.set_page_config(page_title="Balaji Logistics Live", page_icon="🚕", layout="centered")

# २. रिअल GPS लोकेशन मिळवणे
loc = streamlit_js_eval(key='get_location', component_width=0, function_name='getCurrentPosition')

# ३. मेमरी लॉक (Persistence) - अ‍ॅप बंद करून उघडलं तरी राईड सुरूच राहील
if "is_auth" not in st.session_state: st.session_state.is_auth = False
if "ride_stage" not in st.session_state: st.session_state.ride_stage = "Home" 
if "user_name" not in st.session_state: st.session_state.user_name = "Customer"
if "otp" not in st.session_state: st.session_state.otp = random.randint(1000, 9999)
if "car_pos_offset" not in st.session_state: st.session_state.car_pos_offset = 0.006

MY_NUMBER = "9767981986"

# ४. अल्ट्रा-प्रो प्रीमियम CSS
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; }
    .uber-header { background: #000; color: #fff; padding: 20px; text-align: center; font-size: 24px; font-weight: bold; border-radius: 0 0 25px 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
    .driver-card { background: white; border-radius: 20px; padding: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); border: 1px solid #eee; margin-top: -60px; position: relative; z-index: 1000; }
    .otp-box { background: #000; color: #fff; padding: 8px 15px; border-radius: 10px; font-weight: bold; font-size: 22px; }
    .wa-btn { text-align:center; background-color:#25D366; color:white !important; padding:15px; border-radius:12px; font-weight:bold; text-decoration:none; display:block; margin:15px 0; font-size:18px; }
    .stButton>button { width: 100%; background: #000 !important; color: #fff !important; border-radius: 15px !important; height: 55px; font-weight: bold; font-size: 18px; border: none; }
    .info-box { background: #f8f9fa; padding: 15px; border-radius: 15px; border-left: 6px solid #000; margin: 15px 0; }
</style>
""", unsafe_allow_html=True)

# ५. लॉगिन (एकदाच)
if not st.session_state.is_auth:
    st.markdown("<div class='uber-header'>🚕 Balaji Logistics</div>", unsafe_allow_html=True)
    st.write("<br>", unsafe_allow_html=True)
    name = st.text_input("तुमचे नाव टाका")
    phone = st.text_input("मोबाईल नंबर (१० अंकी)")
    if st.button("Log In ➔"):
        if name and len(phone) == 10:
            st.session_state.user_name = name
            st.session_state.is_auth = True
            st.rerun()
    st.stop()

# मुख्य अ‍ॅप हेडर
st.markdown("<div class='uber-header'>Balaji Logistics</div>", unsafe_allow_html=True)

# --- स्टेज १: होम आणि बुकिंग ---
if st.session_state.ride_stage == "Home":
    st.write(f"### नमस्कार, {st.session_state.user_name}! 👋")
    
    # रिअल लोकेशन मॅप
    u_lat = loc['coords']['latitude'] if loc else 20.0022
    u_lon = loc['coords']['longitude'] if loc else 73.7898
    m1 = folium.Map(location=[u_lat, u_lon], zoom_start=15, zoom_control=False)
    folium.CircleMarker([u_lat, u_lon], radius=10, color='blue', fill=True, fill_opacity=0.7).add_to(m1)
    st_folium(m1, width="100%", height=250, key="home_map")

    drop = st.text_input("🏁 तुम्हाला कुठे जायचे आहे?", placeholder="उदा. नाशिक रोड स्टेशन")
    
    st.markdown("<b>उपलब्ध गाडी:</b>", unsafe_allow_html=True)
    st.markdown('<div style="background:#f1f1f1; padding:15px; border-radius:15px; display:flex; justify-content:space-between; align-items:center;"><div>🚖 <b>Sedan - Anil Nagre</b><br><small>जवळपास १ मिनीट</small></div><div style="font-size:20px; font-weight:bold;">₹220</div></div>', unsafe_allow_html=True)

    if st.button("Confirm Balaji Ride ✅"):
        if drop:
            st.session_state.drop_loc = drop
            # व्हॉट्सॲप मेसेज तयार करणे
            msg = f"🚩 *New Booking*\n👤 Cust: {st.session_state.user_name}\n📍 To: {drop}\n🚕 Driver: Anil Nagre\n🔢 OTP: {st.session_state.otp}"
            wa_url = f"https://wa.me/91{MY_NUMBER}?text={msg.replace(' ', '%20')}"
            
            st.success("पिकअप कंफर्म करण्यासाठी खालील बटण दाबा!")
            st.markdown(f'<a href="{wa_url}" target="_blank" class="wa-btn">📲 व्हॉट्सॲप मेसेज पाठवा</a>', unsafe_allow_html=True)
            
            if st.button("मेसेज पाठवला, राईड ट्रॅक करा ➔"):
                st.session_state.ride_stage = "DriverComing"
                st.rerun()

# --- स्टेज २: रिअल-टाइम ट्रॅकिंग (Active Mode) ---
elif st.session_state.ride_stage == "DriverComing":
    u_lat = loc['coords']['latitude'] if loc else 20.0022
    u_lon = loc['coords']['longitude'] if loc else 73.7898
    
    # गाडीची हालचाल (Animation Logic)
    if st.session_state.car_pos_offset > 0:
        st.session_state.car_pos_offset -= 0.0007 # गाडी जवळ येतेय
        time.sleep(1) # दर सेकंदाला रिफ्रेश
        st.rerun()
    else:
        st.session_state.ride_stage = "Arrived"
        st.rerun()

    m2 = folium.Map(location=[u_lat, u_lon], zoom_start=16, zoom_control=False)
    # युजरचे लोकेशन
    folium.CircleMarker([u_lat, u_lon], radius=10, color='blue', fill=True).add_to(m2)
    # ड्रायव्हर अनिल नागरे यांची गाडी
    folium.Marker([u_lat + st.session_state.car_pos_offset, u_lon + st.session_state.car_pos_offset], 
                  icon=folium.Icon(color='black', icon='car', prefix='fa')).add_to(m2)
    st_folium(m2, width="100%", height=350, key="live_tracking")

    # अंतर आणि वेळ दाखवणे
    dist = int(st.session_state.car_pos_offset * 100000)
    st.markdown(f"""
    <div class="driver-card">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div><h3>Anil Nagre</h3><p style="color:#E67E22; margin:0;"><b>MH01BY3960</b> • Swift</p></div>
            <div style="text-align:center;"><small>PIN</small><div class="otp-box">{st.session_state.otp}</div></div>
        </div>
        <div class="info-box">📏 अंतर: <b>{max(0, dist)} मीटर</b> | ⏱️ वेळ: <b>१ मिनीट</b></div>
        <p style="text-align:center; color:green; font-weight:bold;">🚕 ड्रायव्हर पिकअपसाठी येत आहे...</p>
    </div>
    """, unsafe_allow_html=True)

# --- स्टेज ३: अराईव्हड आणि इन-ट्रिप ---
elif st.session_state.ride_stage == "Arrived":
    st.success("🏁 अनिल नागरे तुमच्या लोकेशनवर पोहोचले आहेत!")
    st.image("https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?auto=format&fit=crop&w=800")
    if st.button("प्रवास सुरू करा (Start Trip) ➔"):
        st.session_state.ride_stage = "InTrip"
        st.rerun()

elif st.session_state.ride_stage == "InTrip":
    st.info(f"🚕 तुम्ही सध्या {st.session_state.drop_loc} कडे जात आहात.")
    st.markdown("### 🛣️ प्रवास सुरू आहे...")
    if st.button("प्रवास पूर्ण झाला 🏁"):
        st.session_state.ride_stage = "Finished"
        st.rerun()

# --- स्टेज ४: फायनल बिल ---
elif st.session_state.ride_stage == "Finished":
    st.balloons()
    st.markdown(f"""
    <div style="text-align:center; padding:30px; border:2px solid #000; border-radius:20px;">
        <h2 style="color:green;">प्रवास यशस्वी! ✅</h2>
        <p>भाडे: <b>₹220</b></p>
        <p>ड्रायव्हर: Anil Nagre (MH01BY3960)</p>
        <hr>
        <h4>Balaji Logistics वापरल्याबद्दल धन्यवाद!</h4>
    </div>
    """, unsafe_allow_html=True)
    if st.button("परत होम पेजवर 🏠"):
        st.session_state.ride_stage = "Home"
        st.session_state.car_pos_offset = 0.006
        st.rerun()
