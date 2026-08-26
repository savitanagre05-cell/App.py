import streamlit as st
import pandas as pd
import os
import hashlib
import hmac
import secrets
from datetime import datetime, timezone, timedelta
import urllib.parse
import sqlite3
import re
from pathlib import Path
from uuid import uuid4

# ============================================================
# BALAJI LOGISTICS & TOURS - Streamlit App
# ============================================================

st.set_page_config(
    page_title="Balaji Logistics & Tours",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------- CONFIG ----------------
IST = timezone(timedelta(hours=5, minutes=30))
WA_LINK_NO = os.getenv("BALAJI_WA_NUMBER", "919767981986")
ADMIN_PASS = os.getenv("BALAJI_ADMIN_PASS", "12345")  # CHANGE before production
UPI_ID = os.getenv("BALAJI_UPI_ID", "9309146504-2@ybl")
DB_NAME = os.getenv("BALAJI_DB", "balaji_logistics.db")
UPLOAD_DIR = Path(os.getenv("BALAJI_UPLOAD_DIR", "uploads"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

RATES = {
    "WagonR": 11,
    "Swift Dzire": 13,
    "Ertiga": 18,
    "Innova": 24,
    "Tempo Traveller": 35,
}

STATUS_OPTIONS = ["Confirmed", "Completed", "Cancelled"]
TRIP_OPTIONS = ["One-Way", "Round Trip"]
PAYMENT_OPTIONS = ["Cash", "Online"]

# ---------------- DATABASE HELPERS ----------------
def get_conn():
    conn = sqlite3.connect(DB_NAME, timeout=30, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout = 30000")
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_conn()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                mobile TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.execute("""
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
                status TEXT NOT NULL,
                trip_type TEXT NOT NULL,
                driver_name TEXT DEFAULT 'Not Assigned',
                driver_mobile TEXT DEFAULT 'Not Assigned'
            )
        """)

        # Upgrade older database files without deleting existing data.
        user_cols = {r[1] for r in conn.execute("PRAGMA table_info(users)").fetchall()}
        if "created_at" not in user_cols:
            conn.execute("ALTER TABLE users ADD COLUMN created_at TEXT DEFAULT ''")
            conn.execute("UPDATE users SET created_at = ? WHERE created_at = ''", (now_str(),))

        conn.commit()
    finally:
        conn.close()


def now_str():
    return datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")


init_db()

# ---------------- SECURITY ----------------
def hash_password(password: str) -> str:
    # PBKDF2 with a random salt. Stored format: pbkdf2$iterations$salt$hash
    iterations = 210_000
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), bytes.fromhex(salt), iterations
    ).hex()
    return f"pbkdf2${iterations}${salt}${digest}"


def verify_password(password: str, stored: str) -> tuple[bool, bool]:
    # Returns (valid, legacy_sha256)
    if stored.startswith("pbkdf2$"):
        try:
            _, iterations, salt, expected = stored.split("$", 3)
            actual = hashlib.pbkdf2_hmac(
                "sha256", password.encode("utf-8"), bytes.fromhex(salt), int(iterations)
            ).hex()
            return hmac.compare_digest(actual, expected), False
        except Exception:
            return False, False

    # Compatibility with old users created by the original code.
    legacy = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return hmac.compare_digest(legacy, stored), True


def valid_mobile(mobile: str) -> bool:
    return bool(re.fullmatch(r"[6-9]\d{9}", mobile.strip()))


def valid_username(username: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9_]{3,30}", username.strip()))


def clean_text(value: str, max_len: int = 120) -> str:
    return " ".join(str(value).strip().split())[:max_len]


def make_booking_id() -> str:
    return "BT" + datetime.now(IST).strftime("%Y%m%d%H%M%S") + uuid4().hex[:4].upper()


def get_user_mobile(username: str) -> str:
    conn = get_conn()
    try:
        row = conn.execute("SELECT mobile FROM users WHERE username = ?", (username,)).fetchone()
        return str(row["mobile"]) if row else ""
    finally:
        conn.close()

# ---------------- UI STYLE ----------------
st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
.stApp { background:#0e0e0e; color:#fff; max-width:100% !important; overflow-x:hidden; }
.block-container { max-width:720px; padding-top:1rem; padding-bottom:3rem; }
.stButton > button, .stDownloadButton > button {
    background:linear-gradient(135deg,#FFBB00,#e6a800);
    color:#000; font-weight:700; border:0; border-radius:10px;
    min-height:44px; width:100%;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background:linear-gradient(135deg,#ffcc33,#FFBB00);
}
input, textarea, [data-baseweb="select"] > div {
    background:#1a1a1a !important; color:#fff !important;
    border-radius:8px !important;
}
[data-testid="stMetricValue"] { color:#FFBB00; }
.small-note { color:#aaa; font-size:12px; text-align:center; }
.card { background:#151515; padding:16px; border-radius:15px; margin:10px 0; border:1px solid #292929; }
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
def init_session():
    defaults = {
        "logged_in": False,
        "user": "",
        "page": "Home",
        "admin_unlocked": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session()

# ---------------- FLASH SCREEN ----------------
# No time.sleep(): it blocks the server thread and makes the app feel slow.
if "flash_done" not in st.session_state:
    st.session_state.flash_done = True

# ---------------- LOGIN / REGISTER ----------------
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center;color:#FFBB00;'>🚩 BALAJI LOGISTICS</h2>", unsafe_allow_html=True)
    st.markdown("<p class='small-note'>Tours & Travels • Maharashtra & All India Service</p>", unsafe_allow_html=True)

    mode = st.radio("Select Option", ["Login", "Register"], horizontal=True)

    if mode == "Login":
        with st.form("login_form"):
            username = st.text_input("Username", max_chars=30)
            password = st.text_input("Password", type="password", max_chars=100)
            submitted = st.form_submit_button("🔐 Login to App", use_container_width=True)

        if submitted:
            username = username.strip()
            conn = get_conn()
            try:
                row = conn.execute(
                    "SELECT password FROM users WHERE username = ?", (username,)
                ).fetchone()

                if row:
                    valid, legacy = verify_password(password, row["password"])
                    if valid:
                        # Upgrade old SHA-256 password automatically.
                        if legacy:
                            conn.execute(
                                "UPDATE users SET password = ? WHERE username = ?",
                                (hash_password(password), username),
                            )
                            conn.commit()
                        st.session_state.logged_in = True
                        st.session_state.user = username
                        st.session_state.page = "Home"
                        st.session_state.admin_unlocked = False
                        st.rerun()
                    else:
                        st.error("❌ Wrong Username or Password!")
                else:
                    st.error("❌ Wrong Username or Password!")
            finally:
                conn.close()

    else:
        with st.form("register_form"):
            new_username = st.text_input("Choose Username", max_chars=30)
            new_mobile = st.text_input("Mobile Number", max_chars=10, placeholder="10 digit mobile")
            new_password = st.text_input("Create Password", type="password", max_chars=100)
            register = st.form_submit_button("📝 Register Account", use_container_width=True)

        if register:
            new_username = new_username.strip()
            new_mobile = new_mobile.strip()

            if not valid_username(new_username):
                st.error("Username: 3-30 characters, only A-Z, 0-9 and _ allowed.")
            elif not valid_mobile(new_mobile):
                st.error("Please enter a valid 10-digit Indian mobile number.")
            elif len(new_password) < 6:
                st.error("Password must contain at least 6 characters.")
            else:
                conn = get_conn()
                try:
                    exists = conn.execute(
                        "SELECT 1 FROM users WHERE username = ?", (new_username,)
                    ).fetchone()
                    if exists:
                        st.error("❌ Username already exists!")
                    else:
                        conn.execute(
                            "INSERT INTO users (username,password,mobile,created_at) VALUES (?,?,?,?)",
                            (new_username, hash_password(new_password), new_mobile, now_str()),
                        )
                        conn.commit()
                        st.success("✅ Account Created! Please login.")
                except sqlite3.IntegrityError:
                    st.error("Username already exists. Please choose another.")
                finally:
                    conn.close()

# ---------------- MAIN APP ----------------
else:
    menu_options = ["🏠 Home", "🚗 Book", "📜 History", "👤 Profile", "🛠 Admin", "🚪 Logout"]
    page_mapping = {
        "🏠 Home": "Home",
        "🚗 Book": "Book",
        "📜 History": "History",
        "👤 Profile": "Profile",
        "🛠 Admin": "Admin",
        "🚪 Logout": "Logout",
    }

    inverse = {v: k for k, v in page_mapping.items()}
    current = inverse.get(st.session_state.page, "🏠 Home")
    selected = st.selectbox("📌 Menu Navigation", menu_options, index=menu_options.index(current))

    if selected == "🚪 Logout":
        st.session_state.clear()
        st.rerun()

    st.session_state.page = page_mapping[selected]
    st.markdown("---")

    # ---------------- HOME ----------------
    if st.session_state.page == "Home":
        st.markdown("""
        <div class="card" style="text-align:center;">
            <h3 style="color:#FFBB00;margin-bottom:5px;">🚩 BALAJI LOGISTICS</h3>
            <p style="font-weight:bold;margin:5px;">Tours & Travels</p>
            <p style="color:#aaa;font-size:12px;">🌍 Maharashtra & All India Service</p>
            <p style="color:#FFBB00;font-size:12px;">🚗 Safe • Fast • Comfortable Rides</p>
        </div>
        """, unsafe_allow_html=True)

        st.image(
            "https://cdn.pixabay.com/photo/2016/11/18/12/34/car-1835506_1280.jpg",
            use_container_width=True,
        )
        st.success("WELCOME 🚗 SELECT 'BOOK' FROM MENU TO RIDE")

        st.subheader("📍 Our Service Hub (Nashik)")
        map_df = pd.DataFrame({"lat": [19.9975], "lon": [73.7898]})
        st.map(map_df, zoom=11)

        st.markdown(
            f"""<div style='text-align:center;margin-top:15px;'>
            <a href='tel:{WA_LINK_NO}' style='background:#25D366;color:white;padding:12px 20px;border-radius:10px;text-decoration:none;font-weight:bold;'>📞 Call Support Now</a>
            </div>""",
            unsafe_allow_html=True,
        )

    # ---------------- BOOK ----------------
    elif st.session_state.page == "Book":
        mobile = get_user_mobile(st.session_state.user)
        st.markdown("<div class='card' style='text-align:center;'><h3 style='color:#FFBB00;margin:0;'>🚗 Book Your Ride</h3></div>", unsafe_allow_html=True)

        with st.form("booking_form", clear_on_submit=False):
            pickup = st.text_input("Pickup Location", max_chars=120)
            drop = st.text_input("Drop Location", max_chars=120)
            vehicle = st.selectbox("Select Vehicle", list(RATES.keys()))
            trip_type = st.radio("Trip Type", TRIP_OPTIONS, horizontal=True)
            km = st.number_input("Estimated KM", min_value=1, max_value=10000, value=50, step=1)
            payment = st.radio("Payment Method", PAYMENT_OPTIONS, horizontal=True)
            payment_screenshot = st.file_uploader(
                "Upload Payment Screenshot (Online only)",
                type=["png", "jpg", "jpeg"],
            ) if payment == "Online" else None

            fare = km * RATES[vehicle] * (2 if trip_type == "Round Trip" else 1)
            st.markdown(f"### 💰 Estimated Fare: ₹{fare:.2f}")
            confirm = st.form_submit_button("✅ Confirm Booking Now", use_container_width=True)

        if confirm:
            pickup = clean_text(pickup)
            drop = clean_text(drop)

            if not pickup or not drop:
                st.warning("Please fill out both pickup and drop locations.")
            elif pickup.lower() == drop.lower():
                st.warning("Pickup and drop locations cannot be the same.")
            elif not mobile or not valid_mobile(mobile):
                st.error("Please update your valid mobile number in Profile first.")
            elif payment == "Online" and payment_screenshot is None:
                st.warning("Please upload the payment screenshot for Online payment.")
            else:
                bid = make_booking_id()
                booking_time = now_str()
                screenshot_path = ""

                if payment_screenshot is not None:
                    safe_name = re.sub(r"[^A-Za-z0-9_.-]", "_", payment_screenshot.name)
                    screenshot_path = str(UPLOAD_DIR / f"{bid}_{safe_name}")
                    with open(screenshot_path, "wb") as out:
                        out.write(payment_screenshot.getbuffer())

                conn = get_conn()
                try:
                    conn.execute("""
                        INSERT INTO bookings
                        (booking_id,username,date,from_loc,to_loc,vehicle,fare,payment,mobile,screenshot,status,trip_type,driver_name,driver_mobile)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    """, (
                        bid, st.session_state.user, booking_time, pickup, drop, vehicle,
                        float(fare), payment, mobile, screenshot_path, "Confirmed",
                        trip_type, "Not Assigned", "Not Assigned"
                    ))
                    conn.commit()
                except sqlite3.Error as exc:
                    st.error(f"Booking could not be saved: {exc}")
                finally:
                    conn.close()

                st.success(f"🎉 Booking Confirmed! ID: {bid}")

                msg = (
                    "🚩 BALAJI LOGISTICS & TOURS 🚩\n"
                    "━━━━━━━━━━━━━━━\n"
                    f"🆔 Booking ID: {bid}\n"
                    f"🕒 Time: {booking_time}\n"
                    f"👤 Customer: {st.session_state.user}\n"
                    f"📞 Mobile: {mobile}\n"
                    f"📍 Pickup: {pickup}\n"
                    f"🏁 Drop: {drop}\n"
                    f"🚗 Vehicle: {vehicle} ({trip_type})\n"
                    f"📏 KM: {km}\n"
                    f"💰 Fare: ₹{fare:.2f}\n"
                    f"💳 Payment: {payment}\n\n"
                    "🌍 All India Service\n"
                    "⚡ Safe & Comfortable Ride\n"
                    "━━━━━━━━━━━━━━━"
                )

                wa_url = "https://wa.me/" + WA_LINK_NO + "?text=" + urllib.parse.quote(msg)
                st.link_button("📲 Send Details on WhatsApp", wa_url, use_container_width=True)

    # ---------------- HISTORY ----------------
    elif st.session_state.page == "History":
        st.subheader("📜 Your Bookings")
        search_query = st.text_input("🔍 Search Booking by ID", max_chars=30)

        conn = get_conn()
        try:
            user_df = pd.read_sql_query(
                "SELECT * FROM bookings WHERE username = ? ORDER BY date DESC",
                conn,
                params=(st.session_state.user,),
            )
        finally:
            conn.close()

        if search_query and not user_df.empty:
            user_df = user_df[user_df["booking_id"].str.contains(search_query.strip(), case=False, na=False)]

        if user_df.empty:
            st.info("No bookings found.")
        else:
            for _, row in user_df.iterrows():
                status = str(row["status"])
                status_color = "#32CD32" if status == "Confirmed" else ("#FFA500" if status == "Completed" else "#FF4B4B")
                st.markdown(f"""
                <div class='card' style='border-left:5px solid #FFBB00;'>
                    <h4 style='margin:0 0 8px 0;'>🆔 {row['booking_id']} <span style='color:{status_color};'>| {status}</span></h4>
                    <div style='font-size:13px;line-height:1.7;'>
                    🚗 <b>{row['vehicle']}</b> ({row['trip_type']})<br>
                    📍 {row['from_loc']} ➜ {row['to_loc']}<br>
                    💰 ₹{float(row['fare']):.2f} | 💳 {row['payment']}<br>
                    👨‍✈️ Driver: {row['driver_name']} ({row['driver_mobile']})
                    </div>
                </div>
                """, unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                invoice_text = f"""========================================
       BALAJI LOGISTICS & TOURS
========================================
Booking ID   : {row['booking_id']}
Date         : {row['date']}
Customer     : {row['username']}
Mobile       : {row['mobile']}
Vehicle      : {row['vehicle']} ({row['trip_type']})
Pickup       : {row['from_loc']}
Drop         : {row['to_loc']}
Driver       : {row['driver_name']} ({row['driver_mobile']})
Fare         : Rs. {float(row['fare']):.2f}
Payment      : {row['payment']}
Status       : {row['status']}
========================================
"""
                with col1:
                    st.download_button(
                        "📥 Invoice", invoice_text,
                        file_name=f"Invoice_{row['booking_id']}.txt",
                        mime="text/plain", key=f"inv_{row['booking_id']}"
                    )

                if status == "Confirmed":
                    with col2:
                        if st.button("❌ Cancel", key=f"cancel_{row['booking_id']}"):
                            conn = get_conn()
                            try:
                                conn.execute(
                                    "UPDATE bookings SET status = 'Cancelled' WHERE booking_id = ? AND username = ? AND status = 'Confirmed'",
                                    (row['booking_id'], st.session_state.user),
                                )
                                conn.commit()
                                st.success("Booking cancelled successfully!")
                                st.rerun()
                            finally:
                                conn.close()

    # ---------------- PROFILE ----------------
    elif st.session_state.page == "Profile":
        st.subheader("👤 User Profile")
        current_mobile = get_