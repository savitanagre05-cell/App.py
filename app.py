import streamlit as st
import time
import pandas as pd
import os
import hashlib
from datetime import datetime
import urllib.parse

# ================= CONFIG =================
WA_LINK_NO = "919767981986"
UPI_ID = "9309146504-2@ybl"
ADMIN_PASS = "12345"

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

def check_hashes(password, hashed):
    return make_hashes(password) == hashed

# ================= DB INIT =================
if not os.path.exists(USER_DB):
    pd.DataFrame(columns=['username','password','mobile']).to_csv(USER_DB,index=False)

if not os.path.exists(BOOKING_DB):
    pd.DataFrame(columns=[
        'username','date','from_loc','to_loc',
        'vehicle','fare','pay_mode','cust_mob'
    ]).to_csv(BOOKING_DB,index=False)

# ================= SESSION =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = ""
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "flash_done" not in st.session_state:
    st.session_state.flash_done = False

# ================= FLASH SCREEN =================
if not st.session_state.flash_done:

    placeholder = st.empty()

    with placeholder.container():
        st.markdown("""
        <style>
        .flash{
            position:fixed;
            top:0;left:0;
            width:100vw;
            height:100vh;
            background:black;
            display:flex;
            justify-content:center;
            align-items:center;
            z-index:9999;
        }
        .logo{
            color:#FFBB00;
            font-size:42px;
            font-weight:bold;
            text-align:center;
        }
        </style>

        <div class="flash">
            <div class="logo">
                🚩 BALAJI<br>
                <span style="font-size:18px;color:white;">
                TOURS & TRAVELS
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        time.sleep(2)

    placeholder.empty()
    st.session_state.flash_done = True
    st.rerun()

# ================= LOGIN =================
if not st.session_state.logged_in:

    st.title("🚩 BALAJI LOGISTICS")

    mode = st.radio("Select", ["Login","Register"])

    if mode == "Login":
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")

        if st.button("Login"):
            users = pd.read_csv(USER_DB)

            if u in users['username'].values:
                hashed = users[users['username']==u]['password'].values[0]

                if check_hashes(p, hashed):
                    st.session_state.logged_in = True
                    st.session_state.user = u
                    st.rerun()

            st.error("Wrong details")

    else:
        nu = st.text_input("Username")
        nm = st.text_input("Mobile")
        np = st.text_input("Password", type="password")

        if st.button("Register"):
            pd.DataFrame([[nu,make_hashes(np),nm]],
            columns=['username','password','mobile']
            ).to_csv(USER_DB,mode='a',header=False,index=False)

            st.success("Account created")

# ================= MAIN APP =================
else:

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        if st.button("Book"):
            st.session_state.page = "Book"
    with c2:
        if st.button("History"):
            st.session_state.page = "History"
    with c3:
        if st.button("Admin"):
            st.session_state.page = "Admin"
    with c4:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    st.markdown("---")

    # ================= BOOK =================
    if st.session_state.page == "Book":

        users = pd.read_csv(USER_DB)
        mob = users[users['username']==st.session_state.user]['mobile'].values[0]

        with st.form("booking"):

            s = st.text_input("Pickup Location")
            d = st.text_input("Drop Location")
            v = st.selectbox("Vehicle", list(RATES.keys()))
            km = st.number_input("Distance (KM)", value=50)
            pay = st.radio("Payment", ["Cash","Online"])

            if st.form_submit_button("Confirm Booking"):

                fare = km * RATES[v]

                new_row = pd.DataFrame([[
                    st.session_state.user,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    s,d,v,fare,pay,mob
                ]], columns=[
                    'username','date','from_loc','to_loc',
                    'vehicle','fare','pay_mode','cust_mob'
                ])

                file_exists = os.path.exists(BOOKING_DB)

                new_row.to_csv(
                    BOOKING_DB,
                    mode='a',
                    header=not file_exists,
                    index=False
                )

                st.success(f"Booking Confirmed ₹{fare}")

                # ===== WHATSAPP MESSAGE =====
                msg = (
                    f"🚩 BALAJI TOURS & TRAVELS 🚩\n\n"
                    f"👤 {st.session_state.user}\n"
                    f"📍 {s} → {d}\n"
                    f"🚗 {v}\n"
                    f"💰 ₹{fare}\n"
                    f"💳 {pay}\n"
                    f"🙏 Thank you!"
                )

                encoded = urllib.parse.quote(msg)

                st.markdown(f"[📲 WhatsApp Send](https://wa.me/{WA_LINK_NO}?text={encoded})")

                # ===== ONLINE PAYMENT =====
                if pay == "Online":
                    upi = f"upi://pay?pa={UPI_ID}&pn=Balaji&am={fare}&cu=INR"
                    st.markdown(f"[💳 Pay Now]({upi})")

    # ================= HISTORY =================
    elif st.session_state.page == "History":

        df = pd.read_csv(BOOKING_DB)
        user_df = df[df['username']==st.session_state.user]

        st.subheader("Your Booking History")

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

    # ================= ADMIN =================
    elif st.session_state.page == "Admin":

        st.subheader("Admin Panel 🔐")

        password = st.text_input("Enter Password", type="password")

        if password == ADMIN_PASS:

            df = pd.read_csv(BOOKING_DB)

            if not df.empty:
                st.metric("Total Bookings", len(df))
                st.metric("Total Revenue", df['fare'].sum())
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No Data")

        elif password != "":
            st.error("Wrong Password")