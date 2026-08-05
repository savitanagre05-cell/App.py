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

st.set_page_config(page_title="Balaji Logistics & Tours", layout="centered", page_icon="🚗")

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

# ================= PERFECT MOBILE WEB-VIEW APP STYLING =================
st.markdown("""
<style>
    /* Hide Streamlit default elements for App/WebView look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #0e0e0e;
        color: #ffffff;
        max-width: 100% !important;
        overflow-x: hidden;
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
        width: 100%;
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
    /* Mobile Responsive Adjustments */
    .element-container, .stTextInput, .stSelectbox, .stRadio {
        width: 100% !important;
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
<div style="background:#111;padding:30px;border-radius:20px;
box-shadow:0px 0px 30px rgba(255,187,0,0.4);text-align:center;width:90%;max-width:320px;">
<h1 style="color:#FFBB00;font-size:26px;">🚩 BALAJI</h1>
<h2 style="color:white;font-size:20px;">LOGISTICS</h2>
<p style="color:#bbbbbb;font-size:14px;">& TOURS & TRAVELS</p>
<p style="color:white;font-size:12px;">🌍 All India Service</p>
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
    st.markdown("<h2 style='text-align: center; color: #FFBB00;'>🚩 BALAJI LOGISTICS</h2>", unsafe_allow_html=True)
    
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
                    st.success("Account Created! Please login.")
                conn.close()
            else:
                st.warning("Please fill out all fields.")

# ================= MAIN APP (MOBILE FRIENDLY NAVIGATION) =================
else:
    menu_options = ["🏠 Home", "🚗 Book", "📜 History", "👤 Profile", "🛠 Admin", "🚪 Logout"]
    
    page_mapping = {
        "🏠 Home": "Home",
        "🚗 Book": "Book",
        "📜 History": "History",
        "👤 Profile": "Profile",
        "🛠 Admin": "Admin",
        "🚪 Logout": "Logout"
    }
    
    current_inverse_mapping = {v: k for k, v in page_mapping.items()}
    default_selection = current_inverse_mapping.get(st.session_state.page, "🏠 Home")
    
    selected_menu = st.selectbox("📌 Menu Navigation", menu_options, index=menu_options.index(default_selection) if default_selection in menu_options else 0)
    
    if selected_menu == "🚪 Logout":
        st.session_state.logged_in = False
        st.session_state.user = ""
        st.session_state.page = "Home"
        st.rerun()
    else:
        st.session_state.page = page_mapping[selected_menu]

    st.markdown("---")

    # ---------------- HOME PAGE ----------------
    if st.session_state.page == "Home":
        st.markdown("""
<div style="background:#111;padding:20px;border-radius:15px;
box-shadow:0 0 15px rgba(255,187,0,0.3);text-align:center;">
<h3 style="color:#FFBB00; margin-bottom:5px;">🚩 BALAJI LOGISTICS</h3>
<p style="color:white; font-size:14px; font-weight:bold;">Tours & Travels</p>
<p style="color:#bbbbbb; font-size:12px;">🌍 Maharashtra & All India Service</p>
<p style="color:#FFBB00; font-size:12px;">🚗 Safe • Fast • Comfortable Rides</p>
</div>
""", unsafe_allow_html=True)

        st.write("")
        st.image(
            "https://cdn.pixabay.com/photo/2016/11/18/12/34/car-1835506_1280.jpg",
            use_container_width=True
        )
        st.success("WELCOME 🚗 SELECT 'BOOK' FROM MENU TO RIDE")
        
        st.subheader("📍 Our Service Hub (Nashik)")
        map_df = pd.DataFrame({'lat': [19.9975], 'lon': [73.7898]})
        st.map(map_df, zoom=11)

        st.markdown(f"""
        <div style="text-align:center; margin-top:15px;">
            <a href="tel:{WA_LINK_NO}" style="background-color:#25D366; color:white; padding:10px 20px; border-radius:10px; text-decoration:none; font-weight:bold; font-size:14px;">
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
<div style="background:#111;padding:15px;border-radius:15px;
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
            <div style="background:#181818; padding:15px; border-radius:15px; text-align:center; border:2px solid #5f259f; max-width:100%; margin:auto;">
                <h3 style="color:#9b51e0; margin:0;">PhonePe</h3>
                <p style="color:white; font-size:13px; margin:5px 0;">ACCEPTED HERE</p>
                <div style="background:white; padding:10px; display:inline-block; border-radius:10px; margin:10px 0;">
                    <img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi://pay?pa={UPI_ID}&pn=Balaji&am={fare}&cu=INR" width="150">
                </div>
                <p style="color:#FFBB00; font-size:15px; font-weight:bold; margin:5px 0;">Amount: ₹{fare}</p>
            </div>
            """, unsafe_allow_html=True)

            st.write("")
            col_g, col_p = st.columns(2)
            with col_g:
                if st.button("📱 GPay", use_container_width=True):
                    upi_link = f"upi://pay?pa={UPI_ID}&pn=Balaji&am={fare}&cu=INR"
                    st.markdown(f"[Open GPay]({upi_link})")
            with col_p:
                if st.button("📱 PhonePe", use_container_width=True):
                    upi_link = f"upi://pay?pa={UPI_ID}&pn=Balaji&am={fare}&cu=INR"
                    st.markdown(f"[Open PhonePe]({upi_link})")

            st.code(f"UPI: {UPI_ID}")
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
                    f"🕒 Time: {booking_time_str}\n"
                    f"👤 Customer: {st.session_state.user}\n"
                    f"📞 Mobile: {mob}\n"
                    f"📍 Pickup: {s}\n"
                    f"🏁 Drop: {d}\n"
                    f"🚗 Vehicle: {v} ({trip_type})\n"
                    f"💰 Fare: ₹{fare}\n"
                    f"💳 Payment: {pay}\n\n"
                    "🌍 All India Service\n"
                    "⚡ Safe & Comfortable Ride\n"
                    "━━━━━━━━━━━━━━━"
                )

                link = urllib.parse.quote(msg)
                wa_url = "https://wa.me/" + WA_LINK_NO + "?text=" + link
                st.markdown(f"### [📲 Send Details on WhatsApp]({wa_url})")

    # ---------------- HISTORY PAGE ----------------
    elif st.session_state.page == "History":
        conn = sqlite3.connect(DB_NAME)
        user_df = pd.read_sql("SELECT * FROM bookings WHERE username = ?", conn, params=(st.session_state.user,))
        conn.close()

        st.subheader("📜 Your Bookings")

        search_query = st.text_input("🔍 Search Booking by ID")
        if search_query and not user_df.empty:
            user_df = user_df[user_df["booking_id"].str.contains(search_query, case=False, na=False)]

        if user_df.empty:
            st.info("No bookings found.")
        else:
            for idx, r in user_df.iterrows():
                status_color = "green" if r["status"] == "Confirmed" else ("orange" if r["status"] == "Completed" else "red")
                st.markdown(f"""
                <div style="background:#1a1a1a; padding:12px; border-radius:10px; margin-bottom:12px; border-left: 5px solid #FFBB00;">
                    <h4 style="margin:0 0 5px 0; font-size:15px;">🆔 {r['booking_id']} | <span style="color:{status_color};">{r['status']}</span></h4>
                    <p style="margin:3px 0; font-size:13px;">🚗 <b>{r['vehicle']}</b> ({r['trip_type']})<br>
                    📍 {r['from_loc']} ➔ {r['to_loc']}<br>
                    💰 ₹{r['fare']} | 💳 {r['payment']}<br>
                    👨‍✈️ Driver: {r['driver_name']} ({r['driver_mobile']})</p>
                </div>
                """, unsafe_allow_html=True)

                col_inv, col_can = st.columns(2)
                invoice_text = f"""
========================================
       BALAJI LOGISTICS & TOURS
========================================
Booking ID   : {r['booking_id']}
Date         : {r['date']}
Customer     : {r['username']}
Vehicle      : {r['vehicle']} ({r['trip_type']})
Pickup       : {r['from_loc']}
Drop         : {r['to_loc']}
Driver       : {r['driver_name']} ({r['driver_mobile']})
Fare         : Rs. {r['fare']}
Status       : {r['status']}
========================================
"""
                with col_inv:
                    st.download_button(
                        label="📥 Invoice",
                        data=invoice_text,
                        file_name=f"Invoice_{r['booking_id']}.txt",
                        mime="text/plain",
                        key=f"inv_{r['booking_id']}"
                    )

                if r["status"] == "Confirmed":
                    with col_can:
                        if st.button("❌ Cancel", key=f"cancel_{r['booking_id']}"):
                            conn = sqlite3.connect(DB_NAME)
                            cursor = conn.cursor()
                            cursor.execute("UPDATE bookings SET status = 'Cancelled' WHERE booking_id = ?", (r["booking_id"],))
                            conn.commit()
                            conn.close()
                            st.success("Cancelled!")
                            st.rerun()

    # ---------------- PROFILE PAGE ----------------
    elif st.session_state.page == "Profile":
        st.subheader("👤 User Profile")

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT mobile FROM users WHERE username = ?", (st.session_state.user,))
        current_mobile_row = cursor.fetchone()
        conn.close()
        current_mobile = current_mobile_row[0] if current_mobile_row else ""

        new_mob = st.text_input("Update Mobile Number", value=current_mobile)
        new_pass = st.text_input("New Password (leave blank)", type="password")

        if st.button("Update Profile", use_container_width=True):
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
            col_m1.metric("Bookings", len(df))
            
            valid_df = df[df["status"] == "Confirmed"] if not df.empty else df
            total_rev = valid_df["fare"].sum() if not valid_df.empty else 0
            col_m2.metric("Revenue", f"₹{total_rev}")

            if not df.empty:
                st.subheader("📊 Revenue Analytics")
                chart_data = df.groupby("vehicle")["fare"].sum()
                st.bar_chart(chart_data)

            st.subheader("📋 Bookings Database")
            st.dataframe(df, use_container_width=True)

            st.markdown("---")
            st.subheader("👨‍✈️ Manage Booking & Driver")
            if not df.empty:
                b_ids = df["booking_id"].tolist()
                selected_bid = st.selectbox("Select Booking ID", b_ids)
                
                selected_row = df[df["booking_id"] == selected_bid].iloc[0]
                
                if selected_row["screenshot"] and os.path.exists(str(selected_row["screenshot"])):
                    st.image(selected_row["screenshot"], caption="Payment Screenshot", width=200)
                
                d_name = st.text_input("Driver Name", value=str(selected_row["driver_name"]) if selected_row["driver_name"] != "Not Assigned" else "")
                d_mob = st.text_input("Driver Mobile", value=str(selected_row["driver_mobile"]) if selected_row["driver_mobile"] != "Not Assigned" else "")
                new_status = st.selectbox("Update Status", ["Confirmed", "Completed", "Cancelled"], index=["Confirmed", "Completed", "Cancelled"].index(selected_row["status"]) if selected_row["status"] in ["Confirmed", "Completed", "Cancelled"] else 0)

                if st.button("Update Details", use_container_width=True):
                    conn = sqlite3.connect(DB_NAME)
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE bookings 
                        SET driver_name = ?, driver_mobile = ?, status = ? 
                        WHERE booking_id = ?
                    """, (d_name if d_name else "Not Assigned", d_mob if d_mob else "Not Assigned", new_status, selected_bid))
                    conn.commit()
                    conn.close()
                    st.success("Updated successfully!")
                    st.rerun()