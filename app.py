import streamlit as st
import time
import pandas as pd
import os
import hashlib
from datetime import datetime
import urllib.parse

# ================= CONFIG =================
WA_LINK_NO = "919767981986"   
CONTACT_NO = "9767981986"     
UPI_ID = "9309146504-2@ybl"  
PHONEPE_NO = "9309146504"

USER_DB = "users_data.csv"    
BOOKING_DB = "balaji_bookings.csv"

RATES = {"WagonR":11, "Swift Dzire":13, "Ertiga":18, "Innova":24, "Tempo Traveller":35}

st.set_page_config(page_title="Balaji Logistics", layout="wide")

# ================= FUNCTIONS =================
def make_hashes(password): return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password, hashed_text): return make_hashes(password) == hashed_text

# ================= DB =================
if not os.path.isfile(USER_DB):
    pd.DataFrame(columns=['username','password','mobile']).to_csv(USER_DB,index=False)

if not os.path.isfile(BOOKING_DB):
    pd.DataFrame(columns=['username','date','from_loc','to_loc','vehicle','fare','pay_mode','cust_mob']).to_csv(BOOKING_DB,index=False)

# ================= SESSION =================
if 'logged_in' not in st.session_state: st.session_state.logged_in=False
if 'user' not in st.session_state: st.session_state.user=""
if 'flash_done' not in st.session_state: st.session_state.flash_done=False
if 'page' not in st.session_state: st.session_state.page="🏠 Home"

# ================= FLASH =================
if not st.session_state.flash_done:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("""
        <style>
        .flash-bg {
            position: fixed;
            top: 0; left: 0;
            width: 100vw; height: 100vh;
            background: black;
            z-index: 9999;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .flash-logo {
            font-size: 50px;
            color: #FFBB00;
            font-weight: bold;
            text-align: center;
        }
        </style>

        <div class="flash-bg">
            <div class="flash-logo">
                🚩 BALAJI<br>
                <span style="font-size:20px;color:white;">
                TOUR'S AND TRAVELS
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        time.sleep(2.5)

    st.session_state.flash_done=True
    placeholder.empty()
    st.rerun()

# ================= UI =================
st.markdown("""
<style>
header, footer, #MainMenu {visibility: hidden;}

.stApp {
    background: linear-gradient(135deg, #000 0%, #0a0a2e 100%);
    color: white;
}

.neon-card {
    background: rgba(255,255,255,0.05);
    padding: 15px;
    border-radius: 15px;
    border: 1px solid #FFBB00;
    margin-bottom: 20px;
}

.stButton>button {
    width: 100%;
    border-radius: 10px;
    border: 1px solid #FFBB00;
    background: #111;
    color: white;
    height: 45px;
    font-weight: bold;
}

.stButton>button:hover {
    background: #FFBB00;
    color: black;
}
</style>
""", unsafe_allow_html=True)

# ================= AUTH =================
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center;color:#FFBB00;'>🚩 BALAJI LOGISTICS</h2>", unsafe_allow_html=True)

    auth = st.radio("निवडा", ["Login","Register"], horizontal=True)

    if auth=="Login":
        u=st.text_input("नाव")
        p=st.text_input("पासवर्ड", type="password")

        if st.button("LOGIN"):
            users=pd.read_csv(USER_DB)
            if u in users['username'].values:
                if check_hashes(p, users[users['username']==u]['password'].values[0]):
                    st.session_state.logged_in=True
                    st.session_state.user=u
                    st.rerun()
            st.error("माहिती चुकीची!")

    else:
        nu=st.text_input("नाव")
        nm=st.text_input("मोबाईल")
        np=st.text_input("पासवर्ड", type="password")

        if st.button("REGISTER"):
            pd.DataFrame([[nu,make_hashes(np),nm]],
            columns=['username','password','mobile']).to_csv(USER_DB,mode='a',header=False,index=False)
            st.success("अकाउंट तयार झाले!")

# ================= MAIN =================
else:
    m1,m2,m3,m4,m5 = st.columns(5)

    with m1:
        if st.button("🏠 Home"): st.session_state.page="🏠 Home"
    with m2:
        if st.button("📅 Book"): st.session_state.page="📅 Book"
    with m3:
        if st.button("📜 Hist"): st.session_state.page="📜 Hist"
    with m4:
        if st.button("👨‍💼 Admin"): st.session_state.page="Admin"
    with m5:
        if st.button("🚪 Out"): st.session_state.logged_in=False; st.rerun()

    st.markdown("---")

    # ===== HOME =====
    if st.session_state.page=="🏠 Home":
        st.markdown("<h2 style='text-align:center;'>🚩 BALAJI LOGISTICS</h2>", unsafe_allow_html=True)
        st.markdown(f"<div class='neon-card'><p>📞 {CONTACT_NO}</p></div>", unsafe_allow_html=True)

    # ===== BOOK =====
    elif st.session_state.page=="📅 Book":
        users_df=pd.read_csv(USER_DB)
        mob=users_df[users_df['username']==st.session_state.user]['mobile'].values[0]

        with st.form("booking"):
            s=st.text_input("Pickup Point")
            d=st.text_input("Drop Point")
            v=st.selectbox("गाडी", list(RATES.keys()))
            km=st.number_input("किमी", value=50)
            pay=st.radio("पेमेंट", ["Cash","Online"], horizontal=True)

            if st.form_submit_button("Confirm Booking ✅"):
                if s and d:
                    fare=km*RATES[v]

                    pd.DataFrame([[st.session_state.user,datetime.now().strftime("%d-%m-%Y"),s,d,v,fare,pay,mob]],
                    columns=['username','date','from_loc','to_loc','vehicle','fare','pay_mode','cust_mob']).to_csv(BOOKING_DB,mode='a',header=False,index=False)

                    raw_msg=f"{s} → {d} | ₹{fare}"
                    encoded_msg=urllib.parse.quote(raw_msg)

                    st.success(f"बुकिंग झाले! भाडे: ₹{fare}")

                    if pay=="Online":
                        st.warning(f"PhonePe: {PHONEPE_NO}")

                        upi=f"upi://pay?pa={UPI_ID}&pn=Balaji&am={fare}&cu=INR"
                        st.markdown(f"<a href='{upi}'><button>💳 Pay with PhonePe</button></a>", unsafe_allow_html=True)

                        uploaded_file = st.file_uploader("📸 Screenshot upload करा", type=["png","jpg","jpeg"])

                        if uploaded_file is not None:
                            if not os.path.exists("payment_screenshots"):
                                os.makedirs("payment_screenshots")

                            path = os.path.join("payment_screenshots", f"{time.time()}.png")

                            with open(path,"wb") as f:
                                f.write(uploaded_file.getbuffer())

                            st.success("Screenshot upload झाला!")

                    st.markdown(f"### [🚀 व्हॉट्सॲपवर पाठवा](https://wa.me/{WA_LINK_NO}?text={encoded_msg})")

                else:
                    st.error("कृपया पिकअप आणि ड्रॉप टाका!")

    # ===== HISTORY =====
    elif st.session_state.page=="📜 Hist":
        df=pd.read_csv(BOOKING_DB)
        st.dataframe(df[df['username']==st.session_state.user])

    # ===== ADMIN =====
    elif st.session_state.page=="Admin":
        st.subheader("👨‍💼 Admin Panel")

        df=pd.read_csv(BOOKING_DB)
        st.dataframe(df)

        st.write("Total Bookings:", len(df))
        st.write("Total Revenue: ₹", df['fare'].sum())

        st.subheader("📸 Screenshots")
        if os.path.exists("payment_screenshots"):
            for f in os.listdir("payment_screenshots"):
                st.image(f"payment_screenshots/{f}", width=200)