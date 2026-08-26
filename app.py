import streamlit as st
import pandas as pd
import os
import hashlib
from datetime import datetime, timezone, timedelta
import urllib.parse
import sqlite3
import secrets
import re
from pathlib import Path

# =========================================================
# BALAJI LOGISTICS & TOURS - PRODUCTION-READY STREAMLIT APP
# Existing features preserved + stability/security fixes
# =========================================================

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Balaji Logistics & Tours",
    layout="centered",
    page_icon="🚗",
    initial_sidebar_state="collapsed",
)

# ---------------- CONFIG ----------------
IST = timezone(timedelta(hours=5, minutes=30))

# IMPORTANT:
# For production, put these values in Streamlit Secrets instead of
# keeping real credentials in source code.
WA_LINK_NO = st.secrets.get("WA_LINK_NO", os.getenv("WA_LINK_NO", "919767981986"))
ADMIN_PASS = st.secrets.get("ADMIN_PASS", os.getenv("ADMIN_PASS", "12345"))
UPI_ID = st.secrets.get("UPI_ID", os.getenv("UPI_ID", "9309146504-2@ybl"))

DB_NAME = st.secrets.get("DB_NAME", os.getenv("DB_NAME", "balaji_logistics.db"))
UPLOAD_DIR = Path(st.secrets.get("UPLOAD_DIR", os.getenv("UPLOAD_DIR", "uploads")))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

RATES = {
    "WagonR": 11,
    "Swift Dzire": 13,
    "Ertiga": 18,
    "Innova": 24,
    "Tempo Traveller": 35,
}

# ---------------- DATABASE ----------------
def get_db():
    conn = sqlite3.connect(DB_NAME, timeout=30, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=30000")
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            mobile TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            date TEXT NOT NULL,
            from_loc TEXT NOT NULL,
            to_loc TEXT NOT NULL,
            vehicle TEXT NOT NULL,
            fare REAL NOT NULL,
            payment TEXT NOT NULL,
            mobile TEXT NOT NULL,
            screenshot TEXT DEFAULT '',
            status TEXT NOT NULL DEFAULT 'Confirmed',
            trip_type TEXT NOT NULL,
            driver_name TEXT DEFAULT 'Not Assigned',
            driver_mobile TEXT DEFAULT 'Not Assigned'
        )
    """)

    conn.commit()
    conn.close()


init_db()

# ---------------- HELPERS ----------------
def hash_pw(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def check_pw(password: str, stored_hash: str) -> bool:
    return secrets.compare_digest(hash_pw(password), stored_hash)


def valid_mobile(mobile: str) -> bool:
    return bool(re.fullmatch(r"[0-9]{10}", mobile.strip()))


def make_booking_id() -> str:
    # UUID-like random suffix prevents same-second booking ID collisions.
    now = datetime.now(IST).strftime("%d%H%M%S")
    return f"BT{now}{secrets.token_hex(2).upper()}"


def safe_filename(name: str) -> str:
    name = os.path.basename(name)
    name = re.sub(r"[^A-Za-z0-9._-]", "_", name)
    return name[:100]


def make_upi_link(amount: float) -> str:
    return (
        f"upi://pay?pa={urllib.parse.quote(UPI_ID)}"
        f"&pn=Balaji"
        f"&am={amount:.2f}"
        f"&cu=INR"
    )


def make_whatsapp_url(message: str) -> str:
    return f"https://wa.me/{WA_LINK_NO}?text={urllib.parse.quote(message)}"


# ---------------- UI CSS ----------------
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp {
    background-color: #0e0e0e;
    color: #ffffff;
    max-width: 100% !important;
    overflow-x: hidden;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
    max-width: 720px;
}

.stButton > button {
    background: linear-gradient(135deg, #FFBB00, #e6a800);
    color: #000000;
    font-weight: bold;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
    width: 100%;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #ffcc33, #FFBB00);
}

input, select, textarea {
    background-color: #1a1a1a !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    border: 1px solid #333 !important;
}

[data-testid="stMetric"] {
    background: #181818;
    padding: 12px;
    border-radius: 12px;
}

.booking-card {
    background: #1a1a1a;
    padding: 14px;
    border-radius: 12px;
    margin-bottom: 12px;
    border-left: 5px solid #FFBB00;
}

.brand-card {
    background: #111;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 0 15px rgba(255,187,0,0.25);
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
defaults = {
    "logged_in": False,
    "user": "",
    "page": "Home",
    "flash_done": False,
    "admin_authenticated": False,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------- SIMPLE FLASH SCREEN ----------------
# No time.sleep(): avoids blocking the Streamlit server.
if not st.session_state.flash_done:
    st.markdown("""
    <div style="
        display:flex;
        justify-content:center;
        align-items:center;
        min-height:75vh;
        background:linear-gradient(135deg,#000000,#1a1a1a);
        border-radius:20px;">
        <div style="
            background:#111;
            padding:30px;
            border-radius:20px;
            box-shadow:0 0 30px rgba(255,187,0,0.4);
            text-align:center;
            width:90%;
            max-width:320px;">
            <h1 style="color:#FFBB00;font-size:26px;">🚩 BALAJI</h1>
            <h2 style="color:white;font-size:20px;">LOGISTICS</h2>
            <p style="color:#bbbbbb;font-size:14px;">& TOURS & TRAVELS</p>
            <p style="color:white;font-size:12px;">🌍 All India Service</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.session_state.flash_done = True
    st.stop()

# =========================================================
# LOGIN / REGISTER
# =========================================================
if not st.session_state.logged_in:

    st.markdown(
        "<h2 style='text-align:center;color:#FFBB00;'>🚩 BALAJI LOGISTICS</h2>",
        unsafe_allow_html=True,
    )

    mode = st.radio(
        "Select Option",
        ["Login", "Register"],
        horizontal=True,
        key="auth_mode",
    )

    if mode == "Login":
        u = st.text_input("Username", key="login_username")
        p = st.text_input("Password", type="password", key="login_password")

        if st.button("Login to App", use_container_width=True):
            u = u.strip()

            if not u or not p:
                st.warning("Please enter username and password.")
            else:
                conn = get_db()
                row = conn.execute(
                    "SELECT password FROM users WHERE username = ?",
                    (u,),
                ).fetchone()
                conn.close()

                if row and check_pw(p, row["password"]):
                    st.session_state.logged_in = True
                    st.session_state.user = u
                    st.session_state.page = "Home"
                    st.session_state.admin_authenticated = False
                    st.rerun()
                else:
                    st.error("Wrong Username or Password!")

    else:
        nu = st.text_input("Choose Username", key="register_username")
        nm = st.text_input("Mobile Number", key="register_mobile")
        np = st.text_input(
            "Create Password",
            type="password",
            key="register_password",
        )

        if st.button("Register Account", use_container_width=True):
            nu = nu.strip()
            nm = nm.strip()

            if not nu or not nm or not np:
                st.warning("Please fill out all fields.")
            elif len(nu) < 3:
                st.warning("Username must contain at least 3 characters.")
            elif not valid_mobile(nm):
                st.warning("Enter a valid 10-digit mobile number.")
            elif len(np) < 6:
                st.warning("Password must contain at least 6 characters.")
            else:
                conn = get_db()
                exists = conn.execute(
                    "SELECT username FROM users WHERE username = ?",
                    (nu,),
                ).fetchone()

                if exists:
                    st.error("Username already exists!")
                else:
                    conn.execute(
                        "INSERT INTO users (username, password, mobile) VALUES (?, ?, ?)",
                        (nu, hash_pw(np), nm),
                    )
                    conn.commit()
                    st.success("Account Created! Please login.")

                conn.close()

    st.stop()

# =========================================================
# MAIN APP
# =========================================================
menu_options = [
    "🏠 Home",
    "🚗 Book",
    "📜 History",
    "👤 Profile",
    "🛠 Admin",
    "🚪 Logout",
]

page_mapping = {
    "🏠 Home": "Home",
    "🚗 Book": "Book",
    "📜 History": "History",
    "👤 Profile": "Profile",
    "🛠 Admin": "Admin",
    "🚪 Logout": "Logout",
}

inverse_mapping = {v: k for k, v in page_mapping.items()}
default_selection = inverse_mapping.get(
    st.session_state.page,
    "🏠 Home",
)

selected_menu = st.selectbox(
    "📌 Menu Navigation",
    menu_options,
    index=menu_options.index(default_selection),
)

if selected_menu == "🚪 Logout":
    st.session_state.logged_in = False
    st.session_state.user = ""
    st.session_state.page = "Home"
    st.session_state.admin_authenticated = False
    st.rerun()

st.session_state.page = page_mapping[selected_menu]

st.markdown("---")

# =========================================================
# HOME
# =========================================================
if st.session_state.page == "Home":

    st.markdown("""
    <div class="brand-card">
        <h3 style="color:#FFBB00;margin-bottom:5px;">🚩 BALAJI LOGISTICS</h3>
        <p style="color:white;font-size:14px;font-weight:bold;">Tours & Travels</p>
        <p style="color:#bbbbbb;font-size:12px;">🌍 Maharashtra & All India Service</p>
        <p style="color:#FFBB00;font-size:12px;">
            🚗 Safe • Fast • Comfortable Rides
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    st.image(
        "https://cdn.pixabay.com/photo/2016/11/18/12/34/car-1835506_1280.jpg",
        use_container_width=True,
    )

    st.success("WELCOME 🚗 SELECT 'BOOK' FROM MENU TO RIDE")

    st.subheader("📍 Our Service Hub (Nashik)")
    map_df = pd.DataFrame({
        "lat": [19.9975],
        "lon": [73.7898],
    })
    st.map(map_df, zoom=11)

    st.markdown(
        f"""
        <div style="text-align:center;margin-top:15px;">
            <a href="tel:{WA_LINK_NO}"
               style="
               background-color:#25D366;
               color:white;
               padding:10px 20px;
               border-radius:10px;
               text-decoration:none;
               font-weight:bold;
               font-size:14px;">
               📞 Call Support Now
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================================================
# BOOKING
# =========================================================
elif st.session_state.page == "Book":

    conn = get_db()
    user_row = conn.execute(
        "SELECT mobile FROM users WHERE username = ?",
        (st.session_state.user,),
    ).fetchone()
    conn.close()

    mob = user_row["mobile"] if user_row else ""

    st.markdown("""
    <div class="brand-card">
        <h3 style="color:#FFBB00;margin:0;">🚗 Book Your Ride</h3>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    s = st.text_input("Pickup Location")
    d = st.text_input("Drop Location")

    v = st.selectbox(
        "Select Vehicle",
        list(RATES.keys()),
    )

    trip_type = st.radio(
        "Trip Type",
        ["One-Way", "Round Trip"],
        horizontal=True,
    )

    km = st.number_input(
        "Estimated KM",
        value=50,
        min_value=1,
        max_value=5000,
        step=1,
    )

    pay = st.radio(
        "Payment Method",
        ["Cash", "Online"],
        horizontal=True,
    )

    base_fare = km * RATES[v]
    fare = base_fare * 2 if trip_type == "Round Trip" else base_fare

    st.info(f"💰 Estimated Fare: ₹{fare:,.2f}")

    file = None

    if pay == "Online":
        st.markdown("### 💳 PhonePe UPI & QR Payment")

        upi_link = make_upi_link(fare)

        qr_data = urllib.parse.quote(upi_link, safe="")
        qr_url = (
            "https://api.qrserver.com/v1/create-qr-code/"
            f"?size=180x180&data={qr_data}"
        )

        st.markdown(
            f"""
            <div style="
                background:#181818;
                padding:15px;
                border-radius:15px;
                text-align:center;
                border:2px solid #5f259f;">

                <h3 style="color:#9b51e0;margin:0;">PhonePe</h3>
                <p style="color:white;font-size:13px;">
                    ACCEPTED HERE
                </p>

                <div style="
                    background:white;
                    padding:10px;
                    display:inline-block;
                    border-radius:10px;
                    margin:10px 0;">
                    <img src="{qr_url}" width="180">
                </div>

                <p style="
                    color:#FFBB00;
                    font-size:15px;
                    font-weight:bold;">
                    Amount: ₹{fare:,.2f}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        col_g, col_p = st.columns(2)

        with col_g:
            st.link_button(
                "📱 GPay / UPI",
                upi_link,
                use_container_width=True,
            )

        with col_p:
            st.link_button(
                "📱 PhonePe",
                upi_link,
                use_container_width=True,
            )

        st.code(f"UPI: {UPI_ID}")

        file = st.file_uploader(
            "Upload Payment Screenshot",
            type=["png", "jpg", "jpeg"],
        )

    st.write("")

    if st.button(
        "Confirm Booking Now",
        use_container_width=True,
    ):

        s_clean = s.strip()
        d_clean = d.strip()

        if not s_clean or not d_clean:
            st.warning(
                "Please fill out both pickup and drop locations."
            )
        else:

            booking_time_str = datetime.now(IST).strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            bid = make_booking_id()

            img_path = ""

            if file is not None:
                safe_name = safe_filename(file.name)
                destination = UPLOAD_DIR / f"{bid}_{safe_name}"

                with open(destination, "wb") as output:
                    output.write(file.getbuffer())

                img_path = str(destination)

            conn = get_db()

            conn.execute(
                """
                INSERT INTO bookings (
                    booking_id,
                    username,
                    date,
                    from_loc,
                    to_loc,
                    vehicle,
                    fare,
                    payment,
                    mobile,
                    screenshot,
                    status,
                    trip_type,
                    driver_name,
                    driver_mobile
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    bid,
                    st.session_state.user,
                    booking_time_str,
                    s_clean,
                    d_clean,
                    v,
                    fare,
                    pay,
                    mob,
                    img_path,
                    "Confirmed",
                    trip_type,
                    "Not Assigned",
                    "Not Assigned",
                ),
            )

            conn.commit()
            conn.close()

            st.success(
                f"Booking Confirmed 🎉 ID: {bid}"
            )

            msg = (
                "🚩 BALAJI LOGISTICS & TOURS 🚩\n"
                "━━━━━━━━━━━━━━━\n"
                f"🆔 Booking ID: {bid}\n"
                f"🕒 Time: {booking_time_str}\n"
                f"👤 Customer: {st.session_state.user}\n"
                f"📞 Mobile: {mob}\n"
                f"📍 Pickup: {s_clean}\n"
                f"🏁 Drop: {d_clean}\n"
                f"🚗 Vehicle: {v} ({trip_type})\n"
                f"💰 Fare: ₹{fare:,.2f}\n"
                f"💳 Payment: {pay}\n\n"
                "🌍 All India Service\n"
                "⚡ Safe & Comfortable Ride\n"
                "━━━━━━━━━━━━━━━"
            )

            st.link_button(
                "📲 Send Details on WhatsApp",
                make_whatsapp_url(msg),
                use_container_width=True,
            )

# =========================================================
# HISTORY
# =========================================================
elif st.session_state.page == "History":

    conn = get_db()

    user_df = pd.read_sql_query(
        """
        SELECT *
        FROM bookings
        WHERE username = ?
        ORDER BY date DESC
        """,
        conn,
        params=(st.session_state.user,),
    )

    conn.close()

    st.subheader("📜 Your Bookings")

    search_query = st.text_input(
        "🔍 Search Booking by ID"
    ).strip()

    if search_query and not user_df.empty:
        user_df = user_df[
            user_df["booking_id"].str.contains(
                search_query,
                case=False,
                na=False,
            )
        ]

    if user_df.empty:
        st.info("No bookings found.")

    else:
        for _, r in user_df.iterrows():

            if r["status"] == "Confirmed":
                status_color = "#00c853"
            elif r["status"] == "Completed":
                status_color = "#ff9800"
            else:
                status_color = "#f44336"

            st.markdown(
                f"""
                <div class="booking-card">
                    <h4 style="margin:0 0 5px 0;font-size:15px;">
                        🆔 {r['booking_id']}
                        |
                        <span style="color:{status_color};">
                            {r['status']}
                        </span>
                    </h4>

                    <p style="margin:3px 0;font-size:13px;">
                        🚗 <b>{r['vehicle']}</b>
                        ({r['trip_type']})<br>
                        📍 {r['from_loc']} ➔ {r['to_loc']}<br>
                        💰 ₹{r['fare']:,.2f}
                        | 💳 {r['payment']}<br>
                        👨‍✈️ Driver:
                        {r['driver_name']}
                        ({r['driver_mobile']})
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            col_inv, col_can = st.columns(2)

            invoice_text = f"""
========================================
       BALAJI LOGISTICS & TOURS
========================================
Booking ID   : {r['booking_id']}
Date         : {r['date']}
Customer     : {r['username