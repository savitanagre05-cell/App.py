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
PHONEPE_NO = "9309146504"
UPI_ID = "9309146504-2@ybl"
ADMIN_PASS = "12345"

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
            font-size: 45px;
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

.stButton > button {
    width: 100% !important;
    height: 45px !important;
    border-radius: 10px !important;
    font-weight: bold !important;
    font-size: 13px !important;
    border: 1px solid #FFBB00 !important;
    background-color: #111 !important;
    color: white !important;
}

.stButton > button:hover {
    background-color: #FFBB00 !important;
    color: black !important;
}

/* FULL SCREEN APP */
.block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
}

html, body, .stApp {
    height: 100vh;
    overflow: hidden;
}

section.main {
    overflow: hidden !important;
}

[data-testid="stVerticalBlock"] {
    overflow-y: auto;
    max-height: 85vh;
}

/* menu fix */
div[data-testid="column"] {
    padding: 2px !important;
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

        if st.button("LOGIN", use_container_width=True):
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

        if st.button("REGISTER", use_container_width=True):
            pd.DataFrame([[nu,make_hashes(np),nm]],
            columns=['username','password','mobile']).to_csv(USER_DB,mode='a',header=False,index=False)
            st.success("अकाउंट तयार झाले!")

# ================= MAIN =================
else:
    m1,m2,m3,m4,m5 = st.columns([1,1,1,1,1])

    with m1:
        if st.button("🏠 Home", use_container_width=True): st.session_state.page="🏠 Home"
    with m2:
        if st.button("📅 Book", use_container_width=True): st.session_state.page="📅 Book"
    with m3:
        if st.button("📜 Hist", use_container_width=True): st.session_state.page="📜 Hist"
    with m4:
        if st.button("👨‍💼 Admin", use_container_width=True): st.session_state.page="Admin"
    with m5:
        if st.button("🚪 Out", use_container_width=True): st.session_state.logged_in=False; st.rerun()

    st.markdown("---")

    # ===== BOOK =====
    if st.session_state.page=="📅 Book":
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
                    bid=f"BT{datetime.now().strftime('%d%H%M')}"

                    pd.DataFrame([[st.session_state.user,
                                   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                   s,d,v,fare,pay,mob]],
                    columns=['username','date','from_loc','to_loc','vehicle','fare','pay_mode','cust_mob']
                    ).to_csv(BOOKING_DB,mode='a',header=False,index=False)

                    raw_msg=(f"🚩 *BALAJI TOURS* 🚩\n"
                             f"🆔 ID: {bid}\n"
                             f"👤 {st.session_state.user}\n"
                             f"📞 {mob}\n"
                             f"📍 {s} → {d}\n"
                             f"🚗 {v}\n"
                             f"💰 ₹{fare}\n"
                             f"💳 {pay}")

                    encoded_msg=urllib.parse.quote(raw_msg)

                    st.success(f"बुकिंग झाले! ₹{fare}")

                    if pay=="Online":
                        upi=f"upi://pay?pa={UPI_ID}&pn=Balaji&am={fare}&cu=INR"
                        st.markdown(f"<a href='{upi}'><button>💳 Pay</button></a>", unsafe_allow_html=True)

                    st.markdown(f"[🚀 WhatsApp Send](https://wa.me/{WA_LINK_NO}?text={encoded_msg})")

    # ===== HISTORY =====
    elif st.session_state.page=="📜 Hist":
        try:
            df=pd.read_csv(BOOKING_DB)
        except:
            df=pd.DataFrame()

        user_df=df[df['username']==st.session_state.user]

        if not user_df.empty:
            st.dataframe(user_df[['date','from_loc','to_loc','vehicle','fare','pay_mode']])
        else:
            st.info("तुमची booking नाही")

    # ===== ADMIN =====
    elif st.session_state.page=="Admin":
        st.subheader("👨‍💼 Admin Panel")

        password = st.text_input("Enter Password", type="password")

        if password == ADMIN_PASS:
            st.success("Access Granted")

            try:
                df=pd.read_csv(BOOKING_DB)
            except:
                df=pd.DataFrame()

            if not df.empty:
                st.dataframe(df)
                st.write("Total Bookings:", len(df))
                st.write("Revenue:", df['fare'].sum())
            else:
                st.info("No data")

        elif password != "":
            st.error("Wrong Password")