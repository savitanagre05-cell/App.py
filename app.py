import streamlit as st
import pandas as pd
import os
import hashlib
from datetime import datetime, timezone, timedelta
import urllib.parse
import time
import sqlite3

# ================= IST TIMEZONE SETUP =================
IST = timezone(timedelta(hours=5, minutes=30))

# ================= CONFIG & DATABASE =================
WA_LINK_NO = "919767981986"
ADMIN_PASS = "12345"
UPI_ID = "9309146504-2@ybl"
DB_NAME = "balaji_logistics.db"

RATES = {
    "WagonR": 11,
    "Swift Dzire": 13,
    "Ertiga": 18,
    "Innova": 24,
    "Tempo Traveller": 35
}

st.set_page_config(page_title="Balaji Logistics & Tours", layout="wide", page_icon="🚗")

# ================= SQLITE DATABASE INITIALIZATION =================
def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            mobile TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id TEXT PRIMARY KEY,
            username TEXT,
            date TEXT,
            from_loc TEXT,
            to_loc TEXT,
            vehicle TEXT,
            fare REAL,
            payment TEXT,
            mobile TEXT,
            screenshot TEXT,
            status TEXT,
            trip_type TEXT,
            driver_name TEXT,
            driver_mobile TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ================= CUSTOM APP STYLING (UI/UX) =================
st.markdown("""
<style>
    /* Hide Streamlit default elements for App/WebView look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #0e0e0e;
        color: #ffffff;
    }
    .stButton>button {
        background: linear-gradient(135deg, #FFBB00, #e6a800);
        color: #000000;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        box-shadow: 0px 4px 10px rgba(255, 187, 0, 0.3);
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #ffcc33, #FFBB00);
        box-shadow: 0px 6px 15px rgba(255, 187, 0, 0.5);
    }
    input, select, textarea {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        border: 1px solid #333 !important;
    }
</style>
""", unsafe_allow_html=True)

# ================= FLASH SCREEN =================
if "flash_done" not in st.session_state:
    st.session_state.flash_done = False

if not st.session_state.flash_done:
    flash = st.empty()
    flash.markdown("""
<div style="display:flex;justify-content:center;align-items:center;height:80vh;
background: linear-gradient(135deg, #000000, #1a1a1a);border-radius:20px;">
<div style="background:#111;padding:40px;border-radius:20px;
box-shadow:0px 0px 30px rgba(255,187,0,0.4);text-align:center;width:90%;max-width:350px;">
<h1 style="color:#FFBB00;font-size:30px;">🚩 BALAJI</h1>
<h2 style="color:white;font-size:24px;">LOGISTICS</h2>
<p style="color:#bbbbbb;">& TOURS & TRAVELS</p>
<p style="color:white;">🌍 All India Service</p>
</div>
</div>
""", unsafe_allow_html=True)
    time.sleep(2)
    flash.empty()
    st.session_state.flash_done = True
    st.rerun()

# ================= HASHING =================
def hash_pw(p):
    return hashlib.sha256(str.encode(p)).hexdigest()

def check_pw(p, h):
    return hash_pw(p) == h

# ================= SESSION STATE =================
for k in ["logged_in", "user", "page"]:
    if k not in st.session_state:
        st.session_state[k] = False if k == "logged_in" else ""

if st.session_state.page == "":
    st.session_state.page = "Home"

# ================= LOGIN / REGISTER =================
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #FFBB00;'>🚩 BALAJI LOGISTICS & TOURS</h1>", unsafe_allow_html=True)
    
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        mode = st.radio("Select Option", ["Login", "Register"], horizontal=True)

        if mode == "Login":
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")

            if st.button("Login to App", use_container_width=True):
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cursor.execute("SELECT password FROM users WHERE username = ?", (u,))
                row = cursor.fetchone()
                conn.close()

                if row and check_pw(p, row[0]):
                    st.session_state.logged_in = True
                    st.session_state.user = u
                    st.rerun()
                else:
                    st.error("Wrong Username or Password!")
        else:
            nu = st.text_input("Choose Username")
            nm = st.text_input("Mobile Number")
            np = st.text_input("Create Password", type="password")

            if st.button("Register Account", use_container_width=True):
                if nu and nm and np:
                    conn = sqlite3.connect(DB_NAME)
                    cursor = conn.cursor()
                    cursor.execute("SELECT username FROM users WHERE username = ?", (nu,))
                    exists = cursor.fetchone()
                    if exists:
                        st.error("Username already exists!")
                    else:
                        cursor.execute("INSERT INTO users (username, password, mobile) VALUES (?, ?, ?)", 
                                       (nu, hash_pw(np), nm))
                        conn.commit()
                        st.success("Account Created Successfully! Please login now.")
                    conn.close()
                else:
                    st.warning("Please fill out all fields.")

# ================= MAIN APP =================
else:
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = "Home"
    with col2:
        if st.button("🚗 Book", use_container_width=True):
            st.session_state.page = "Book"
    with col3:
        if st.button("📜 History", use_container_width=True):
            st.session_state.page = "History"
    with col4:
        if st.button("👤 Profile", use_container_width=True):
            st.session_state.page = "Profile"
    with col5:
        if st.button("🛠 Admin", use_container_width=True):
            st.session_state.page = "Admin"
    with col6:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = ""
            st.session_state.page = "Home"
            st.rerun()

    st.markdown("---")

    # ---------------- HOME PAGE ----------------
    if st.session_state.page == "Home":
        st.markdown("""
<div style="background:#111;padding:30px;border-radius:20px;
box-shadow:0 0 20px rgba(255,187,0,0.3);text-align:center;">
<h2 style="color:#FFBB00; margin-bottom:5px;">🚩 BALAJI LOGISTICS</h2>
<p style="color:white; font-size:18px; font-weight:bold;">Tours & Travels</p>
<p style="color:#bbbbbb;">🌍 Maharashtra & All India Service (Nashik Based)</p>
<p style="color:#FFBB00;">🚗 Safe • Fast • Comfortable Rides</p>
</div>
""", unsafe_allow_html=True)

        st.write("")
        st.image(
            "https://cdn.pixabay.com/photo/2016/11/18/12/34/car-1835506_1280.jpg",
            use_container_width=True
        )
        st.success("WELCOME 🚗 BOOK YOUR RIDE NOW FROM THE MENU ABOVE")
        
        st.subheader("📍 Our Service Hub (Nashik, Maharashtra)")
        map_df = pd.DataFrame({'lat': [19.9975], 'lon': [73.7898]})
        st.map(map_df, zoom=11)

        st.markdown(f"""
        <div style="text-align:center; margin-top:20px;">
            <a href="tel:{WA_LINK_NO}" style="background-color:#25D366; color:white; padding:12px 25px; border-radius:10px; text-decoration:none; font-weight:bold; font-size:16px;">
                📞 Call Support Now
            </a>
        </div>
        """, unsafe_allow_html=True)

    # ---------------- BOOKING PAGE ----------------
    elif st.session_state.page == "Book":
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT mobile FROM users WHERE username = ?", (st.session_state.user,))
        user_row = cursor.fetchone()
        conn.close()
        mob = user_row[0] if user_row else ""

        st.markdown("""
<div style="background:#111;padding:20px;border-radius:20px;
box-shadow:0 0 15px rgba(255,187,0,0.2);text-align:center;">
<h3 style="color:#FFBB00; margin:0;">🚗 Book Your Ride</h3>
</div>
""", unsafe_allow_html=True)
        st.write("")

        s = st.text_input("Pickup Location")
        d = st.text_input("Drop Location")
        v = st.selectbox("Select Vehicle", list(RATES.keys()))
        trip_type = st.radio("Trip Type", ["One-Way", "Round Trip"], horizontal=True)
        km = st.number_input("Estimated KM", value=50, min_value=1)

        pay = st.radio("Payment Method", ["Cash", "Online"], horizontal=True)
        
        base_fare = km * RATES[v]
        fare = base_fare * 2 if trip_type == "Round Trip" else base_fare

        file = None
        if pay == "Online":
            st.markdown("### 💳 PhonePe UPI & QR Payment")
            
            st.markdown(f"""
            <div style="background:#181818; padding:20px; border-radius:15px; text-align:center; border:2px solid #5f259f; max-width:400px; margin:auto;">
                <h3 style="color:#9b51e0; margin:0;">PhonePe</h3>
                <p style="color:white; font-size:14px; margin:5px 0;">ACCEPTED HERE</p>
                <p style="color:#cccccc; font-size:12px;">Scan & Pay Using PhonePe App</p>
                <div style="background:white; padding:10px; display:inline-block; border-radius:10px; margin:10px 0;">
                    <img src="https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=upi://pay?pa={UPI_ID}&pn=Balaji&am={fare}&cu=INR" width="180">
                </div>
                <p style="color:#FFBB00; font-size:16px; font-weight:bold; margin:5px 0;">Amount: ₹{fare}</p>
                <p style="color:#888888; font-size:10px; margin:0;">© 2026, PhonePe Ltd</p>
            </div>
            """, unsafe_allow_html=True)

            st.write("")
            col_g, col_p = st.columns(2)
            with col_g:
                if st.button("📱 Open Google Pay", use_container_width=True):
                    upi_link = f"upi://pay?pa={UPI_ID}&pn=Balaji&am={fare}&cu=INR"
                    st.markdown(f"[Click here if GPay doesn't open]({upi_link})")
            with col_p:
                if st.button("📱 Open PhonePe", use_container_width=True):
                    upi_link = f"upi://pay?pa={UPI_ID}&pn=Balaji&am={fare}&cu=INR"
                    st.markdown(f"[Click here if PhonePe doesn't open]({upi_link})")

            st.code(f"UPI ID: {UPI_ID}")
            file = st.file_uploader("Upload Payment Screenshot", type=["png", "jpg", "jpeg"])

        st.write("")
        if st.button("Confirm Booking Now", use_container_width=True):
            if not s or not d:
                st.warning("Please fill out both pickup and drop locations.")
            else:
                booking_time_str = datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")
                bid = "BT" + datetime.now(IST).strftime("%d%H%M%S")

                img_path = ""
                if file:
                    os.makedirs("uploads", exist_ok=True)
                    img_path = f"uploads/{bid}_{file.name}"
                    with open(img_path, "wb") as f:
                        f.write(file.getbuffer())

                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO bookings (booking_id, username, date, from_loc, to_loc, vehicle, fare, payment, mobile, screenshot, status, trip_type, driver_name, driver_mobile)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (bid, st.session_state.user, booking_time_str, s, d, v, fare, pay, mob, img_path, "Confirmed", trip_type, "Not Assigned", "Not Assigned"))
                conn.commit()
                conn.close()

                st.success("Booking Confirmed 🎉 ID: " + bid)

                msg = (
                    "🚩 BALAJI LOGISTICS & TOURS 🚩\n"
                    "━━━━━━━━━━━━━━━\n"
                    f"🆔 Booking ID: {bid}\n"
                    f"🕒 Booking Time: {booking_time_str}\n"
                    f"👤 Customer: {st.session_state.user}\n"
                    f"📞 Mobile: {mob}\n"
                    f"📍 Pickup: {s}\n"
                    f"🏁 Drop: {d}\n"
                    f"🚗 Vehicle: {v}\n"
                    f"🔄 Trip Type: {trip_type}\n"
                    f"📏 Distance: {km} KM\n"
                    f"💰 Fare: ₹{fare}\n"
                    f"💳 Payment: {pay}\n\n"
                    "🌍 Maharashtra & All India Service\n"
                    "⚡ Safe • Fast • Comfortable Ride\n\n"
                    "⚠️ Note: Toll & Parking extra\n"
                    "━━━━━━━━━━━━━━━\n"
                    "🙏 Thank you for booking with us!"
                )

                link = urllib.parse.quote(msg)
                wa_url = "https://wa.me/" + WA_LINK_NO + "?text=" + link
                st.markdown(f"### [📲 Click to Send Booking Details on WhatsApp]({wa_url})")

    # ---------------- HISTORY PAGE ----------------
    elif st.session_state.page == "History":
        conn = sqlite3.connect(DB_NAME)
        user_df = pd.read_sql("SELECT * FROM bookings WHERE username = ?", conn, params=(st.session_state.user,))
        conn.close()

        st.subheader("📜 Your Booking History & Invoices")

        search_query = st.text_input("🔍 Search Booking by ID")
        if search_query and not user_df.empty:
            user_df = user_df[user_df["booking_id"].str.contains(search_query, case=False, na=False)]

        if user_df.empty:
            st.info("No bookings found. Book your first ride today!")
        else:
            for idx, r in user_df.iterrows():
                status_color = "green" if r["status"] == "Confirmed" else ("orange" if r["status"] == "Completed" else "red")
                st.markdown(f"""
                <div style="background:#1a1a1a; padding:15px; border-radius:10px; margin-bottom:15px; border-left: 5px solid #FFBB00;">
                    <h4>🆔 ID: {r['booking_id']} | Status: <span style="color:{status_color};">{r['status']}</span></h4>
                    <p style="margin:5px 0;">🚗 <b>{r['vehicle']}</b> ({r['trip_type']})<br>
                    📍 <b>From:</b> {r['from_loc']} ➔ <b>To:</b> {r['to_loc']}<br>
                    💰 <b>Fare:</b> ₹{r['fare']} | 💳 <b>Payment:</b> {r['payment']}<br>
                    👨‍✈️ <b>Driver:</b> {r['driver_name']} ({r['driver_mobile']})<br>
                    📅 <b>Date & Time:</b> {r['date']}</p>
                </div>
                """, unsafe_allow_html=True)

                col_inv, col_can = st.columns(2)
                invoice_text = f"""
========================================
       BALAJI LOGISTICS & TOURS
========================================
Booking ID   : {r['booking_id']}
Booking Time : {r['date']}
Customer     : {r['username']}
Mobile       : {r['mobile']}
Trip Type    : {r['trip_type']}
Vehicle      : {r['vehicle']}
Pickup       : {r['from_loc']}
Drop         : {r['to_loc']}
Driver Name  : {r['driver_name']}
Driver Mob   : {r['driver_mobile']}
Fare         : Rs. {r['fare']}
Payment      : {r['payment']}
Status       : {r['status']}
----------------------------------------
Note: Toll & Parking charges extra.
Thank you for choosing Balaji Logistics!
========================================
"""
                with col_inv:
                    st.download_button(
                        label="📥 Download Invoice",
                        data=invoice_text,
                        file_name=f"Invoice_{r['booking_id']}.txt",
                        mime="text/plain",
                        key=f"inv_{r['booking_id']}"
                    )

                if r["status"] == "Confirmed":
                    with col_can:
                        if st.button("❌ Cancel Booking", key=f"cancel_{r['booking_id']}"):
                            conn = sqlite3.connect(DB_NAME)
                            cursor = conn.cursor()
                            cursor.execute("UPDATE bookings SET status = 'Cancelled' WHERE booking_id = ?", (r["booking_id"],))
                            conn.commit()
                            conn.close()
                            st.success("Booking Cancelled Successfully!")
                            st.rerun()

    # ---------------- PROFILE PAGE ----------------
    elif st.session_state.page == "Profile":
        st.subheader("👤 User Profile Management")

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT mobile FROM users WHERE username = ?", (st.session_state.user,))
        current_mobile_row = cursor.fetchone()
        conn.close()
        current_mobile = current_mobile_row[0] if current_mobile_row else ""

        new_mob = st.text_input("Update Mobile Number", value=current_mobile)
        new_pass = st.text_input("New Password (leave blank to keep current)", type="password")

        if st.button("Update Profile Details"):
            if new_mob:
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                if new_pass:
                    cursor.execute("UPDATE users SET mobile = ?, password = ? WHERE username = ?", 
                                   (new_mob, hash_pw(new_pass), st.session_state.user))
                else:
                    cursor.execute("UPDATE users SET mobile = ? WHERE username = ?", 
                                   (new_mob, st.session_state.user))
                conn.commit()
                conn.close()
                st.success("Profile Updated Successfully!")
            else:
                st.warning("Mobile number cannot be empty.")

    # ---------------- ADMIN PAGE ----------------
    elif st.session_state.page == "Admin":
        pw = st.text_input("Enter Admin Password", type="password")

        if pw == ADMIN_PASS:
            st.success("Admin Access Granted 🛠️")
            conn = sqlite3.connect(DB_NAME)
            df = pd.read_sql("SELECT * FROM bookings", conn)
            conn.close()

            col_m1, col_m2 = st.columns(2)
            col_m1.metric("Total Bookings", len(df))
            
            valid_df = df[df["status"] == "Confirmed"] if not df.empty else df
            total_rev = valid_df["fare"].sum() if not valid_df.empty else 0
            col_m2.metric("Total Confirmed Revenue", f"₹{total_rev}")

            if not df.empty:
                st.subheader("📊 Revenue & Booking Analytics")
                chart_data = df.groupby("vehicle")["fare"].sum()
                st.bar_chart(chart_data)

            st.subheader("📋 All Bookings Database")
            st.dataframe(df, use_container_width=True)

            st.markdown("---")
            st.subheader("👨‍✈️ Manage Booking, Status & Assign Driver")
            if not df.empty:
                b_ids = df["booking_id"].tolist()
                selected_bid = st.selectbox("Select Booking ID", b_ids)
                
                selected_row = df[df["booking_id"] == selected_bid].iloc[0]
                
                if selected_row["screenshot"] and os.path.exists(str(selected_row["screenshot"])):
                    st.image(selected_row["screenshot"], caption="Payment Screenshot Uploaded", width=250)
           