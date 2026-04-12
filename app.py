import streamlit as st
import time
import pandas as pd
import os
import hashlib
from datetime import datetime
import urllib.parse

# ================= CONFIG =================
WA_LINK_NO = "919767981986"
PHONEPE_NO = "9309146504"
UPI_ID = "9309146504-2@ybl"

ADMIN_PASS = "12345"
ADMIN_USER = "BalajiAdmin"   # 🔒 only you can access admin

USER_DB = "users_data.csv"
BOOKING_DB = "balaji_bookings.csv"

RATES = {
    "WagonR": 11,
    "Swift Dzire": 13,
    "Ertiga": 18,
    "Innova": 24,
    "Tempo Traveller": 35
}

st.set_page_config(page_title="Balaji Logistics", layout="wide")

# ================= FUNCTIONS =================
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

# ================= DB INIT =================
if not os.path.isfile(USER_DB):
    pd.DataFrame(columns=['username','password','mobile']).to_csv(USER_DB,index=False)

if not os.path.isfile(BOOKING_DB):
    pd.DataFrame(columns=[
        'username','date','from_loc','to_loc',
        'vehicle','fare','pay_mode','cust_mob'
    ]).to_csv(BOOKING_DB,index=False)

# ================= SESSION =================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in=False
if 'user' not in st.session_state:
    st.session_state.user=""
if 'page' not in st.session_state:
    st.session_state.page="Home"
if 'flash_done' not in st.session_state:
    st.session_state.flash_done=False

# ================= FLASH SCREEN =================
if not st.session_state.flash_done:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("""
        <style>
        .flash-bg{
            position:fixed;top:0;left:0;
            width:100vw;height:100vh;
            background:black;
            display:flex;
            justify-content:center;
            align-items:center;
            z-index:9999;
        }
        .flash-logo{
            color:#FFBB00;
            font-size:40px;
            font-weight:bold;
            text-align:center;
        }
        </style>

        <div class="flash-bg">
            <div class="flash-logo">
                🚩 BALAJI<br>
                <span style="font-size:18px;color:white;">
                TOURS & TRAVELS
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        time.sleep(2)

    st.session_state.flash_done=True
    placeholder.empty()
    st.rerun()

# ================= UI STYLE =================
st.markdown("""
<style>
header, footer, #MainMenu {visibility:hidden;}

.stButton > button {
    width:100% !important;
    height:45px !important;
    border-radius:10px !important;
    background:#111 !important;
    color:white !important;
    border:1px solid #FFBB00 !important;
    font-weight:bold;
}

.stButton > button:hover {
    background:#FFBB00 !important;
    color:black !important;
}

.block-container{
    padding-top:0rem;
}
</style>
""", unsafe_allow_html=True)

# ================= LOGIN =================
if not st.session_state.logged_in:

    st.markdown("<h2 style='text-align:center;color:#FFBB00;'>🚩 BALAJI LOGISTICS</h2>", unsafe_allow_html=True)

    mode = st.radio("निवडा", ["Login","Register"], horizontal=True)

    if mode=="Login":
        u = st.text_input("नाव")
        p = st.text_input("पासवर्ड", type="password")

        if st.button("LOGIN"):
            users = pd.read_csv(USER_DB)

            if u in users['username'].values:
                if check_hashes(p, users[users['username']==u]['password'].values[0]):
                    st.session_state.logged_in=True
                    st.session_state.user=u
                    st.rerun()

            st.error("चुकीची माहिती!")

    else:
        nu = st.text_input("नाव")
        nm = st.text_input("मोबाईल")
        np = st.text_input("पासवर्ड", type="password")

        if st.button("REGISTER"):
            pd.DataFrame([[nu,make_hashes(np),nm]],
            columns=['username','password','mobile']
            ).to_csv(USER_DB,mode='a',header=False,index=False)

            st.success("Account तयार झाले!")

# ================= MAIN APP =================
else:

    c1,c2,c3,c4,c5 = st.columns(5)

    with c1:
        if st.button("Home"): st.session_state.page="Home"
    with c2:
        if st.button("Book"): st.session_state.page="Book"
    with c3:
        if st.button("History"): st.session_state.page="Hist"
    with c4:
        if st.button("Admin"): st.session_state.page="Admin"
    with c5:
        if st.button("Logout"):
            st.session_state.logged_in=False
            st.rerun()

    st.markdown("---")

    # ================= BOOK =================
    if st.session_state.page=="Book":

        users = pd.read_csv(USER_DB)
        mob = users[users['username']==st.session_state.user]['mobile'].values[0]

        with st.form("booking"):
            s = st.text_input("Pickup")
            d = st.text_input("Drop")
            v = st.selectbox("Vehicle", list(RATES.keys()))
            km = st.number_input("KM", value=50)
            pay = st.radio("Payment", ["Cash","Online"])

            if st.form_submit_button("Confirm Booking"):
                fare = km * RATES[v]

                pd.DataFrame([[
                    st.session_state.user,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    s,d,v,fare,pay,mob
                ]], columns=[
                    'username','date','from_loc','to_loc',
                    'vehicle','fare','pay_mode','cust_mob'
                ]).to_csv(BOOKING_DB,mode='a',header=False,index=False)

                msg = f"""
🚩 BALAJI TOURS
👤 {st.session_state.user}
📍 {s} → {d}
🚗 {v}
💰 ₹{fare}
"""

                link = urllib.parse.quote(msg)

                st.success("Booking Done!")

                st.markdown(f"[WhatsApp Send](https://wa.me/{WA_LINK_NO}?text={link})")

    # ================= HISTORY (USER) =================
    elif st.session_state.page=="Hist":

        df = pd.read_csv(BOOKING_DB)
        user_df = df[df['username']==st.session_state.user]

        st.subheader("Your History")

        if not user_df.empty:

            st.metric("Total Bookings", len(user_df))
            st.metric("Total Spent", user_df['fare'].sum())

            user_df = user_df.sort_values("date", ascending=False)

            for _, row in user_df.iterrows():
                st.markdown(f"""
                🚗 **{row['vehicle']}**  
                📍 {row['from_loc']} → {row['to_loc']}  
                💰 ₹{row['fare']}  
                📅 {row['date']}
                ---
                """)

        else:
            st.info("No bookings yet")

    # ================= ADMIN (SECURE) =================
    elif st.session_state.page=="Admin":

        st.subheader("Admin Panel 🔐")

        # 🔒 HARD LOCK
        if st.session_state.user != ADMIN_USER:
            st.error("No Access")
            st.stop()

        password = st.text_input("Enter Password", type="password")

        if password == ADMIN_PASS:

            df = pd.read_csv(BOOKING_DB)

            if not df.empty:
                st.metric("Total Bookings", len(df))
                st.metric("Revenue", df['fare'].sum())
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No Data")

        elif password != "":
            st.error("Wrong Password")