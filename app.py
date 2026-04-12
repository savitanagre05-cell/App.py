import streamlit as st
import pandas as pd
import os
import hashlib
from datetime import datetime
import urllib.parse

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
    "booking_id","username","date","from_loc","to_loc",
    "vehicle","fare","pay_mode","cust_mob","screenshot"
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
for k in ["logged_in","user","page","payment_done"]:
    if k not in st.session_state:
        st.session_state[k] = False if k!="user" and k!="page" else ""

if st.session_state.page == "":
    st.session_state.page = "Home"

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

    # ================= MENU =================
    if st.button("🏠 Home"):
        st.session_state.page = "Home"
    if st.button("🚗 Book"):
        st.session_state.page = "Book"
    if st.button("📜 History"):
        st.session_state.page = "History"
    if st.button("🛠 Admin"):
        st.session_state.page = "Admin"

    st.markdown("---")

    # ================= HOME (FIXED ICON SAFE) =================
    if st.session_state.page == "Home":

        st.markdown("""
        ## BALAJI LOGISTICS & TOURS

        MAHARASHTRA & ALL INDIA SERVICE  
        SAFE • FAST • COMFORTABLE TRAVEL
        """)

        st.image(
            "https://cdn.pixabay.com/photo/2016/11/18/12/34/car-1835506_1280.jpg",
            use_container_width=True
        )

        st.success("WELCOME 🚗 BOOK YOUR RIDE NOW")

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

        st.write("💰 Fare:", fare)

        file = None

        if pay == "Online":
            upi = f"upi://pay?pa={UPI_ID}&pn=Balaji&am={fare}&cu=INR"
            st.markdown(f"[Pay Now]({upi})")

            if st.button("Payment Done"):
                st.session_state.payment_done = True

        if pay == "Online" and st.session_state.payment_done:
            file = st.file_uploader("Upload Screenshot", type=["png","jpg","jpeg"])

        if st.button("Confirm Booking"):

            bid = "BT" + datetime.now().strftime("%d%H%M%S")

            img = ""
            if file:
                os.makedirs("uploads", exist_ok=True)
                img = f"uploads/{datetime.now().strftime('%H%M%S')}_{file.name}"
                with open(img, "wb") as f:
                    f.write(file.getbuffer())

            new = pd.DataFrame([[
                bid,
                st.session_state.user,
                datetime.now().strftime("%Y-%m-%d %H:%M"),
                s,d,v,fare,pay,mob,img
            ]], columns=BOOKING_COLS)

            old = safe_read(BOOKING_DB, BOOKING_COLS)
            pd.concat([old, new]).to_csv(BOOKING_DB, index=False)

            st.success("Booking Confirmed 🎉 ID: " + bid)

            msg = f"""
🚩 BALAJI LOGISTICS & TOURS 🚩
━━━━━━━━━━━━━━━
Booking ID: {bid}
Customer: {st.session_state.user}
Mobile: {mob}
Pickup: {s}
Drop: {d}
Vehicle: {v}
Distance: {km} KM
Fare: ₹{fare}
Payment: {pay}

Thank you for