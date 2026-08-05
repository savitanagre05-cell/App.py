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

# ================= FLASH SCREEN =================
if "flash_done" not in st.session_state:
    st.session_state.flash_done = False

if not st.session_state.flash_done:

    flash = st.empty()

    flash.markdown("""
<div style="display:flex;justify-content:center;align-items:center;height:80vh;
background: linear-gradient(135deg, #000000, #1a1a1a);border-radius:20px;">

<div style="background:#111;padding:40px;border-radius:20px;
box-shadow:0px 0px 30px rgba(255,187,0,0.3);text-align:center;width:90%;max-width:350px;">

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

# ================= INIT FILES & SCHEMAS =================
USER_COLS = ["username","password","mobile"]
BOOKING_COLS = ["booking_id","username","date","from_loc","to_loc","vehicle","fare","payment","mobile","screenshot","status","trip_type"]

if not os.path.exists(USER_DB):
    pd.DataFrame(columns=USER_COLS).to_csv(USER_DB, index=False)

if not os.path.exists(BOOKING_DB):
    pd.DataFrame(columns=BOOKING_COLS).to_csv(BOOKING_DB, index=False)

# ================= SAFE READ (Backward Compatible) =================
def safe_read(path, cols):
    try:
        df = pd.read_csv(path)
        for c in cols:
            if c not in df.columns:
                df[c] = ""
        return df
    except:
        return pd.DataFrame(columns=cols)

# ================= HASH =================
def hash_pw(p):
    return hashlib.sha256(str.encode(p)).hexdigest()

def check_pw(p, h):
    return hash_pw(p) == h

# ================= SESSION =================
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
                hashed = users[users["username"]==u]["password"].values[0]

                if check_pw(p, hashed):
                    st.session_state.logged_in = True
                    st.session_state.user = u
                    st.rerun()

            st.error("Wrong Login")

    else:
        nu = st.text_input("Username")
        nm = st.text_input("Mobile")
        np = st.text_input("Password", type="password")

        if st.button("Register"):
            if nu and nm and np:
                old = safe_read(USER_DB, USER_COLS)
                if nu in old["username"].values:
                    st.error("Username already exists!")
                else:
                    new = pd.DataFrame([[nu, hash_pw(np), nm]], columns=USER_COLS)
                    pd.concat([old, new], ignore_index=True).to_csv(USER_DB, index=False)
                    st.success("Account Created Successfully! Please login.")
            else:
                st.warning("Please fill out all fields.")

# ================= MAIN APP =================
else:

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        if st.button("🏠 Home"):
            st.session_state.page = "Home"

    with col2:
        if st.button("🚗 Book"):
            st.session_state.page = "Book"

    with col3:
        if st.button("📜 History"):
            st.session_state.page = "History"

    with col4:
        if st.button("👤 Profile"):
            st.session_state.page = "Profile"

    with col5:
        if st.button("🛠 Admin"):
            st.session_state.page = "Admin"

    with col6:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.user = ""
            st.session_state.page = "Home"
            st.rerun()

    st.markdown("---")

    # ================= HOME =================
    if st.session_state.page == "Home":

        st.markdown("""
<div style="background:#111;padding:25px;border-radius:20px;
box-shadow:0 0 15px rgba(255,187,0,0.2);text-align:center;">
<h2 style="color:#FFBB00;">🚩 BALAJI LOGISTICS</h2>
<p style="color:white;">Tours & Travels</p>
<p style="color:#bbbbbb;">🌍 Maharashtra & All India Service</p>
<p style="color:white;">🚗 Safe • Fast • Comfortable</p>
</div>
""", unsafe_allow_html=True)

        st.image(
            "https://cdn.pixabay.com/photo/2016/11/18/12/34/car-1835506_1280.jpg",
            width="stretch"
        )

        st.success("WELCOME 🚗 BOOK YOUR RIDE NOW")

    # ================= BOOK =================
    elif st.session_state.page == "Book":

        users = safe_read(USER_DB, USER_COLS)
        user_row = users[users["username"]==st.session_state.user]
        mob = user_row["mobile"].values[0] if not user_row.empty else ""

        st.markdown("""
<div style="background:#111;padding:20px;border-radius:20px;
box-shadow:0 0 15px rgba(255,187,0,0.2);text-align:center;">
<h3 style="color:#FFBB00;">🚗 Book Your Ride</h3>
</div>
""", unsafe_allow_html=True)

        s = st.text_input("Pickup Location")
        d = st.text_input("Drop Location")
        v = st.selectbox("Vehicle", list(RATES.keys()))
        trip_type = st.radio("Trip Type", ["One-Way", "Round Trip"])
        km = st.number_input("Estimated KM", value=50, min_value=1)

        pay = st.radio("Payment Method", ["Cash","Online"])
        
        base_fare = km * RATES[v]
        fare = base_fare * 2 if trip_type == "Round Trip" else base_fare

        file = None

        if pay == "Online":

            st.subheader("💳 Online Payment (UPI)")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("📱 Google Pay"):
                    upi_link = f"upi://pay?pa={UPI_ID}&pn=Balaji&am={fare}&cu=INR"
                    st.markdown(f"[Open GPay]({upi_link})")

            with col2:
                if st.button("📱 PhonePe"):
                    upi_link = f"upi://pay?pa={UPI_ID}&pn=Balaji&am={fare}&cu=INR"
                    st.markdown(f"[Open PhonePe]({upi_link})")

            st.code(f"UPI ID: {UPI_ID}")
            st.code(f"Amount: ₹{fare}")

            file = st.file_uploader("Upload Payment Screenshot", type=["png","jpg","jpeg"])

        if st.button("Confirm Booking"):
            if not s or not d:
                st.warning("Please fill out both pickup and drop locations.")
            else:
                booking_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                bid = "BT" + datetime.now().strftime("%d%H%M%S")

                img_path = ""
                if file:
                    os.makedirs("uploads", exist_ok=True)
                    img_path = f"uploads/{bid}_{file.name}"
                    with open(img_path, "wb") as f:
                        f.write(file.getbuffer())

                new = pd.DataFrame([[
                    bid,
                    st.session_state.user,
                    booking_time_str,
                    s, d, v, fare, pay, mob, img_path, "Confirmed", trip_type
                ]], columns=BOOKING_COLS)

                old = safe_read(BOOKING_DB, BOOKING_COLS)
                pd.concat([old, new], ignore_index=True).to_csv(BOOKING_DB, index=False)

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
                st.markdown(f"[📲 Send Details on WhatsApp]({wa_url})")

    # ================= HISTORY =================
    elif st.session_state.page == "History":

        df = safe_read(BOOKING_DB, BOOKING_COLS)
        user_df = df[df["username"] == st.session_state.user]

        st.subheader("📜 Your Booking History & Invoices")

        if user_df.empty:
            st.info("No bookings found. Book your first ride today!")
        else:
            for idx, r in user_df.iterrows():
                status_color = "green" if r["status"] == "Confirmed" else "red"
                st.markdown(f"""
                <div style="background:#1e1e1e; padding:15px; border-radius:10px; margin-bottom:10px;">
                    <h4>🆔 ID: {r['booking_id']} | Status: <span style="color:{status_color};">{r['status']}</span></h4>
                    <p>🚗 <b>{r['vehicle']}</b> ({r['trip_type']})<br>
                    📍 {r['from_loc']} ➔ {r['to_loc']}<br>
                    💰 Fare: ₹{r['fare']} | Payment: {r['payment']}<br>
                    📅 Date & Time: {r['date']}</p>
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
                            df.loc[df["booking_id"] == r["booking_id"], "status"] = "Cancelled"
                            df.to_csv(BOOKING_DB, index=False)
                            st.success("Booking Cancelled Successfully!")
                            st.rerun()

    # ================= PROFILE =================
    elif st.session_state.page == "Profile":
        st.subheader("👤 User Profile Management")

        users = safe_read(USER_DB, USER_COLS)
        current_user_row = users[users["username"] == st.session_state.user]
        current_mobile = current_user_row["mobile"].values[0] if not current_user_row.empty else ""

        new_mob = st.text_input("Update Mobile Number", value=current_mobile)
        new_pass = st.text_input("New Password (leave blank to keep current)", type="password")

        if st.button("Update Profile"):
            if new_mob:
                users.loc[users["username"] == st.session_state.user, "mobile"] = new_mob
                if new_pass:
                    users.loc[users["username"] == st.session_state.user, "password"] = hash_pw(new_pass)
                users.to_csv(USER_DB, index=False)
                st.success("Profile Updated Successfully!")
            else:
                st.warning("Mobile number cannot be empty.")

    # ================= ADMIN =================
    elif st.session_state.page == "Admin":

        pw = st.text_input("Admin Password", type="password")

        if pw == ADMIN_PASS:

            df = safe_read(BOOKING_DB, BOOKING_COLS)

            col1, col2 = st.columns(2)
            col1.metric("Total Bookings", len(df))
            
            valid_df = df[df["status"] == "Confirmed"] if not df.empty else df
            total_rev = valid_df["fare"].sum() if not valid_df.empty else 0
            col2.metric("Total Revenue", f"₹{total_rev}")

            st.subheader("All Bookings Data")
            st.dataframe(df, width="