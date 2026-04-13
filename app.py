import streamlit as st
import pandas as pd
import os
import hashlib
from datetime import datetime
import urllib.parse
import time

# ================= CONFIG =================
WA_LINK_NO = "919767981986"
ADMIN_PASS = "12345"
UPI_ID = "9309146504-2@ybl"

USER_DB = "users.csv"
BOOKING_DB = "bookings.csv"

RATES = {
    "WagonR": 11,
    "Swift Dzire": 13,
    "Ertiga": 18,
    "Innova": 24,
    "Tempo Traveller": 35
}

st.set_page_config(page_title="Balaji Logistics", layout="wide")

# ================= UI STYLE =================
st.markdown("""
<style>
body { background-color:#0e0e0e; }
.stButton>button {
    width:100%;
    border-radius:10px;
    height:45px;
    font-size:16px;
    background:#FFBB00;
    color:black;
}
</style>
""", unsafe_allow_html=True)

# ================= FLASH =================
if "flash_done" not in st.session_state:
    st.session_state.flash_done = False

if not st.session_state.flash_done:
    flash = st.empty()
    flash.markdown("""
<div style="text-align:center;padding:80px;background:#111;border-radius:20px;">
<h1 style="color:#FFBB00;font-size:38px;white-space:nowrap;">🚩 BALAJI LOGISTICS</h1>
<h3 style="color:white;">& TOURS & TRAVELS</h3>
<p style="color:white;">🌍 Maharashtra & All India Service</p>
<p style="color:white;">🚗 Safe • Fast • Comfortable</p>
</div>
""", unsafe_allow_html=True)

    time.sleep(2)
    flash.empty()
    st.session_state.flash_done = True
    st.rerun()

# ================= INIT =================
USER_COLS = ["username","password","mobile"]
BOOKING_COLS = ["booking_id","username","date","from_loc","to_loc","vehicle","fare","payment","mobile","screenshot"]

if not os.path.exists(USER_DB):
    pd.DataFrame(columns=USER_COLS).to_csv(USER_DB, index=False)

if not os.path.exists(BOOKING_DB):
    pd.DataFrame(columns=BOOKING_COLS).to_csv(BOOKING_DB, index=False)

def safe_read(path, cols):
    try:
        df = pd.read_csv(path)
        for c in cols:
            if c not in df.columns:
                return pd.DataFrame(columns=cols)
        return df
    except:
        return pd.DataFrame(columns=cols)

def hash_pw(p):
    return hashlib.sha256(str.encode(p)).hexdigest()

def check_pw(p, h):
    return hash_pw(p) == h

for k in ["logged_in","user","page"]:
    if k not in st.session_state:
        st.session_state[k] = False if k=="logged_in" else ""

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
                if check_pw(p, users[users["username"]==u]["password"].values[0]):
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
            new = pd.DataFrame([[nu, hash_pw(np), nm]], columns=USER_COLS)
            pd.concat([old, new]).to_csv(USER_DB, index=False)
            st.success("Account Created")

# ================= MAIN =================
else:

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.button("🏠 Home", on_click=lambda: st.session_state.update(page="Home"))

    with col2:
        st.button("🚗 Book", on_click=lambda: st.session_state.update(page="Book"))

    with col3:
        st.button("📜 History", on_click=lambda: st.session_state.update(page="History"))

    with col4:
        st.button("🛠 Admin", on_click=lambda: st.session_state.update(page="Admin"))

    with col5:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.user = ""
            st.rerun()

    st.markdown("---")

    # HOME
    if st.session_state.page == "Home":

        st.markdown("""
<div style="background:#1a1a1a;padding:25px;border-radius:15px;text-align:center;">
<h2 style="color:#FFBB00;">🚩 BALAJI LOGISTICS & TOURS</h2>
<p style="color:white;">🌍 Maharashtra & All India Service</p>
<p style="color:white;">🚗 Safe • Fast • Comfortable Ride</p>
</div>
""", unsafe_allow_html=True)

        st.image("https://cdn.pixabay.com/photo/2016/11/18/12/34/car-1835506_1280.jpg", use_container_width=True)
        st.success("WELCOME 🚗 BOOK YOUR RIDE NOW")

    # BOOK
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

            st.subheader("💳 Online Payment")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("📱 GPay"):
                    st.markdown(f"[Pay](upi://pay?pa={UPI_ID}&pn=Balaji&am={fare}&cu=INR)")

            with col2:
                if st.button("📱 PhonePe"):
                    st.markdown(f"[Pay](upi://pay?pa={UPI_ID}&pn=Balaji&am={fare}&cu=INR)")

            st.code(f"UPI: {UPI_ID} | ₹{fare}")
            file = st.file_uploader("Upload Screenshot")

        if st.button("Confirm Booking"):

            bid = "BT" + datetime.now().strftime("%d%H%M%S")

            img_path = ""
            if file:
                os.makedirs("uploads", exist_ok=True)
                img_path = f"uploads/{bid}_{file.name}"
                with open(img_path, "wb") as f:
                    f.write(file.getbuffer())

            new = pd.DataFrame([[bid, st.session_state.user, datetime.now(), s,d,v,fare,pay,mob,img_path]], columns=BOOKING_COLS)
            pd.concat([safe_read(BOOKING_DB, BOOKING_COLS), new]).to_csv(BOOKING_DB, index=False)

            st.success("Booking Done 🎉")

    # HISTORY
    elif st.session_state.page == "History":

        df = safe_read(BOOKING_DB, BOOKING_COLS)
        df = df[df["username"] == st.session_state.user]

        for _, r in df.iterrows():
            st.write(f"{r['booking_id']} | {r['vehicle']} | ₹{r['fare']}")

    # ADMIN
    elif st.session_state.page == "Admin":

        pw = st.text_input("Password", type="password")

        if pw == ADMIN_PASS:
            df = safe_read(BOOKING_DB, BOOKING_COLS)
            st.dataframe(df)