import streamlit as st
import time
import pandas as pd
import os
import hashlib
from datetime import datetime
import urllib.parse

# ================= CONFIG =================
WA_LINK_NO = "919767981986"   
CONTACT_NO = "9767981986"     
UPI_ID = "9309146504-2@ybl"  
PHONEPE_NO = "9309146504"

USER_DB = "users_data.csv"    
BOOKING_DB = "balaji_bookings.csv"

RATES = {"WagonR":11, "Swift Dzire":13, "Ertiga":18, "Innova":24, "Tempo Traveller":35}

st.set_page_config(page_title="Balaji Logistics", layout="wide")

# ================= FUNCTIONS =================
def make_hashes(password): return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password, hashed_text): return make_hashes(password) == hashed_text

# ================= DB =================
if not os.path.isfile(USER_DB):
    pd.DataFrame(columns=['username','password','mobile']).to_csv(USER_DB,index=False)

if not os.path.isfile(BOOKING_DB):
    pd.DataFrame(columns=['username','date','from_loc','to_loc','vehicle','fare','pay_mode','cust_mob']).to_csv(BOOKING_DB,index=False)

# ================= SESSION =================
if 'logged_in' not in st.session_state: st.session_state.logged_in=False
if 'user' not in st.session_state: st.session_state.user=""
if 'flash_done' not in st.session_state: st.session_state.flash_done=False
if 'page' not in st.session_state: st.session_state.page="🏠 Home"

# ================= FLASH =================
if not st.session_state.flash_done:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("""
        <div style='background:black;height:100vh;display:flex;justify-content:center;align-items:center;color:#FFBB00;font-size:40px;'>
        🚩 BALAJI
        </div>
        """, unsafe_allow_html=True)
        time.sleep(2)
    st.session_state.flash_done=True
    placeholder.empty()
    st.rerun()

# ================= UI =================
st.markdown("""
<style>
.stApp {background:linear-gradient(135deg,#000,#0a0a2e);color:white;}
.stButton>button {border-radius:10px;background:#111;color:white;}
.stButton>button:hover {background:#FFBB00;color:black;}
</style>
""", unsafe_allow_html=True)

# ================= AUTH =================
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center;color:#FFBB00;'>🚩 BALAJI LOGISTICS</h2>", unsafe_allow_html=True)
    auth = st.radio("Select", ["Login","Register"])

    if auth=="Login":
        u=st.text_input("Username")
        p=st.text_input("Password", type="password")
        if st.button("Login"):
            users=pd.read_csv(USER_DB)
            if u in users['username'].values:
                if check_hashes(p, users[users['username']==u]['password'].values[0]):
                    st.session_state.logged_in=True
                    st.session_state.user=u
                    st.rerun()
            st.error("Invalid")

    else:
        nu=st.text_input("Username")
        nm=st.text_input("Mobile")
        np=st.text_input("Password", type="password")
        if st.button("Register"):
            pd.DataFrame([[nu,make_hashes(np),nm]],columns=['username','password','mobile']).to_csv(USER_DB,mode='a',header=False,index=False)
            st.success("Registered!")

# ================= MAIN =================
else:
    col1,col2,col3,col4,col5 = st.columns(5)

    if col1.button("🏠 Home"): st.session_state.page="🏠 Home"
    if col2.button("📅 Book"): st.session_state.page="📅 Book"
    if col3.button("📜 Hist"): st.session_state.page="📜 Hist"
    if col4.button("👨‍💼 Admin"): st.session_state.page="Admin"
    if col5.button("🚪 Out"): st.session_state.logged_in=False; st.rerun()

    st.markdown("---")

    # ===== HOME =====
    if st.session_state.page=="🏠 Home":
        st.markdown("<h2 style='text-align:center;'>🚩 BALAJI LOGISTICS</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'>📞 {CONTACT_NO}</p>", unsafe_allow_html=True)

    # ===== BOOK =====
    elif st.session_state.page=="📅 Book":
        users_df=pd.read_csv(USER_DB)
        mob=users_df[users_df['username']==st.session_state.user]['mobile'].values[0]

        with st.form("booking"):
            s=st.text_input("Pickup")
            d=st.text_input("Drop")
            v=st.selectbox("Vehicle", list(RATES.keys()))
            km=st.number_input("KM", value=50)
            pay=st.radio("Payment", ["Cash","Online"])

            if st.form_submit_button("Confirm"):
                if s and d:
                    fare=km*RATES[v]

                    pd.DataFrame([[st.session_state.user,datetime.now(),s,d,v,fare,pay,mob]],
                    columns=['username','date','from_loc','to_loc','vehicle','fare','pay_mode','cust_mob']).to_csv(BOOKING_DB,mode='a',header=False,index=False)

                    msg=f"{s} to {d} ₹{fare}"
                    encoded=urllib.parse.quote(msg)

                    st.success(f"Booked ₹{fare}")

                    if pay=="Online":
                        st.warning(f"PhonePe: {PHONEPE_NO}")

                        upi=f"upi://pay?pa={UPI_ID}&pn=Balaji&am={fare}&cu=INR"
                        st.markdown(f"<a href='{upi}'><button>💳 Pay</button></a>", unsafe_allow_html=True)

                        file=st.file_uploader("Upload Screenshot")
                        if file:
                            if not os.path.exists("screenshots"):
                                os.makedirs("screenshots")
                            with open(f"screenshots/{time.time()}.png","wb") as f:
                                f.write(file.getbuffer())
                            st.success("Uploaded!")

                    st.markdown(f"[WhatsApp](https://wa.me/{WA_LINK_NO}?text={encoded})")

    # ===== HISTORY =====
    elif st.session_state.page=="📜 Hist":
        df=pd.read_csv(BOOKING_DB)
        st.dataframe(df[df['username']==st.session_state.user])

    # ===== ADMIN =====
    elif st.session_state.page=="Admin":
        st.subheader("👨‍💼 Admin Panel")

        df=pd.read_csv(BOOKING_DB)
        st.dataframe(df)

        st.write("Total Bookings:", len(df))
        st.write("Total Revenue:", df['fare'].sum())

        st.subheader("Screenshots")
        if os.path.exists("screenshots"):
            for f in os.listdir("screenshots"):
                st.image(f"screenshots/{f}", width=200)