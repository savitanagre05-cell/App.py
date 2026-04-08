import streamlit as st
import urllib.parse, folium, os, pandas as pd
from streamlit_folium import st_folium

# 1. Main Settings
st.set_page_config(page_title="Balaji Logistics", layout="centered", page_icon="📦")
MY_NO = "9767981986"
DB_FILE = "balaji_history.csv"

CAR_MODELS = {"Balaji Go 🚗": 13, "Balaji Sedan 🚙": 17, "Balaji SUV 🚐": 22}

# 2. Database Functions
def save_booking(user_p, data):
    data['phone'] = user_p
    df = pd.DataFrame([data])
    if not os.path.isfile(DB_FILE): df.to_csv(DB_FILE, index=False)
    else: df.to_csv(DB_FILE, mode='a', header=False, index=False)

def get_history(user_p):
    if os.path.isfile(DB_FILE):
        df = pd.read_csv(DB_FILE)
        user_df = df[df['phone'].astype(str) == str(user_p)]
        return user_df.to_dict('records')
    return []

# 3. Dictionary
T = {
    "English": {
        "title": "BALAJI LOGISTICS 📦", "home": "Home", "act": "History", "supp": "Support", "logout": "Logout",
        "from": "📍 Pick-up", "to": "🏁 Drop", "next": "Next ➔", "book": "Confirm", "lang_sel": "Language"
    },
    "Marathi": {
        "title": "बालाजी लॉजिस्टिक्स 📦", "home": "होम", "act": "हिस्ट्री", "supp": "सपोर्ट", "logout": "लॉगआउट",
        "from": "📍 पिक-अप", "to": "🏁 ड्रॉप", "next": "पुढील ➔", "book": "कन्फर्म", "lang_sel": "भाषा"
    }
}

if "lang" not in st.session_state: st.session_state.lang = "English"
if "auth" not in st.session_state: st.session_state.auth = False
if "pg" not in st.session_state: st.session_state.pg = "Home"
if "step" not in st.session_state: st.session_state.step = 1

L = T[st.session_state.lang]

# 4. Advanced CSS for Mobile-like Bottom Nav
st.markdown(f"""
<style>
    .main-header {{background: #000; color:#FFD700; padding:20px; text-align:center; border-radius:0 0 20px 20px; margin-top:-60px;}}
    .stButton>button {{width:100%; border-radius:10px; background-color: #000; color: #fff;}}
    
    /* Fixed Bottom Navigation */
    .nav-wrapper {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: white;
        border-top: 1px solid #e0e0e0;
        padding: 10px 0;
        z-index: 1000;
        display: flex;
        justify-content: space-around;
    }}
</style>
""", unsafe_allow_html=True)

# 5. Auth Logic
if not st.session_state.auth:
    st.session_state.lang = st.selectbox(f"🌐 {L['lang_sel']}", ["English", "Marathi"])
    st.markdown(f'<div class="main-header"><h1>{L["title"]}</h1></div><br>', unsafe_allow_html=True)
    p_login = st.text_input("Mobile Number", max_chars=10)
    if st.button("Login / Start"):
        if len(p_login) == 10:
            st.session_state.u = {"n": "User", "p": p_login}
            st.session_state.auth = True
            st.rerun()
else:
    # 6. Pages
    if st.session_state.pg == "Home":
        st.subheader(f"Welcome! 👋")
        if st.session_state.step == 1:
            m = folium.Map(location=[19.9975, 73.7898], zoom_start=12)
            st_folium(m, height=200, width=700)
            src = st.text_input(L["from"])
            dst = st.text_input(L["to"])
            if st.button(L["next"]):
                if src and dst: st.session_state.route = {"s": src, "d": dst}; st.session_state.step = 2; st.rerun()
        else:
            km = st.number_input("KM", min_value=1.0, value=5.0)
            car = st.radio("Vehicle", list(CAR_MODELS.keys()), horizontal=True)
            fare = km * CAR_MODELS[car]
            st.write(f"### Fare: ₹{fare}")
            if st.button(L["book"]):
                save_booking(st.session_state.u['p'], {"s": st.session_state.route['s'], "d": st.session_state.route['d'], "f": fare, "c": car})
                st.success("Booked!")
                st.session_state.step = 1; st.rerun()

    elif st.session_state.pg == "Activity":
        st.header(L["act"])
        data = get_history(st.session_state.u['p'])
        for h in reversed(data):
            st.info(f"🏁 {h['s']} to {h['d']} \n💰 ₹{h['f']} | {h['c']}")

    elif st.session_state.pg == "Support":
        st.header(L["supp"])
        st.write(f"Contact Support: {MY_NO}")
        st.markdown(f'<a href="https://wa.me/{MY_NO}" style="background:#25D366; color:white; padding:10px; border-radius:10px; text-decoration:none; display:block; text-align:center;">Chat on WhatsApp</a>', unsafe_allow_html=True)

    # 7. THE BOTTOM NAVIGATION (Exactly like your image)
    st.markdown("<br><br><br><br>", unsafe_allow_html=True) # Bottom space
    
    # We use columns inside a fixed container for that horizontal look
    nav_col = st.columns(4)
    
    if nav_col[0].button(f"🏠\n{L['home']}"):
        st.session_state.pg = "Home"; st.rerun()
        
    if nav_col[1].button(f"🕒\n{L['act']}"):
        st.session_state.pg = "Activity"; st.rerun()
        
    if nav_col[2].button(f"📞\n{L['supp']}"):
        st.session_state.pg = "Support"; st.rerun()
        
    if nav_col[3].button(f"🚪\n{L['logout']}"):
        st.session_state.auth = False; st.rerun()