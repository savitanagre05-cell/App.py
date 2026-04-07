
    """, unsafe_allow_html=True)
    if st.button("पिकअप झाला ➔"): st.session_state.ride_stage = "InTrip"; st.rerun()

# --- स्टेज ३: प्रवासात आणि पूर्ण ---
elif st.session_state.ride_stage == "Arrived":
    st.success("🏁 ड्रायव्हर पोहोचला आहे!")
    if st.button("प्रवास सुरू करा"): st.session_state.ride_stage = "InTrip"; st.rerun()

elif st.session_state.ride_stage == "InTrip":
    st.info(f"🚕 तुम्ही {st.session_state.drop_loc} कडे जात आहात.")
    if st.button("प्रवास पूर्ण करा 🏁"): st.session_state.ride_stage = "Finished"; st.rerun()

elif st.session_state.ride_stage == "Finished":
    st.balloons()
    st.markdown(f"<div style='text-align:center; padding:30px; border:2px solid #000; border-radius:15px;'><h2>बिल: ₹{st.session_state.total_fare}</h2><p>धन्यवाद, {st.session_state.user_name}!</p></div>", unsafe_allow_html=True)
    if st.button("Home 🏠"): 
        st.session_state.ride_stage = "Home"
        st.session_state.car_pos_offset = 0.006
        st.rerun()
