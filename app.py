import streamlit as st
import random
import folium
import time
from streamlit_folium import st_folium
from streamlit_js_eval import streamlit_js_eval

# १. अ‍ॅप सेटिंग्स
st.set_page_config(page_title="Balaji Logistics", layout="centered")

# २. रिअल GPS लोकेशन
loc = streamlit_js_eval(key='get_location', component_width=0, function_name='getCurrentPosition')

# ३. सर्व स्टेट्स लॉक (Memory Lock)
if "lang" not in st.session_state: st.session_state.lang = "मराठी"
if "is_auth" not in st.session_state: st.session_state.is_auth = False
if "ride_stage" not in st.session_state: st.session_state.ride_stage = "Home" 
if "user_name" not in st.session_state: st.session_state.user_name = "Customer"
if "car_pos_offset" not in st.session_state: st.session_state.car_pos_offset = 0.006
if "otp" not in st.session_state: st.session_state.otp = random.randint(1000, 9999)

MY_NUMBER = "9767981986"

# ४. तुझा ओरिजिनल शब्दकोश (Dictionary)
texts = {
    "मराठी": {
        "title": "बालाजी लॉजिस्टिक", "login": "लॉगिन", "reg": "नोंदणी", "name": "पूर्ण नाव",
        "phone": "मोबाईल नंबर", "from": "कुठून? (Pickup)", "to": "कुठे? (Drop)", 
        "car": "गाडी निवडा", "fare": "एकूण भाडे", "book_btn": "बुकिंग निश्चित करा ✅"
    },
    "English": {
        "title": "Balaji Logistics", "login": "Login", "reg": "Register", "name": "Full Name",
        "phone": "Mobile Number", "from": "From (Pickup)", "to": "To (Drop)", 
        "car": "Select Car", "fare": "Total Fare", "book_btn": "Confirm Booking ✅"
    }
}
T = texts[st.session_state.lang]

# ५. प्रीमियम CSS
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; }
    .header { background: #000; color: #fff; padding: 20px; text-align: center; font-size: 24px; font-weight: bold; border-radius: 0 0 20px 20px; }
    .driver-card { background: white; border-radius: 20px; padding: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); border: 1px solid #eee; margin-top: -40px; position: relative; z-index: 1000; }
    .wa-btn { text-align:center; background-color:#25D366; color:white !important; padding:12px; border-radius:10px; font-weight:bold; text-decoration:none; display:block; margin:10px 0; }
    .stButton>button { width: 100%; background: #000 !important; color: #fff !important; border-radius: 12px !important; height: 50px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ६. लॉगिन सिस्टीम
if not st.session_state.is_auth:
    st.markdown(f"<div class='header'>🚕 {T['title']}</div>", unsafe_allow_html=True)
    st.session_state.lang = st.radio("Language / भाषा", ["मराठी", "English"], horizontal=True)
    n = st.text_input(T['name'])
    p = st.text_input(T['phone'])
    if st.button(T['login']):
        if n and len(p) == 10:
            st.session_state.user_name = n
            st.session_state.is_auth = True
            st.rerun()
    st.stop()

st.markdown(f"<div class='header'>{T['title']}</div>", unsafe_allow_html=True)

# --- स्टेज १: होम आणि बुकिंग (तुझे सर्व जुने ऑप्शन्स इथे आहेत) ---
if st.session_state.ride_stage == "Home":
    st.write(f"### नमस्कार, {st.session_state.user_name}!")
    
    # मॅप
    u_lat = loc['coords']['latitude'] if loc else 20.0022
    u_lon = loc['coords']['longitude'] if loc else 73.7898
    m1 = folium.Map(location=[u_lat, u_lon], zoom_start=15, zoom_control=False)
    folium.CircleMarker([u_lat, u_lon], radius=10, color='blue', fill=True).add_to(m1)
    st_folium(m1, width="100%", height=250, key="h_map")

    # बुकिंग फॉर्म
    p_up = st.text_input(T['from'], value="Current Location")
    d_off = st.text_input(T['to'])
    car = st.selectbox(T['car'], ["🚗 Mini (₹11/km)", "🚖 Sedan (₹14/km)", "🚐 SUV (₹17/km)"])
    km = st.number_input("अंदाजित किमी / Est. KM", min_value=1, value=5)
    
    rate = 11 if "Mini" in car else (14 if "Sedan" in car else 17)
    total = km * rate
    st.info(f"💰 {T['fare']}: ₹{total}")

    if st.button(T['book_btn']):
        if d_off:
            st.session_state.drop_loc = d_off
            st.session_state.total_fare = total
            # मेसेज पाठवणे
            msg = f"🚩 *New Booking*\nCust: {st.session_state.user_name}\nFrom: {p_up}\nTo: {d_off}\nCar: {car}\nFare: ₹{total}\nOTP: {st.session_state.otp}"
            wa_url = f"https://wa.me/91{MY_NUMBER}?text={msg.replace(' ', '%20')}"
            st.markdown(f'<a href="{wa_url}" target="_blank" class="wa-btn">📲 व्हॉट्सॲपवर बुकिंग पाठवा</a>', unsafe_allow_html=True)
            if st.button("मेसेज पाठवला, ट्रॅकिंग सुरू करा ➔"):
                st.session_state.ride_stage = "Tracking"
                st.rerun()

# --- स्टेज २: लाइव्ह ट्रॅकिंग (Uber Style) ---
elif st.session_state.ride_stage == "Tracking":
    u_lat = loc['coords']['latitude'] if loc else 20.0022
    u_lon = loc['coords']['longitude'] if loc else 73.7898
    
    if st.session_state.car_pos_offset > 0:
        st.session_state.car_pos_offset -= 0.0006
        time.sleep(1)
        st.rerun()
    else:
        st.session_state.ride_stage = "Arrived"
        st.rerun()

    m2 = folium.Map(location=[u_lat, u_lon], zoom_start=16, zoom_control=False)
    folium.Marker([u_lat + st.session_state.car_pos_offset, u_lon + st.session_state.car_pos_offset], icon=folium.Icon(color='black', icon='car')).add_to(m2)
    st_folium(m2, width="100%", height=350, key="t_map")

    st.markdown(f"""
    <div class="driver-card">
        <h3>Anil Nagre (MH01BY3960)</h3>
        <p>गाडी तुमच्याकडे येत आहे...</p>
        <div style="text-align:right;">PIN: <b>{st.session_state.otp}</b></div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("पिकअप झाला ➔"): st.session_state.ride_stage = "InTrip"; st.rerun()

# --- स्टेज ३: प्रवासात आणि पूर्ण ---
elif st.session_state.ride_stage == "Arrived":
    st.success("🏁 ड्रायव्हर पोहोचला आहे!")
    if st.button("प्रवास सुरू करा"): st.session_state.ride_stage = "InTrip"; st.rerun()

elif st.session_state.ride_stage == "InTrip":
    st.info(f"🚕 तुम्ही {st.session_state.drop_loc} कडे जात आहात.")
    if st.button("प्रवास पूर्ण करा 🏁"): st.session_state.ride_stage = "Finished"; st.rerun()

elif st.session_state.ride_stage == "Finished":
    st.balloons()
    st.markdown(f"<div style='text-align:center; padding:30px; border:2px solid #000; border-radius:15px;'><h2>बिल: ₹{st.session_state.total_fare}</h2><p>धन्यवाद, {st.session_state.user_name}!</p></div>", unsafe_allow_html=True)
    if st.button("Home 🏠"): 
        st.session_state.ride_stage = "Home"
        st.session_state.car_pos_offset = 0.006
        st.rerun()
