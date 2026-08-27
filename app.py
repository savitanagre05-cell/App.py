import streamlit as st
import pandas as pd
import os
import hashlib
from datetime import datetime, timezone, timedelta
import urllib.parse
import sqlite3
import re
from pathlib import Path
import time

# ============================================================
# BALAJI LOGISTICS & TOURS
# Final stable Streamlit version + Flash Screen
# ============================================================

IST = timezone(timedelta(hours=5, minutes=30))

WA_LINK_NO = "919767981986"
ADMIN_PASS = "12345"
UPI_ID = "9309146504-2@ybl"
DB_NAME = "balaji_logistics.db"
UPLOAD_DIR = Path("uploads")

RATES = {
    "WagonR": 11,
    "Swift Dzire": 13,
    "Ertiga": 18,
    "Innova": 24,
    "Tempo Traveller": 35,
}

st.set_page_config(
    page_title="Balaji Logistics & Tours",
    layout="centered",
    page_icon="🚩",
    initial_sidebar_state="collapsed",
)

@st.cache_resource
def get_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            mobile TEXT NOT NULL
        )
    """)
    cur.execute("""
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
            screenshot TEXT,
            status TEXT NOT NULL,
            trip_type TEXT NOT NULL,
            driver_name TEXT,
            driver_mobile TEXT
        )
    """)
    conn.commit()

init_db()

st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
.stApp {
    background:#0e0e0e;
    color:#ffffff;
    max-width:100% !important;
    overflow-x:hidden;
}
.block-container {
    padding-top:1rem;
    padding-bottom:4rem;
    max-width:720px;
}
.stButton > button {
    background:linear-gradient(135deg,#FFBB00,#e6a800);
    color:#000000;
    font-weight:700;
    border-radius:10px;
    border:none;
    padding:10px 20px;
    width:100%;
}
.stButton > button:hover {
    background:linear-gradient(135deg,#ffcc33,#FFBB00);
}
input, textarea {
    background-color:#1a1a1a !important;
    color:#ffffff !important;
    border-radius:8px !important;
    border:1px solid #333 !important;
}
[data-baseweb="select"] > div {
    background-color:#1a1a1a !important;
    color:#ffffff !important;
}
.balaji-card {
    background:#111111;
    padding:24px 18px;
    border-radius:18px;
    box-shadow:0 0 22px rgba(255,187,0,.22);
    text-align:center;
    border:1px solid #292929;
}
.brand-title {
    color:#FFBB00;
    font-size:30px;
    font-weight:800;
    letter-spacing:1px;
    margin:0;
}
.brand-sub {
    color:#ffffff;
    font-size:22px;
    font-weight:700;
    margin:10px 0 3px;
}
.brand-small {
    color:#aaaaaa;
    font-size:14px;
    margin:0;
}
.booking-card {
    background:#1a1a1a;
    padding:14px;
    border-radius:10px;
    margin-bottom:12px;
    border-left:5px solid #FFBB00;
}
.extra-note {
    background:#171717;
    border:1px solid #3a3a3a;
    border-radius:10px;
    padding:10px 12px;
    color:#dddddd;
    font-size:13px;
}
.flash-screen {
    position:fixed;
    top:0;
    left:0;
    width:100vw;
    height:100vh;
    background:#0e0e0e;
    z-index:999999;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    text-align:center;
}
.flash-logo {
    color:#FFBB00;
    font-size:48px;
    font-weight:900;
    letter-spacing:3px;
    margin:0;
    animation:flashLogo 1.2s ease-in-out infinite alternate;
}
.flash-title {
    color:#ffffff;
    font-size:30px;
    font-weight:800;
    margin:8px 0 0;
    letter-spacing:2px;
}
.flash-sub {
    color:#aaaaaa;
    font-size:14px;
    margin:8px 0 0;
    letter-spacing:1px;
}
.flash-line {
    width:180px;
    height:3px;
    background:#FFBB00;
    border-radius:10px;
    margin-top:22px;
    animation:flashLine 1.2s ease-in-out infinite alternate;
}
@keyframes flashLogo {
    from {opacity:.65; transform:scale(.97);}
    to {opacity:1; transform:scale(1.03);}
}
@keyframes flashLine {
    from {width:80px; opacity:.5;}
    to {width:200px; opacity:1;}
}
</style>
""", unsafe_allow_html=True)

# ================= FLASH / SPLASH SCREEN =================
if "flash_done" not in st.session_state:
    st.session_state.flash_done = False

if not st.session_state.flash_done:
    flash_placeholder = st.empty()
    flash_placeholder.markdown("""
    <div class="flash-screen">
        <p class="flash-logo">🚩 BALAJI</p>
        <p class="flash-title">LOGISTICS</p>
        <p class="flash-sub">&amp; TOURS &amp; TRAVELS</p>
        <div class="flash-line"></div>
        <p class="flash-sub" style="margin-top:18px;">
            🌍 All India Service
        </p>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(2)
    st.session_state.flash_done = True
    flash_placeholder.empty()
    st.rerun()

def hash_pw(password):
    return hashlib.sha256(str(password).encode("utf-8")).hexdigest()

def check_pw(password, stored_hash):
    return hash_pw(password) == stored_hash

def valid_mobile(mobile):
    digits = re.sub(r"\D", "", str(mobile))
    return 10 <= len(digits) <= 13

def safe_filename(name):
    return re.sub(r"[^A-Za-z0-9._-]", "_", str(name))

def new_booking_id():
    return "BT" + datetime.now(IST).strftime("%d%m%H%M%S%f")[-12:]

def create_upi_url(amount):
    params = urllib.parse.urlencode({
        "pa": UPI_ID,
        "pn": "Balaji Logistics",
        "am": f"{float(amount):.2f}",
        "cu": "INR",
    })
    return "upi://pay?" + params

def whatsapp_url(message):
    return "https://wa.me/" + WA_LINK_NO + "?text=" + urllib.parse.quote(message)

def get_user_mobile(username):
    conn = get_db()
    row = conn.execute(
        "SELECT mobile FROM users WHERE username=?",
        (username,)
    ).fetchone()
    return row[0] if row else ""

def brand_card():
    st.markdown("""
    <div class="balaji-card">
        <p class="brand-title">🚩 BALAJI</p>
        <p class="brand-sub">LOGISTICS</p>
        <p class="brand-small">&amp; TOURS &amp; TRAVELS</p>
        <p class="brand-small" style="margin-top:16px;">🌍 All India Service</p>
    </div>
    """, unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = ""
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "language" not in st.session_state:
    st.session_state.language = "English"

if not st.session_state.logged_in:
    brand_card()
    st.write("")

    lang = st.selectbox(
        "🌐 Language / भाषा",
        ["English", "मराठी", "हिंदी"],
        index=["English", "मराठी", "हिंदी"].index(st.session_state.language),
        key="pre_language"
    )
    st.session_state.language = lang

    if lang == "मराठी":
        login_label = "लॉगिन"
        register_label = "रजिस्टर"
        option_label = "पर्याय निवडा"
    elif lang == "हिंदी":
        login_label = "लॉगिन"
        register_label = "रजिस्टर"
        option_label = "विकल्प चुनें"
    else:
        login_label = "Login"
        register_label = "Register"
        option_label = "Select Option"

    mode = st.radio(option_label, [login_label, register_label], horizontal=True)
    is_login = mode == login_label

    if is_login:
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login to App", use_container_width=True):
            username = username.strip()
            if not username or not password:
                st.warning("Please enter username and password.")
            else:
                conn = get_db()
                row = conn.execute(
                    "SELECT password FROM users WHERE username=?",
                    (username,)
                ).fetchone()
                if row and check_pw(password, row[0]):
                    st.session_state.logged_in = True
                    st.session_state.user = username
                    st.session_state.page = "Home"
                    st.rerun()
                else:
                    st.error("Wrong Username or Password!")
    else:
        new_username = st.text_input("Choose Username", key="register_username")
        new_mobile = st.text_input("Mobile Number", key="register_mobile")
        new_password = st.text_input("Create Password", type="password", key="register_password")

        if st.button("Register & Open App", use_container_width=True):
            new_username = new_username.strip()
            new_mobile = new_mobile.strip()

            if not new_username or not new_mobile or not new_password:
                st.warning("Please fill out all fields.")
            elif len(new_username) < 3:
                st.warning("Username must contain at least 3 characters.")
            elif not valid_mobile(new_mobile):
                st.warning("Please enter a valid mobile number.")
            elif len(new_password) < 4:
                st.warning("Password must contain at least 4 characters.")
            else:
                conn = get_db()
                exists = conn.execute(
                    "SELECT username FROM users WHERE username=?",
                    (new_username,)
                ).fetchone()

                if exists:
                    st.error("Username already exists!")
                else:
                    conn.execute(
                        "INSERT INTO users(username,password,mobile) VALUES(?,?,?)",
                        (new_username, hash_pw(new_password), new_mobile)
                    )
                    conn.commit()
                    st.session_state.logged_in = True
                    st.session_state.user = new_username
                    st.session_state.page = "Home"
                    st.success("Account Created! Opening app...")
                    st.rerun()

else:
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

    inverse = {v: k for k, v in page_mapping.items()}
    default_menu = inverse.get(st.session_state.page, "🏠 Home")

    selected_menu = st.selectbox(
        "📌 Menu Navigation",
        menu_options,
        index=menu_options.index(default_menu)
    )

    if selected_menu == "🚪 Logout":
        st.session_state.logged_in = False
        st.session_state.user = ""
        st.session_state.page = "Home"
        st.rerun()

    st.session_state.page = page_mapping[selected_menu]

    st.session_state.language = st.selectbox(
        "🌐 Language / भाषा",
        ["English", "मराठी", "हिंदी"],
        index=["English", "मराठी", "हिंदी"].index(st.session_state.language),
        key="main_language"
    )

    st.markdown("---")

    if st.session_state.page == "Home":
        brand_card()
        st.write("")
        st.success("WELCOME 🚗 SELECT 'BOOK' FROM MENU TO RIDE")
        st.subheader("📍 Our Service Hub (Nashik)")

        map_df = pd.DataFrame({"lat": [19.9975], "lon": [73.7898]})
        st.map(map_df, zoom=11)

        st.markdown(
            f"""
            <div style="text-align:center;margin-top:15px;">
                <a href="tel:{WA_LINK_NO}"
                   style="background:#25D366;color:white;padding:10px 20px;
                   border-radius:10px;text-decoration:none;font-weight:bold;">
                    📞 Call Support Now
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

    elif st.session_state.page == "Book":
        mob = get_user_mobile(st.session_state.user)

        st.markdown("""
        <div class="balaji-card">
            <h3 style="color:#FFBB00;margin:0;">🚗 Book Your Ride</h3>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        pickup = st.text_input("Pickup Location")
        drop = st.text_input("Drop Location")
        vehicle = st.selectbox("Select Vehicle", list(RATES.keys()))
        trip_type = st.radio("Trip Type", ["One-Way", "Round Trip"], horizontal=True)
        km = st.number_input("Estimated KM", min_value=1.0, value=50.0, step=1.0)
        payment = st.radio("Payment Method", ["Cash", "Online"], horizontal=True)

        st.markdown("""
        <div class="extra-note">
        🛣️ <b>Toll, parking and other applicable extra charges are extra
        and will be paid by the customer.</b>
        </div>
        """, unsafe_allow_html=True)

        base_fare = km * RATES[vehicle]
        fare = base_fare * 2 if trip_type == "Round Trip" else base_fare
        fare = round(fare, 2)

        st.info(f"Estimated Ride Fare: ₹{fare:.2f}  |  Toll/Parking: Extra")

        payment_file = None

        if payment == "Online":
            st.markdown("### 💳 UPI / QR Payment")
            upi_url = create_upi_url(fare)
            encoded_qr_data = urllib.parse.quote(upi_url, safe="")

            st.markdown(
                f"""
                <div style="background:#181818;padding:15px;border-radius:15px;
                text-align:center;border:2px solid #5f259f;">
                    <h3 style="color:#9b51e0;margin:0;">PhonePe / UPI</h3>
                    <p style="color:white;font-size:13px;">ACCEPTED HERE</p>
                    <div style="background:white;padding:10px;
                    display:inline-block;border-radius:10px;">
                        <img src="https://api.qrserver.com/v1/create-qr-code/?size=180x180&data={encoded_qr_data}" width="180">
                    </div>
                    <p style="color:#FFBB00;font-weight:bold;">
                        Amount: ₹{fare:.2f}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write("")
            st.link_button("📱 Open UPI Payment", upi_url, use_container_width=True)
            st.code(f"UPI ID: {UPI_ID}")

            payment_file = st.file_uploader(
                "Upload Payment Screenshot",
                type=["png", "jpg", "jpeg"],
                key="payment_screenshot"
            )

        st.write("")

        if st.button("Confirm Booking Now", use_container_width=True):
            pickup = pickup.strip()
            drop = drop.strip()

            if not pickup or not drop:
                st.warning("Please fill out both pickup and drop locations.")
            elif pickup.lower() == drop.lower():
                st.warning("Pickup and Drop locations should be different.")
            elif payment == "Online" and payment_file is None:
                st.warning("Please upload the payment screenshot.")
            else:
                booking_time = datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")
                booking_id = new_booking_id()
                screenshot_path = ""

                if payment_file:
                    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
                    filename = safe_filename(payment_file.name)
                    screenshot_path = str(UPLOAD_DIR / f"{booking_id}_{filename}")

                    with open(screenshot_path, "wb") as output_file:
                        output_file.write(payment_file.getbuffer())

                conn = get_db()
                conn.execute(
                    """
                    INSERT INTO bookings(
                        booking_id, username, date, from_loc, to_loc,
                        vehicle, fare, payment, mobile, screenshot,
                        status, trip_type, driver_name, driver_mobile
                    )
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    """,
                    (
                        booking_id,
                        st.session_state.user,
                        booking_time,
                        pickup,
                        drop,
                        vehicle,
                        fare,
                        payment,
                        mob,
                        screenshot_path,
                        "Confirmed",
                        trip_type,
                        "Not Assigned",
                        "Not Assigned",
                    )
                )
                conn.commit()

                st.success(f"Booking Confirmed 🎉 ID: {booking_id}")

                message = (
                    "🚩 BALAJI LOGISTICS & TOURS 🚩\n"
                    "━━━━━━━━━━━━━━━━━━\n"
                    f"🆔 Booking ID: {booking_id}\n"
                    f"🕒 Time: {booking_time}\n"
                    f"👤 Customer: {st.session_state.user}\n"
                    f"📞 Mobile: {mob}\n"
                    f"📍 Pickup: {pickup}\n"
                    f"🏁 Drop: {drop}\n"
                    f"🚗 Vehicle: {vehicle} ({trip_type})\n"
                    f"💰 Ride Fare: ₹{fare:.2f}\n"
                    f"💳 Payment: {payment}\n"
                    "🛣️ Toll/Parking/other applicable extra charges: Customer will pay extra.\n"
                    "\n"
                    "🌍 All India Service\n"
                    "⚡ Safe & Comfortable Ride\n"
                    "━━━━━━━━━━━━━━━━━━"
                )

                st.link_button(
                    "📲 Send Details on WhatsApp",
                    whatsapp_url(message),
                    use_container_width=True
                )

    elif st.session_state.page == "History":
        conn = get_db()

        user_df = pd.read_sql_query(
            """
            SELECT * FROM bookings
            WHERE username=?
            ORDER BY date DESC
            """,
            conn,
            params=(st.session_state.user,)
        )

        st.subheader("📜 Your Bookings")
        search_query = st.text_input("🔍 Search Booking by ID")

        if search_query and not user_df.empty:
            user_df = user_df[
                user_df["booking_id"].str.contains(
                    search_query.strip(),
                    case=False,
                    na=False
                )
            ]

        if user_df.empty:
            st.info("No bookings found.")
        else:
            for _, row in user_df.iterrows():
                status = row["status"]

                if status == "Confirmed":
                    status_color = "#00c853"
                elif status == "Completed":
                    status_color = "#ff9800"
                else:
                    status_color = "#ff5252"

                st.markdown(
                    f"""
                    <div class="booking-card">
                        <h4 style="margin:0 0 5px;">
                            🆔 {row['booking_id']}
                            <span style="color:{status_color};">| {status}</span>
                        </h4>
                        <p style="margin:3px 0;font-size:13px;">
                            🚗 <b>{row['vehicle']}</b> ({row['trip_type']})<br>
                            📍 {row['from_loc']} ➔ {row['to_loc']}<br>
                            💰 ₹{float(row['fare']):.2f} | 💳 {row['payment']}<br>
                            👨‍✈️ Driver: {row['driver_name']} ({row['driver_mobile']})<br>
                            🛣️ Toll/Parking: Extra, customer payable
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                col_invoice, col_cancel = st.columns(2)

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
Ride Fare    : Rs. {float(row['fare']):.2f}
Payment      : {row['payment']}
Toll/Parking : Extra - Customer Payable
Status       : {row['status']}
========================================
"""

                with col_invoice:
                    st.download_button(
                        label="📥 Invoice",
                        data=invoice_text,
                        file_name=f"Invoice_{row['booking_id']}.txt",
                        mime="text/plain",
                        key=f"invoice_{row['booking_id']}",
                        use_container_width=True
                    )

                if row["status"] == "Confirmed":
                    with col_cancel:
                        if st.button(
                            "❌ Cancel",
                            key=f"cancel_{row['booking_id']}",
                            use_container_width=True
                        ):
                            conn.execute(
                                """
                                UPDATE bookings
                                SET status='Cancelled'
                                WHERE booking_id=?
                                AND username=?
                                AND status='Confirmed'
                                """,
                                (row["booking_id"], st.session_state.user)
                            )
                            conn.commit()
                            st.success("Booking Cancelled!")
                            st.rerun()

    elif st.session_state.page == "Profile":
        st.subheader("👤 User Profile")

        current_mobile = get_user_mobile(st.session_state.user)

        new_mobile = st.text_input(
            "Update Mobile Number",
            value=current_mobile
        )

        new_password = st.text_input(
            "New Password (leave blank)",
            type="password"
        )

        if st.button("Update Profile", use_container_width=True):
            new_mobile = new_mobile.strip()

            if not new_mobile:
                st.warning("Mobile number cannot be empty.")
            elif not valid_mobile(new_mobile):
                st.warning("Please enter a valid mobile number.")
            elif new_password and len(new_password) < 4:
                st.warning("New password must contain at least 4 characters.")
            else:
                conn = get_db()

                if new_password:
                    conn.execute(
                        """
                        UPDATE users
                        SET mobile=?, password=?
                        WHERE username=?
                        """,
                        (new_mobile, hash_pw(new_password), st.session_state.user)
                    )
                else:
                    conn.execute(
                        """
                        UPDATE users
                        SET mobile=?
                        WHERE username=?
                        """,
                        (new_mobile, st.session_state.user)
                    )

                conn.commit()
                st.success("Profile Updated Successfully!")

    elif st.session_state.page == "Admin":
        st.subheader("🛠 Admin Panel")

        admin_password = st.text_input(
            "Enter Admin Password",
            type="password"
        )

        if admin_password == ADMIN_PASS:
            st.success("Admin Access Granted 🛠️")

            conn = get_db()

            df = pd.read_sql_query(
                """
                SELECT * FROM bookings
                ORDER BY date DESC
                """,
                conn
            )

            col1, col2, col3 = st.columns(3)
            col1.metric("Bookings", len(df))

            confirmed_df = (
                df[df["status"] == "Confirmed"]
                if not df.empty else df
            )

            revenue = (
                confirmed_df["fare"].sum()
                if not confirmed_df.empty else 0
            )

            col2.metric("Revenue", f"₹{revenue:.2f}")

            completed_count = (
                len(df[df["status"] == "Completed"])
                if not df.empty else 0
            )

            col3.metric("Completed", completed_count)

            if not df.empty:
                st.subheader("📊 Revenue Analytics")
                chart_data = df.groupby("vehicle")["fare"].sum()
                st.bar_chart(chart_data)

            st.subheader("📋 Bookings Database")

            if df.empty:
                st.info("No bookings yet.")
            else:
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )

                st.markdown("---")
                st.subheader("👨‍✈️ Manage Booking & Driver")

                booking_ids = df["booking_id"].tolist()

                selected_bid = st.selectbox(
                    "Select Booking ID",
                    booking_ids
                )

                selected_row = df[
                    df["booking_id"] == selected_bid
                ].iloc[0]

                screenshot = str(selected_row["screenshot"] or "")

                if screenshot and os.path.exists(screenshot):
                    st.image(
                        screenshot,
                        caption="Payment Screenshot",
                        width=250
                    )

                driver_name = st.text_input(
                    "Driver Name",
                    value=(
                        ""
                        if selected_row["driver_name"] == "Not Assigned"
                        else str(selected_row["driver_name"])
                    )
                )

                driver_mobile = st.text_input(
                    "Driver Mobile",
                    value=(
                        ""
                        if selected_row["driver_mobile"] == "Not Assigned"
                        else str(selected_row["driver_mobile"])
                    )
                )

                status_options = [
                    "Confirmed",
                    "Completed",
                    "Cancelled",
                ]

                current_status = (
                    selected_row["status"]
                    if selected_row["status"] in status_options
                    else "Confirmed"
                )

                new_status = st.selectbox(
                    "Update Status",
                    status_options,
                    index=status_options.index(current_status)
                )

                if st.button(
                    "Update Details",
                    use_container_width=True
                ):
                    if (
                        driver_mobile.strip()
                        and not valid_mobile(driver_mobile.strip())
                    ):
                        st.warning(
                            "Enter a valid driver mobile number."
                        )
                    else:
                        conn.execute(
                            """
                            UPDATE bookings
                            SET driver_name=?,
                                driver_mobile=?,
                                status=?
                            WHERE booking_id=?
                            """,
                            (
                                driver_name.strip() or "Not Assigned",
                                driver_mobile.strip() or "Not Assigned",
                                new_status,
                                selected_bid,
                            )
                        )

                        conn.commit()

                        st.success(
                            "Booking details updated!"
                        )
                        st.rerun()

        elif admin_password:
            st.error("Wrong Admin Password!")
