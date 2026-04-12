import streamlit as st
import pandas as pd
import os
import hashlib
from datetime import datetime
import urllib.parse
import time

# ================= CONFIG =================
WA_LINK_NO = "919767981986"
CONTACT_NO = "9767981986"
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
if "flash_done" not in st.session_state:
    st.session_state.flash_done = False
if "payment_done" not in st.session_state:
    st.session_state.payment_done = False

# ================= FLASH =================
if not st.session_state.flash_done:
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
        }
        .txt{
            color:#FFBB00;
            font-size:40px;
            font-weight:bold;
            text-align:center;
        }
        </style>

        <div class="flash">
            <div class="txt">
                🚩 BALAJI LOGISTICS
                <br>
                <span style="color:white;font-size:18px;">TOURS & TRAVELS</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        time.sleep(2)

    ph.empty()
    st.session_state.flash_done = True
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

# ================= MAIN =================
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
        <h1 style='text-align:center;color:#FFBB00;'>BALAJI LOGISTICS</h1>
        <h3 style='text-align:center;color:white;'>TOURS & TRAVELS</h3>
        """, unsafe_allow_html=True)

        st.image(
            "https://cdn.pixabay.com/photo/2016/11/18/12/34/car-1835506_1280.jpg",
            use_container_width=True
        )

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

        st.markdown(f"### 💰 Fare: ₹{fare}")

        st.markdown(f"""
        <a href="tel:{CONTACT_NO}">
        <button style="width:100%;padding:10px;background:#FFBB00;border:none;border-radius:10px;">
        📞 CALL NOW
        </button>
        </a>
        """, unsafe_allow_html=True)

        file = None

        if pay == "Online":
            upi = f"upi://pay?pa={UPI_ID}&pn=Balaji&am={fare}&cu=INR"
            st.markdown(f"[Pay Now]({upi})")

            if st.button("Payment Done"):
                st.session_state.payment_done = True

        if pay == "Online" and st.session_state.payment_done:
            file = st.file_uploader("Upload Screenshot", type=["png","jpg","jpeg"])

        if st.button("Confirm Booking"):

            img = ""

            if file:
                os.makedirs("uploads", exist_ok=True)
                img = f"uploads/{datetime.now().strftime('%H%M%S')}_{file.name}"
                with open(img, "wb") as f:
                    f.write(file.getbuffer())

            new = pd.DataFrame([[
                st.session_state.user,
                datetime.now().strftime("%Y-%m-%d %H:%M"),
                s,d,v,fare,pay,mob,img
            ]], columns=BOOKING_COLS)

            old = safe_read(BOOKING_DB, BOOKING_COLS)
            pd.concat([old, new]).to_csv(BOOKING_DB, index=False)

            st.success("Booking Confirmed 🎉")

            msg = f"""
🚩 BALAJI LOGISTICS 🚩
👤 {st.session_state.user}
📍 {s} → {d}
🚗 {v}
💰 ₹{fare}
💳 {pay}
📞 {CONTACT_NO}
"""

            link = urllib.parse.quote(msg)
            st.markdown(f"[📲 WhatsApp]({link})")

    # ================= HISTORY =================
    elif st.session_state.page == "History":

        df = safe_read(BOOKING_DB, BOOKING_COLS)
        user_df = df[df["username"] == st.session_state.user]

        st.subheader("History")

        for _, r in user_df.iterrows():
            st.write(f"🚗 {r['vehicle']} | {r['from_loc']} → {r['to_loc']} | ₹{r['fare']}")

    # ================= ADMIN =================
    elif st.session_state.page == "Admin":

        pw = st.text_input("Admin Password", type="password")

        if pw == ADMIN_PASS:

            df = safe_read(BOOKING_DB, BOOKING_COLS)

            st.metric("Bookings", len(df))
            st.metric("Revenue", df["fare"].sum())

            st.dataframe(df)