import streamlit as st
import pandas as pd
import os
import hashlib
from datetime import datetime, timezone, timedelta
import urllib.parse
import sqlite3
import uuid
import re

# ============================================================
# BALAJI LOGISTICS & TOURS
# Existing app + stability / production modifications
# ============================================================

IST = timezone(timedelta(hours=5, minutes=30))

# ---------------- CONFIG ----------------
WA_LINK_NO = os.getenv("WA_LINK_NO", "919767981986")
ADMIN_PASS = os.getenv("ADMIN_PASS", "12345")
UPI_ID = os.getenv("UPI_ID", "9309146504-2@ybl")
DB_NAME = os.getenv("DB_NAME", "balaji_logistics.db")

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
    page_icon="🚗",
    initial_sidebar_state="collapsed",
)

# ============================================================
# DATABASE
# ============================================================

def get_conn():
    conn = sqlite3.connect(DB_NAME, timeout=20, check_same_thread=False)
    conn.execute("PRAGMA busy_timeout = 20000")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_conn()
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
            screenshot TEXT,
            status TEXT NOT NULL,
            trip_type TEXT NOT NULL,
            driver_name TEXT,
            driver_mobile TEXT
        )
    """)

    conn.commit()
    conn.close()


init_db()

# ============================================================
# HELPERS
# ============================================================

def hash_pw(password):
    return hashlib.sha256(str(password).encode("utf-8")).hexdigest()


def check_pw(password, hashed):
    return hash_pw(password) == hashed


def clean_filename(filename):
    filename = os.path.basename(filename)
    return re.sub(r"[^A-Za-z0-9._-]", "_", filename)


def make_booking_id():
    # UUID prevents two bookings made in the same second
    return "BT" + datetime.now(IST).strftime("%d%H%M%S") + uuid.uuid4().hex[:5].upper()


def valid_mobile(mobile):
    digits = re.sub(r"\D", "", str(mobile))
    return len(digits) >= 10 and len(digits) <= 13


def get_user_mobile(username):
    conn = get_conn()
    row = conn.execute(
        "SELECT mobile FROM users WHERE username = ?",
        (username,),
    ).fetchone()
    conn.close()
    return row[0] if row else ""


def save_uploaded_file(uploaded_file, booking_id):
    if uploaded_file is None:
        return ""

    os.makedirs("uploads", exist_ok=True)
    safe_name = clean_filename(uploaded_file.name)
    path = os.path.join("uploads", f"{booking_id}_{safe_name}")

    with open(path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    return path


def build_whatsapp_message(
    bid, booking_time, username, mobile,
    pickup, drop, vehicle, trip_type, fare, payment
):
    return (
        "🚩 BALAJI LOGISTICS & TOURS 🚩\n"
        "━━━━━━━━━━━━━━━\n"
        f"🆔 Booking ID: {bid}\n"
        f"🕒 Time: {booking_time}\n"
        f"👤 Customer: {username}\n"
        f"📞 Mobile: {mobile}\n"
        f"📍 Pickup: {pickup}\n"
        f"🏁 Drop: {drop}\n"
        f"🚗 Vehicle: {vehicle} ({trip_type})\n"
        f"💰 Fare: ₹{fare:.2f}\n"
        f"💳 Payment: {payment}\n\n"
        "🌍 All India Service\n"
        "⚡ Safe & Comfortable Ride\n"
        "━━━━━━━━━━━━━━━"
    )


# ============================================================
# STYLE
# ============================================================

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

.stButton > button {
    background: linear-gradient(135deg, #FFBB00, #e6a800);
    color: #000000;
    font-weight: bold;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
    box-shadow: 0px 4px 10px rgba(255, 187, 0, 0.3);
    width: 100%;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #ffcc33, #FFBB00);
    box-shadow: 0px 6px 15px rgba(255, 187, 0, 0.5);
}

input, select, textarea {
    background-color: #1a1a1a !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    border: 1px solid #333 !important;
}

[data-testid="stFileUploader"] {
    background-color: #151515;
    border-radius: 10px;
}

.mobile-card {
    background: #111;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0 0 15px rgba(255,187,0,0.20);
    text-align: center;
}

.small-note {
    color: #aaaaaa;
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = ""

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "flash_done" not in st.session_state:
    st.session_state.flash_done = False

# ============================================================
# FLASH SCREEN
# FIX: no time.sleep(), so the app does not block for 2 seconds
# ============================================================

if not st.session_state.flash_done:
    st.markdown("""
    <div style="
        display:flex;
        justify-content:center;
        align-items:center;
        height:70vh;
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

# ============================================================
# LOGIN / REGISTER
# ============================================================

if not st.session_state.logged_in:

    st.markdown(
        "<h2 style='text-align:center;color:#FFBB00;'>🚩 BALAJI LOGISTICS</h2>",
        unsafe_allow_html=True,
    )

    mode = st.radio(
        "Select Option",
        ["Login", "Register"],
        horizontal=True,
    )

    if mode == "Login":

        u = st.text_input("Username", key="login_username")
        p = st.text_input(
            "Password",
            type="password",
            key="login_password",
        )

        if st.button("Login to App", use_container_width=True):

            if not u.strip() or not p:
                st.warning("Please enter Username and Password.")
            else:
                conn = get_conn()
                row = conn.execute(
                    "SELECT password FROM users WHERE username = ?",
                    (u.strip(),),
                ).fetchone()
                conn.close()

                if row and check_pw(p, row[0]):
                    st.session_state.logged_in = True
                    st.session_state.user = u.strip()
                    st.session_state.page = "Home"
                    st.rerun()
                else:
                    st.error("Wrong Username or Password!")

    else:

        nu = st.text_input("Choose Username", key="register_username")
        nm = st.text_input(
            "Mobile Number",
            key="register_mobile",
            max_chars=13,
        )
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
                st.warning("Please enter a valid mobile number.")

            elif len(np) < 4:
                st.warning("Password must contain at least 4 characters.")

            else:
                conn = get_conn()
                exists = conn.execute(
                    "SELECT username FROM users WHERE username = ?",
                    (nu,),
                ).fetchone()

                if exists:
                    st.error("Username already exists!")
                else:
                    conn.execute(
                        """
                        INSERT INTO users(username,password,mobile)
                        VALUES(?,?,?)
                        """,
                        (nu, hash_pw(np), nm),
                    )
                    conn.commit()
                    st.success("Account Created! Please login.")

                conn.close()

# ============================================================
# MAIN APP
# ============================================================

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

    current_inverse_mapping = {
        value: key for key, value in page_mapping.items()
    }

    default_selection = current_inverse_mapping.get(
        st.session_state.page,
        "🏠 Home",
    )

    selected_menu = st.selectbox(
        "📌 Menu Navigation",
        menu_options,
        index=(
            menu_options.index(default_selection)
            if default_selection in menu_options
            else 0
        ),
    )

    if selected_menu == "🚪 Logout":
        st.session_state.logged_in = False
        st.session_state.user = ""
        st.session_state.page = "Home"
        st.rerun()
    else:
        st.session_state.page = page_mapping[selected_menu]

    st.markdown("---")

    # ========================================================
    # HOME
    # ========================================================

    if st.session_state.page == "Home":

        st.markdown("""
        <div class="mobile-card">
            <h3 style="color:#FFBB00;margin-bottom:5px;">
                🚩 BALAJI LOGISTICS
            </h3>
            <p style="color:white;font-size:14px;font-weight:bold;">
                Tours & Travels
            </p>
            <p style="color:#bbbbbb;font-size:12px;">
                🌍 Maharashtra & All India Service
            </p>
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

    # ========================================================
    # BOOKING
    # ========================================================

    elif st.session_state.page == "Book":

        mob = get_user_mobile(st.session_state.user)

        st.markdown("""
        <div class="mobile-card">
            <h3 style="color:#FFBB00;margin:0;">
                🚗 Book Your Ride
            </h3>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        s = st.text_input("Pickup Location", key="pickup")
        d = st.text_input("Drop Location", key="drop")

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
            max_value=10000,
            step=1,
        )

        pay = st.radio(
            "Payment Method",
            ["Cash", "Online"],
            horizontal=True,
        )

        base_fare = km * RATES[v]
        fare = base_fare * 2 if trip_type == "Round Trip" else base_fare

        st.info(f"💰 Estimated Fare: ₹{fare:.2f}")

        uploaded_file = None

        if pay == "Online":

            st.markdown("### 💳 PhonePe UPI & QR Payment")

            # URL encode UPI data safely
            upi_data = (
                f"upi://pay?pa={urllib.parse.quote(UPI_ID)}"
                f"&pn={urllib.parse.quote('Balaji')}"
                f"&am={fare:.2f}&cu=INR"
            )

            qr_url = (
                "https://api.qrserver.com/v1/create-qr-code/"
                f"?size=150x150&data={urllib.parse.quote(upi_data)}"
            )

            st.markdown(
                f"""
                <div style="
                    background:#181818;
                    padding:15px;
                    border-radius:15px;
                    text-align:center;
                    border:2px solid #5f259f;
                    max-width:100%;
                    margin:auto;">

                    <h3 style="color:#9b51e0;margin:0;">
                        PhonePe
                    </h3>

                    <p style="color:white;font-size:13px;">
                        ACCEPTED HERE
                    </p>

                    <div style="
                        background:white;
                        padding:10px;
                        display:inline-block;
                        border-radius:10px;
                        margin:10px 0;">
                        <img src="{qr_url}" width="150">
                    </div>

                    <p style="
                        color:#FFBB00;
                        font-size:15px;
                        font-weight:bold;">
                        Amount: ₹{fare:.2f}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.write("")

            col_g, col_p = st.columns(2)

            with col_g:
                st.markdown(
                    f"[📱 Open GPay]({upi_data})"
                )

            with col_p:
                st.markdown(
                    f"[📱 Open PhonePe]({upi_data})"
                )

            st.code(f"UPI: {UPI_ID}")

            uploaded_file = st.file_uploader(
                "Upload Payment Screenshot",
                type=["png", "jpg", "jpeg"],
                key="payment_screenshot",
            )

        st.write("")

        if st.button(
            "Confirm Booking Now",
            use_container_width=True,
        ):

            pickup = s.strip()
            drop = d.strip()

            if not pickup or not drop:
                st.warning(
                    "Please fill out both pickup and drop locations."
                )

            elif len(pickup) > 200 or len(drop) > 200:
                st.warning(
                    "Location name is too long. Please keep it below 200 characters."
                )

            else:

                booking_time_str = datetime.now(IST).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                bid = make_booking_id()

                img_path = ""

                try:
                    img_path = save_uploaded_file(
                        uploaded_file,
                        bid,
                    )

                    conn = get_conn()

                    conn.execute(
                        """
                        INSERT INTO bookings
                        (
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
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                        """,
                        (
                            bid,
                            st.session_state.user,
                            booking_time_str,
                            pickup,
                            drop,
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

                except Exception as e:

                    st.error(
                        "Booking save nahi ho paya. Please try again."
                    )

                    # Remove uploaded file if database insert failed
                    if img_path and os.path.exists(img_path):
                        try:
                            os.remove(img_path)
                        except OSError:
                            pass

                    st.stop()

                st.success(
                    f"Booking Confirmed 🎉 ID: {bid}"
                )

                msg = build_whatsapp_message(
                    bid,
                    booking_time_str,
                    st.session_state.user,
                    mob,
                    pickup,
                    drop,
                    v,
                    trip_type,
                    fare,
                    pay,
                )

                link = urllib.parse.quote(msg)

                wa_url = (
                    "https://wa.me/"
                    + WA_LINK_NO
                    + "?text="
                    + link
                )

                st.markdown(
                    f"### [📲 Send Details on WhatsApp]({wa_url})"
                )

    # ========================================================
    # HISTORY
    # ========================================================

    elif st.session_state.page == "History":

        conn = get_conn()

        user_df = pd.read_sql(
            """
            SELECT *
            FROM bookings
            WHERE username = ?
            ORDER BY rowid DESC
            """,
            conn,
            params=(st.session_state.user,),
        )

        conn.close()

        st.subheader("📜 Your Bookings")

        search_query = st.text_input(
            "🔍 Search Booking by ID"
        )

        if search_query and not user_df.empty:
            user_df = user_df[
                user_df["booking_id"]
                .str.contains(
                    search_query.strip(),
                    case=False,
                    na=False,
                )
            ]

        if user_df.empty:

            st.info("No bookings found.")

        else:

            for _, r in user_df.iterrows():

                status_color = (
                    "green"
                    if r["status"] == "Confirmed"
                    else (
                        "orange"
                        if r["status"] == "Completed"
                        else "red"
                    )
                )

                st.markdown(
                    f"""
                    <div style="
                        background:#1a1a1a;
                        padding:12px;
                        border-radius:10px;
                        margin-bottom:12px;
                        border-left:5px solid #FFBB00;">

                        <h4 style="
                            margin:0 0 5px 0;
                            font-size:15px;">

                            🆔 {r['booking_id']}
                            |
                            <span style="color:{status_color};">
                                {r['status']}
                            </span>

                        </h4>

                        <p style="
                            margin:3px 0;
                            font-size:13px;">

                            🚗 <b>{r['vehicle']}</b>
                            ({r['trip_type']})<br>

                            📍 {r['from_loc']}
                            ➔
                            {r['to_loc']}<br>

                            💰 ₹{float(r['fare']):.2f}
                            |
                            💳 {r['payment']}<br>

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
Customer     : {r['username']}
Mobile       : {r['mobile']}
Vehicle      : {r['vehicle']} ({r['trip_type']})
Pickup       : {r['from_loc']}
Drop         : {r['to_loc']}
Driver       : {r['driver_name']} ({r['driver_mobile']})
Fare         : Rs. {float(r['fare']):.2f}
Payment      : {r['payment']}
Status       : {r['status']}
========================================
"""

                with col_inv:

                    st.download_button(
                        label="📥 Invoice",
                        data=invoice_text,
                        file_name=(
                            f"Invoice_{r['booking_id']}.txt"
                        ),
                        mime="text/plain",
                        key=f"inv_{r['booking_id']}",
                    )

                if r["status"] == "Confirmed":

                    with col_can:

                        if st.button(
                            "❌ Cancel",
                            key=f"cancel_{r['booking_id']}",
                        ):

                            conn = get_conn()

                            conn.execute(
                                """
                                UPDATE bookings
                                SET status = 'Cancelled'
                                WHERE booking_id = ?
                                AND username = ?
                                AND status = 'Confirmed'
                                """,
                                (
                                    r["booking_id"],
                                    st.session_state.user,
                                ),
                            )

                            conn.commit()
                            conn.close()

                            st.success("Cancelled!")

                            st.rerun()

    # ========================================================
    # PROFILE
    # ========================================================

    elif st.session_state.page == "Profile":

        st.subheader("👤 User Profile")

        current_mobile = get_user_mobile(
            st.session_state.user
        )

        new_mob = st.text_input(
            "Update Mobile Number",
            value=current_mobile,
            max_chars=13,
        )

        new_pass = st.text_input(
            "New Password (leave blank)",
            type="password",
        )

        if st.button(
            "Update Profile",
            use_container_width=True,
        ):

            new_mob = new_mob.strip()

            if not new_mob:

                st.warning(
                    "Mobile number cannot be empty."
                )

            elif not valid_mobile(new_mob):

                st.warning(
                    "Please enter a valid mobile number."
                )

            else:

                conn = get_conn()

                if new_pass:

                    if len(new_pass) < 4:
                        conn.close()
                        st.warning(
                            "New password must contain at least 4 characters."
                        )
                        st.stop()

                    conn.execute(
                        """
                        UPDATE users
                        SET mobile = ?, password = ?
                        WHERE username = ?
                        """,
                        (
                            new_mob,
                            hash_pw(new_pass),
                            st.session_state.user,
                        ),
                    )

                else:

                    conn.execute(
                        """
                        UPDATE users
                        SET mobile = ?
                        WHERE username = ?
                        """,
                        (
                            new_mob,
                            st.session_state.user,
                        ),
                    )

                conn.commit()
                conn.close()

                st.success(
                    "Profile Updated Successfully!"
                )

    # ========================================================
    # ADMIN
    # ========================================================

    elif st.session_state.page == "Admin":

        pw = st.text_input(
            "Enter Admin Password",
            type="password",
        )

        if pw == ADMIN_PASS:

            st.success(
                "Admin Access Granted 🛠️"
            )

            conn = get_conn()

            df = pd.read_sql(
                """
                SELECT *
                FROM bookings
                ORDER BY rowid DESC
                """,
                conn,
            )

            conn.close()

            col_m1, col_m2 = st.columns(2)

            col_m1.metric(
                "Bookings",
                len(df),
            )

            valid_df = (
                df[df["status"] == "Confirmed"]
                if not df.empty
                else df
            )

            total_rev = (
                valid_df["fare"].sum()
                if not valid_df.empty
                else 0
            )

            col_m2.metric(
                "Revenue",
                f"₹{total_rev:.2f}",
            )

            if not df.empty:

                st.subheader(
                    "📊 Revenue Analytics"
                )

                chart_data = (
                    df.groupby("vehicle")["fare"]
                    .sum()
                )

                st.bar_chart(chart_data)

            st.subheader(
                "📋 Bookings Database"
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
            )

            st.markdown("---")

            st.subheader(
                "👨‍✈️ Manage Booking & Driver"
            )

            if not df.empty:

                b_ids = df["booking_id"].tolist()

                selected_bid = st.selectbox(
                    "Select Booking ID",
                    b_ids,
                )

                selected_rows = df[
                    df["booking_id"] == selected_bid
                ]

                selected_row = selected_rows.iloc[0]

                screenshot = str(
                    selected_row["screenshot"]
                )

                if (
                    screenshot
                    and screenshot != "nan"
                    and os.path.exists(screenshot)
                ):
                    st.image(
                        screenshot,
                        caption="Payment Screenshot",
                        width=200,
                    )

                current_driver_name = (
                    ""
                    if selected_row["driver_name"]
                    in ["Not Assigned", "nan", None]
                    else str(
                        selected_row["driver_name"]
                    )
                )

                current_driver_mobile = (
                    ""
                    if selected_row["driver_mobile"]
                    in ["Not Assigned", "nan", None]
                    else str(
                        selected_row["driver_mobile"]
                    )
                )

                d_name = st.text_input(
                    "Driver Name",
                    value=current_driver_name,
                )

                d_mob = st.text_input(
                    "Driver Mobile",
                    value=current_driver_mobile,
                    max_chars=13,
                )

                statuses = [
                    "Confirmed",
                    "Completed",
                    "Cancelled",
                ]

                current_status = str(
                    selected_row["status"]
                )

                status_index = (
                    statuses.index(current_status)
                    if current_status in statuses
                    else 0
                )

                new_status = st.selectbox(
                    "Update Status",
                    statuses,
                    index=status_index,
                )

                if st.button(
                    "Update Details",
                    use_container_width=True,
                ):

                    d_name = d_name.strip()
                    d_mob = d_mob.strip()

                    if d_mob and not valid_mobile(d_mob):
                        st.warning(
                            "Please enter a valid driver mobile number."
                        )
                        st.stop()

                    conn = get_conn()

                    conn.execute(
                        """
                        UPDATE bookings
                        SET
                            driver_name = ?,
                            driver_mobile = ?,
                            status = ?
                        WHERE booking_id = ?
                        """,
                        (
                            d_name
                            if d_name
                            else "Not Assigned",
                            d_mob
                            if d_mob
                            else "Not Assigned",
                            new_status,
                            selected_bid,
                        ),
                    )

                    conn.commit()
                    conn.close()

                    st.success(
                        "Updated successfully!"
                    )

                    st.rerun()

            else:

                st.info(
                    "No bookings available."
                )
