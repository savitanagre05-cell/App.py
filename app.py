import streamlit as st
import pandas as pd
import os
import hashlib
from datetime import datetime
import urllib.parse
import time

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

# ================= SAFE READ =================
def safe_read(path, cols):
    try:
        df = pd.read_csv(path)
        for c in cols:
            if c not in df.columns:
                return pd.DataFrame(columns=cols)
        return df
    except:
        return pd.DataFrame(columns=cols)

BOOKING_COLS = [
    "username","date","from_loc","to_loc",
    "vehicle","fare","pay_mode","cust_mob",
    "screenshot"
]

USER_COLS = ["username","password","mobile"]

# ================= INIT FILES =================
if not os.path.exists(USER_DB):
    pd.DataFrame(columns=USER_COLS).to_csv(USER_DB, index=False)

if not os.path.exists(BOOKING_DB):
    pd.DataFrame(columns=BOOKING_COLS).to_csv(BOOKING_DB, index=False)

# ================= HASH =================
def make_hash(p):
    return hashlib.sha256(str.encode(p)).hexdigest()

def check_hash(p, hashed):
    return make_hash(p) == hashed

# ================= SESSION =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = ""
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "flash" not in st.session_state:
    st.session_state.flash = False
if "payment_done" not in st.session_state:
    st.session_state.payment_done = False

# ================= FLASH SCREEN =================
if not st.session_state.flash:

    ph = st.empty()

    with ph.container():
        st.markdown("""
        <style>
        .flash{
            position:fixed;
            top:0;left:0;
            width:100vw;height:100vh;
            background:black;
            display:flex;
            justify-content:center;
            align-items:center;
            z-index:9999;
        }
        .txt{
            color:#FFBB00;
            font-size:42px;
            font-weight:bold;
            text-align:center;
        }
        </style>

        <div class="flash">
            <div class="txt">
                🚩 BALAJI<br>
                <span style="font-size:18px;color:white;">TOURS & TRAVELS</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        time.sleep(2)

    ph.empty()
    st.session_state.flash = True
    st.rerun()

# ================= LOGIN =================
if not st.session_state.logged_in:

    st.title("🚩 BALAJI LOGISTICS")

    mode = st.radio("Select", ["Login","Register"])

    if mode == "Login":

        u = st.text_input("Username")
        p = st.text_input("Password", type="password")

        if st.button("Login"):
            users = safe_read(USER_DB, USER_COLS)

            if u in users["username"].values:
                hashed = users[users["username"]==u]["password"].values[0]

                if check_hash(p, hashed):
                    st.session_state.logged_in = True
                    st.session_state.user = u
                    st.rerun()

            st.error("Wrong login")

    else:

        nu = st.text_input("Username")
        nm = st.text_input("Mobile")
        np = st.text_input("Password", type="password")

        if st.button("Register"):

            old = safe_read(USER_DB, USER_COLS)
            new = pd.DataFrame([[nu, make_hash(np), nm]], columns=USER_COLS)

            final = pd.concat([old, new], ignore_index=True)
            final.to_csv(USER_DB, index=False)

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

        users = safe_read(USER_DB, USER_COLS)
        mob = users[users["username"]==st.session_state.user]["mobile"].values[0]

        s = st.text_input("Pickup")
        d = st.text_input("Drop")
        v = st.selectbox("Vehicle", list(RATES.keys()))
        km = st.number_input("KM", value=50)
        pay = st.radio("Payment", ["Cash","Online"])

        fare = km * RATES[v]

        file = None

        if pay == "Online":

            upi_link = f"upi://pay?pa={UPI_ID}&pn=Balaji&am={fare}&cu=INR"
            st.markdown(f"[💳 Pay Now]({upi_link})")

            if st.button("✔ I Have Paid"):
                st.session_state.payment_done = True
                st.success("Payment Done ✅")
                st.balloons()

        # ================= SCREENSHOT UPLOAD =================
        if pay == "Online" and st.session_state.payment_done:

            st.markdown("### 📤 Upload Payment Screenshot")

            file = st.file_uploader("Upload SRC", type=["png","jpg","jpeg"])

        if st.button("Confirm Booking"):

            if pay == "Online" and not st.session_state.payment_done:
                st.warning("Please complete payment first")
                st.stop()

            img_path = ""

            if file is not None:
                os.makedirs("uploads", exist_ok=True)
                img_path = f"uploads/{datetime.now().strftime('%H%M%S')}_{file.name}"
                with open(img_path, "wb") as f:
                    f.write(file.getbuffer())

            new = pd.DataFrame([[
                st.session_state.user,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                s,d,v,fare,pay,mob,
                img_path
            ]], columns=BOOKING_COLS)

            old = safe_read(BOOKING_DB, BOOKING_COLS)
            final = pd.concat([old, new], ignore_index=True)
            final.to_csv(BOOKING_DB, index=False)

            st.success("Booking Confirmed 🎉")

            msg = (
                f"🚩 BALAJI TOURS 🚩\n"
                f"👤 {st.session_state.user}\n"
                f"📍 {s} → {d}\n"
                f"🚗 {v}\n"
                f"💰 ₹{fare}\n"
                f"💳 {pay}"
            )

            link = urllib.parse.quote(msg)
            st.markdown(f"[WhatsApp Send](https://wa.me/{WA_LINK_NO}?text={link})")

    # ================= HISTORY =================
    elif st.session_state.page == "History":

        df = safe_read(BOOKING_DB, BOOKING_COLS)
        user_df = df[df["username"]==st.session_state.user]

        st.subheader("Your History")

        if not user_df.empty:

            for _, row in user_df.iterrows():

                st.markdown(f"""
                🚗 {row['vehicle']}  
                📍 {row['from_loc']} → {row['to_loc']}  
                💰 ₹{row['fare']}  
                📅 {row['date']}
                """)

                if row["screenshot"] != "":
                    st.image(row["screenshot"], width=250)

                st.markdown("---")

        else:
            st.info("No bookings")

    # ================= ADMIN =================
    elif st.session_state.page == "Admin":

        st.subheader("Admin Panel 🔐")

        password = st.text_input("Enter Password", type="password")

        if password == ADMIN_PASS:

            df = safe_read(BOOKING_DB, BOOKING_COLS)

            if not df.empty:

                st.metric("Total Bookings", len(df))
                st.metric("Revenue", df["fare"].sum())

                for _, row in df.iterrows():

                    st.markdown(f"""
                    👤 {row['username']}  
                    🚗 {row['vehicle']}  
                    📍 {row['from_loc']} → {row['to_loc']}  
                    💰 ₹{row['fare']}  
                    📅 {row['date']}
                    """)

                    if row["screenshot"] != "":
                        st.image(row["screenshot"], width=250)

                    st.markdown("---")

            else:
                st.info("No Data")

        elif password != "":
            st.error("Wrong Password")