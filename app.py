
import streamlit as st
import random
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import streamlit_js_eval

# १. अ‍ॅप सेटिंग्स
st.set_page_config(page_title="Balaji Logistics", page_icon="🚕", layout="wide")

# २. युजरचे रिअल GPS लोकेशन
loc = streamlit_js_eval(key='get_location', component_width=0, function_name='getCurrentPosition')

# ३. स्टेट मॅनेजमेंट (सगळं मिक्स केलंय)
if "lang" not in st.session_state: st.session_state.lang = "मराठी"
if "is_auth" not in st.session_state: st.session_state.is_auth = False
if "page" not in st.session_state: st.session_state.page = "🏠 Home"
if "booking_status" not in st.session_state: st.session_state.booking_status = "Search"
if "ride_stage" not in st.session_state: st.session_state.ride_stage = "Waiting" # Waiting, Started, Completed
if "otp" not in st.session_state: st.session_state.otp = random.randint(1000, 9999)
if "user_name" not in st.session_state: st.session_state.user_name = "Customer"

# ४. शब्दकोश
texts = {
    "मराठी": {"login": "Login", "reg": "Register", "name": "पूर्ण नाव", "phone": "मोबाईल नंबर", "from": "Pickup", "to": "Drop", "book_btn": "Confirm Booking"},
    "English": {"login": "Login", "reg": "Register", "name": "Full Name", "phone": "Mobile Number", "from": "Pickup", "to": "Drop", "book_btn": "Confirm Booking"}
}
T = texts[st.session_state.lang]
MY_NUMBER = "9767981986"

# ५. अल्ट्रा प्रीमियम CSS
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF !important; }
    .app-header { background-color: #000; color: #FFF !important; padding: 20px; text-align: center; font-size: 24px; font-weight: bold; border-radius: 0 0 20px 20px; }
    .stButton>button { width: 100%; background-color: #000 !important; color: #FFF !important; border-radius: 12px !important; height: 50px; font-weight: bold; }
    .driver-card { background: white; border-radius: 20px; padding: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border: 1px solid #eee; margin-top: -30px; position: relative; z-index: 99; }
    .otp-tag { background: #000; color: #fff; padding: 5px 10px; border-radius: 8px; font-weight: bold; }
    label, p, h3 { color: #000 !important; font-weight: bold !important; }
</style>
""", unsafe_allow_html=True)

# ६. ऑथेंटिकेशन
if not st.session_state.is_auth:
    st.markdown("<div class='app-header'>🚕 Balaji Logistics</div>", unsafe_allow_html=True)
    mode = st.radio("Select", ["Login", "Register"], horizontal=True)
    u_p = st.text_input("Mobile Number")
    if mode == "Register": u_n = st.text_input("Name")
    if st.button("Proceed ➔"):
        if len(u_p) == 10:
            if mode == "Register": st.session_state.user_name = u_n
            st.session_state.is_auth = True
            st.rerun()
    st.stop()

st.markdown("<div class='app-header'>Balaji Logistics</div>", unsafe_allow_html=True)

# --- राईड स्टेज नुसार पेजेस (NEXT PAGE LOGIC) ---

# स्टेज १: ड्रायव्हरची वाट बघणे (Booking Confirmed)
if st.session_state.booking_status == "Confirmed" and st.session_state.ride_stage == "Waiting":
    u_lat = loc['coords']['latitude'] if loc else 20.0022
    u_lon = loc['coords']['longitude'] if loc else 73.7898
    m = folium.Map(location=[u_lat, u_lon], zoom_start=16)
    folium.CircleMarker([u_lat, u_lon], radius=8, color='blue', fill=True).add_to(m)
    folium.Marker([u_lat + 0.001, u_lon + 0.001], icon=folium.Icon(color='black', icon='car', prefix='fa')).add_to(m)
    st_folium(m, width="100%", height=300)

    st.markdown(f"""
    <div class="driver-card">
        <div style="display:flex; justify-content:space-between;">
            <div><h3>Anil Nagre</h3><p style="color:#E67E22;">MH01BY3960</p></div>
            <div style="text-align:center;"><small>OTP</small><div class="otp-tag">{st.session_state.otp}</div></div>
        </div>
        <p style="color:green; text-align:center;">🚕 ड्रायव्हर पिकअपसाठी येत आहे...</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("<br>", unsafe_allow_html=True)
    if st.button("🏁 Start Ride (पिकअप झाला)"):
        st.session_state.ride_stage = "Started"
        st.rerun()

# स्टेज २: प्रवास सुरू (Next Page After Pickup)
elif st.session_state.ride_stage == "Started":
    st.info("🚕 तुमचा प्रवास सुरक्षितपणे सुरू आहे...")
    st.image("https://images.unsplash.com/photo-1514316454349-750a7fd3da3a?auto=format&fit=crop&w=800")
    
    st.markdown(f"""
    <div style="background:#f9f9f9; padding:20px; border-radius:15px; border:2px solid #000;">
        <h4>प्रवास सुरू आहे...</h4>
        <p>ड्रायव्हर: Anil Nagre</p>
        <p>गाडी: MH01BY3960</p>
        <hr>
        <p>लक्ष्य: {st.session_state.get('drop_loc', 'तुमचे ड्रॉप लोकेशन')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("✅ राईड संपवा (Drop Success)"):
        st.session_state.ride_stage = "Completed"
        st.rerun()

# स्टेज ३: राईड पूर्ण (Final Bill Page)
elif st.session_state.ride_stage == "Completed":
    st.balloons()
    st.success("प्रवास पूर्ण झाला! भेट दिल्याबद्दल धन्यवाद. 🙏")
    st.markdown(f"""
    <div style="text-align:center; padding:30px; border:2px dashed #000; border-radius:20px;">
        <h2>FINAL BILL</h2>
        <p>Customer: {st.session_state.user_name}</p>
        <p>Total Fare: ₹{st.session_state.get('fare', 0)}</p>
        <p>Driver: Anil Nagre (MH01BY3960)</p>
        <h3 style="color:green;">Paid via Cash/UPI</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🏠 परत होम पेजवर जा"):
        st.session_state.booking_status = "Search"
        st.session_state.ride_stage = "Waiting"
        st.session_state.page = "🏠 Home"
        st.rerun()

# --- मुख्य होम पेज (जर बुकिंग नसेल तर) ---
else:
    if st.session_state.page == "🏠 Home":
        st.markdown(f"### नमस्कार, {st.session_state.user_name}! 👋")
        st.image("https://images.unsplash.com/photo-1559297434-2d8a1e02a01d?auto=format&fit=crop&w=800")
        if st.button("Book Ride Now ➔"): st.session_state.page = "🚕 Book"; st.rerun()

    elif st.session_state.page == "🚕 Book":
        p_up = st.text_input(T['from'], value="Current Location" if loc else "")
        d_off = st.text_input(T['to'])
        car = st.selectbox("Car Type", ["🚗 Mini", "🚖 Sedan", "🚐 SUV"])
        km = st.number_input("Est. KM", min_value=1, value=5)
        total = km * (11 if "Mini" in car else (14 if "Sedan" in car else 17))
        st.session_state.fare = total
        st.session_state.drop_loc = d_off
        
        if st.button(T['book_btn']):
            msg = f"🚩 *New Booking*\nDriver: Anil Nagre\nFrom: {p_up}\nTo: {d_off}\nTotal: ₹{total}"
            wa_url = f"https://wa.me/91{MY_NUMBER}?text={msg.replace(' ', '%20')}"
            st.markdown(f'<meta http-equiv="refresh" content="0;URL={wa_url}">', unsafe_allow_html=True)
            st.session_state.booking_status = "Confirmed"; st.rerun()

# ८. बॉटम नेव्हिगेशन
if st.session_state.ride_stage == "Waiting":
    st.write("<br><br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("🏠"): st.session_state.page = "🏠 Home"; st.rerun()
    with c2: 
        if st.button("🚕"): st.session_state.page = "🚕 Book"; st.rerun()
    with c3: 
        if st.button("👤"): st.session_state.is_auth = False; st.rerun()
