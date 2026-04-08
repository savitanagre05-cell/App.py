import streamlit as st
import random, urllib.parse, folium
from streamlit_folium import st_folium

# 1. Setup & State
st.set_page_config(page_title="Balaji Logistics", layout="centered")
MY_NO = "9767981986"
R_GO, R_SUV = 13, 20

for k, v in {"auth":False, "pg":"Home", "hist":[], "dst":5.0, "rd":{}}.items():
    if k not in st.session_state: st.session_state[k] = v

# 2. CSS Style
st.markdown("<style>.main-header{background:#000;color:#fff;padding:15px;text-align:center;border-radius:0 0 15px 15px;margin-top:-65px;}.card{border:1px solid #eee;padding:12px;border-radius:10px;margin-bottom:10px;}.btn-wa{display:block;background:#25D366;color:#fff !important;text-align:center;padding:10px;border-radius:8px;text-decoration:none;font-weight:bold;}</style>", unsafe_allow_html=True)

# 3. Registration
if not st.session_state.auth:
    st.markdown('<div class="main-header"><h1>BALAJI</h1></div>', unsafe_allow_html=True)
    n, p = st.text_input("नाव"), st.text_input("नंबर", max_chars=10)
    if st.button("सुरू करा"):
        if n and len(p)==10: st.session_state.auth=True; st.session_state.u={"n":n,"p":p}; st.rerun()

# 4. App Logic
else:
    if st.session_state.pg == "Home":
        st.write(f"नमस्कार, {st.session_state.u['n']}!")
        m = folium.Map(location=[19.99, 73.78], zoom_start=12)
        folium.Marker([19.99, 73.78]).add_to(m)
        st_folium(m, height=200, width=700, key="m")
        dr = st.text_input("🏁 डेस्टिनेशन")
        km = random.randint(5, 15)
        st.write(f"अंदाजे अंतर: {km} किमी")
        c1, c2 = st.columns(2)
        if c1.button(f"Go (₹{km*R_GO})") and dr:
            st.session_state.rd={"d":dr,"km":km,"f":km*R_GO,"v":"Go"}; st.session_state.pg="Process"; st.rerun()
        if c2.button(f"SUV (₹{km*R_SUV})") and dr:
            st.session_state.rd={"d":dr,"km":km,"f":km*R_SUV,"v":"SUV"}; st.session_state.pg="Process"; st.rerun()

    elif st.session_state.pg == "Process":
        r = st.session_state.rd
        msg = urllib.parse.quote(f"🚕 नवीन बुकिंग!\nनाव: {st.session_state.u['n']}\nड्रॉप: {r['d']}\nभाडे: ₹{r['f']}")
        st.markdown(f'<a href="https://wa.me/91{MY_NO}?text={msg}" target="_blank" class="btn-wa">WhatsApp पाठवा</a>', unsafe_allow_html=True)
        st.info(f"🚕 ड्रायव्हर {st.session_state.dst:.1f} किमी लांब आहे")
        if st.session_state.dst > 0.5:
            if st.button("अपडेट 🔄"): st.session_state.dst -= 1.2; st.rerun()
        else:
            if st.button("पूर्ण 🏁"): st.session_state.hist.append(r); st.session_state.pg="Home"; st.session_state.dst=5.0; st.balloons(); st.rerun()

    elif st.session_state.pg == "Activity":
        st.header("🕒 हिस्ट्री")
        for r in reversed(st.session_state.hist): st.write(f"✅ {r['d']} - ₹{r['f']}")

    elif st.session_state.pg == "Account":
        st.write(f"👤 {st.session_state.u['n']}"); st.button("Logout", on_click=lambda: st.session_state.update({"auth":False}))

    # Bottom Navigation
    st.markdown("---")
    nb1, nb2, nb3 = st.columns(3)
    if nb1.button("🏠 Home"): st.session_state.pg="Home"; st.rerun()
    if nb2.button("🕒 Activity"): st.session_state.pg="Activity"; st.rerun()
    if nb3.button("👤 Account"): st.session_state.pg="Account"; st.rerun()
