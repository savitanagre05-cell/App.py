import streamlit as st
import pandas as pd
import os
import hashlib
from datetime import datetime
import urllib.parse
import time
import requests
from streamlit_lottie import st_lottie

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

# ================= LOTTIE =================
def load_lottie(url):
    try:
        r = requests.get(url)
        return r.json()
    except:
        return None

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

# ================= INIT =================
if not os.path.exists(USER_DB):
    pd.DataFrame(columns=USER_COLS).to_csv(USER_DB, index=False)

if not os.path.exists(BOOKING_DB):
    pd.DataFrame(columns=BOOKING_COLS).to_csv(BOOKING_DB, index=False)

# ================= HASH =================
def make_hash(p):
    return hashlib.sha256(str.encode(p)).hexdigest()

def check_hash(p, h):
    return make_hash(p) == h

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
            background:linear-gradient(135deg,#000,#1a1a1a);
            display:flex;
            justify-content:center;
            align-items:center;
            z-index:9999;
        }
        .txt{
            color:#FFBB00;
            font-size:45px;
            font-weight:bold;
            text-align:center;
            animation: glow 1.5s infinite alternate;
        }
        @keyframes glow {
            from {text-shadow:0 0 10px #FFBB00;}
            to {text-shadow:0 0 25px #FFBB00;}
        }
        .sub{
            color:white;
            font-size:18px;
        }
        </style>

        <div class="flash">
            <div class="txt">
                🚩 BALAJI LOGISTICS
                <div class="sub">TOURS & TRAVELS</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        time.sleep(2.5)

    ph.empty()
    st.session_state.flash = True
    st.session_state.page = "Home"
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

            st.error("Wrong Login")

    else:

        nu = st.text_input("Username")
        nm = st.text_input("Mobile")
        np = st.text_input("Password", type="password")

        if st.button("Register"):
            old = safe_read(USER_DB, USER_COLS)
            new = pd.DataFrame([[nu, make_hash(np), nm]], columns=USER_COLS)
            pd.concat([old, new]).to_csv(USER_DB, index=False)
            st.success("Account Created")

# ================= MAIN APP =================
else:

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        if st.button("Home"):
            st.session_state.page = "Home"
    with c2:
        if st.button("Book"):
            st.session_state.page = "Book"
    with c3:
        if st.button("History"):
            st.session_state.page = "History"
    with c4:
        if st.button("Admin"):
            st.session_state.page = "Admin"

    st.markdown("---")

    # ================= HOME =================
    if st.session_state.page == "Home":

        st.markdown("""
        <h1 style='text-align:center;color:#FFBB00;'>
        🚩 BALAJI LOGISTICS & TOURS
        </h1>

        <h3 style='text-align:center;color:white;'>
        TOURS & TRAVELS
        </h3>

        <h2 style='text-align:center;color:#00ffcc;'>
        🌍 MAHARASHTRA & ALL INDIA SERVICE
        </h2>
        """, unsafe_allow_html=True)

        lottie_car = load_lottie("https://assets10.lottiefiles.com/packages/lf20_car.json")
        st_lottie(lottie_car, height=280)

        st.success("Welcome to Premium Travel Experience 🚗")

    # ================= BOOK =================
    elif st.session_state.page == "Book":

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

            upi = f"upi://pay?pa={UPI_ID}&pn=Balaji&am={fare}&cu=INR"
            st.markdown(f"[💳 Pay Now]({upi})")

            if st.button("✔ Payment Done"):
                st.session_state.payment_done = True
                st.success("Payment Marked")

        if pay == "Online" and st.session_state.payment_done:
            file = st.file_uploader("Upload Screenshot", type=["png","jpg","jpeg"])

        if st.button("Confirm Booking"):

            if pay == "Online" and not st.session_state.payment_done:
                st.warning("Complete Payment First")
                st.stop()

            img = ""

            if file:
                os.makedirs("uploads", exist_ok=True)
                img = f"uploads/{datetime.now().strftime('%H%M%S')}_{file.name}"
                with open(img, "wb") as f:
                    f.write(file.getbuffer())

            new = pd.DataFrame([[
                st.session_state.user,
                datetime.now().strftime("%Y-%m-%d %H:%M"),
                s,d,v,fare,pay,mob,
                img
            ]], columns=BOOKING_COLS)

            old = safe_read(BOOKING_DB, BOOKING_COLS)
            pd.concat([old, new]).to_csv(BOOKING_DB, index=False)

            st.success("Booking Confirmed 🎉")

            msg = (
f"🚩 BALAJI LOGISTICS & TOURS 🚩\n"
f"👤 {st.session_state.user}\n"
f"📍 {s} → {d}\n"
f"🚗 {v}\n"
f"💰 ₹{fare}\n"
f"💳 {pay}\n"
f"🌍 Maharashtra & All India Service"
            )

            link = urllib.parse.quote(msg)
            st.markdown(f"[📲 WhatsApp Send](https://wa.me/{WA_LINK_NO}?text={link})")

            st.session_state.payment_done = False

    # ================= HISTORY =================
    elif st.session_state.page == "History":

        df = safe_read(BOOKING_DB, BOOKING_COLS)
        user_df = df[df["username"]==st.session_state.user]

        st.subheader("Your History")

        for _, r in user_df.iterrows():

            st.write(f"🚗 {r['vehicle']} | {r['from_loc']} → {r['to_loc']} | ₹{r['fare']}")
            if r["screenshot"] != "":
                st.image(r["screenshot"], width=250)

    # ================= ADMIN =================
    elif st.session_state.page == "Admin":

        pw = st.text_input("Admin Password", type="password")

        if pw == ADMIN_PASS:

            df = safe_read(BOOKING_DB, BOOKING_COLS)

            st.metric("Total Bookings", len(df))
            st.metric("Revenue", df["fare"].sum())

            for _, r in df.iterrows():

                st.write(f"👤 {r['username']} | 🚗 {r['vehicle']} | ₹{r['fare']}")
                if r["screenshot"] != "":
                    st.image(r["screenshot"], width=250)