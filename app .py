import streamlit as st

# १. अ‍ॅपची प्राथमिक मांडणी (Setup)
st.set_page_config(page_title="Balaji Logistics", page_icon="🚖", layout="centered")

# २. ब्रँडिंग आणि नाव
st.sidebar.image("https://img.icons8.com/color/144/000000/suv.png", width=100)
st.sidebar.title("Balaji Travels")
st.sidebar.info("📞 बुकिंग: 9767981986\n\n💬 सपोर्ट: 8605520369")

st.title("🚩 Balaji Logistics and Tours and Travels")
st.markdown("### **All India Outstation Car Booking**")
st.info("🚗 आमची सेवा: T-Permit | 6+7 Seater | दर: ₹13/किमी + टोल आणि पार्किंग")

# ३. नेव्हिगेशन मेनू
menu = ["Home", "Book A Ride", "Price Estimator", "My Account", "Help & Support", "Admin Panel"]
choice = st.sidebar.selectbox("मेनू निवडा", menu)

# ४. होम स्क्रीन
if choice == "Home":
    st.write("#### आमच्या सुविधा:")
    col1, col2 = st.columns(2)
    with col1:
        st.write("✅ **२४/७ उपलब्ध**")
        st.write("✅ **ऑल इंडिया परमिट**")
    with col2:
        st.write("✅ **अनुभवी ड्रायव्हर**")
        st.write("✅ **स्वच्छ गाड्या (6+7 Seater)**")
    
    st.markdown("---")
    st.write("### बुकिंगसाठी दोन सोपे पर्याय:")
    c1, c2 = st.columns(2)
    with c1:
        st.button("🚕 Outstation (One Way)")
    with c2:
        st.button("🔄 Outstation (Round Trip)")

# ५. Price Estimator (नवीन फीचर)
elif choice == "Price Estimator":
    st.header("📊 भाड्याचा अंदाज")
    kms = st.number_input("अंदाजित किलोमीटर (येणे-जाणे मिळून)", min_value=1, value=100)
    total_price = kms * 13
    st.metric(label="अंदाजित भाडे", value=f"₹{total_price}")
    st.caption("*टोल, पार्किंग आणि बॉर्डर टॅक्स अतिरिक्त असेल.")

# ६. बुकिंग विभाग (WhatsApp Integration सह)
elif choice == "Book A Ride":
    st.header("📝 तुमची राईड बुक करा")
    with st.form("booking_form"):
        name = st.text_input("पूर्ण नाव")
        mobile = st.text_input("मोबाईल नंबर")
        aadhar = st.text_input("आधार कार्ड नंबर")
        pickup = st.text_input("कुठून (Pickup Point)")
        drop = st.text_input("कुठे (Destination)")
        date = st.date_input("प्रवासाची तारीख")
        
        submit = st.form_submit_button("Book Ride Now")
        
        if submit:
            if name and mobile and pickup:
                msg = f"नवीन बुकिंग! \nनाव: {name} \nमोबाईल: {mobile} \nआधार: {aadhar} \nPickup: {pickup} \nDrop: {drop} \nतारीख: {date}"
                whatsapp_url = f"https://wa.me/919767981986?text={msg.replace(' ', '%20')}"
                st.success(f"धन्यवाद {name}! तुमची माहिती सबमिट झाली आहे.")
                st.markdown(f"**[✅ बुकिंग पूर्ण करण्यासाठी येथे क्लिक करा (WhatsApp)]({whatsapp_url})**")
                st.balloons()
            else:
                st.error("कृपया सर्व माहिती भरा!")

# ७. हेल्प आणि सपोर्ट
elif choice == "Help & Support":
    st.header("📞 हेल्प आणि सपोर्ट")
    st.success("संपर्क क्रमांक: 8605520369 / 9767981986")
    st.write("काही अडचण असल्यास किंवा चौकशीसाठी वरील नंबरवर संपर्क साधा.")

# ८. अ‍ॅडमिन पॅनेल
elif choice == "Admin Panel":
    st.header("🔒 अ‍ॅडमिन लॉगिन")
    user_pass = st.text_input("पासवर्ड टाका", type="password")
    if user_pass == "balaji123":
        st.success("लॉगिन यशस्वी!")
        st.write("बुकिंगचा डेटा लवकरच येथे दिसेल.")
    elif user_pass:
        st.error("पासवर्ड चुकीचा आहे!")

# ९. माय अकाउंट
elif choice == "My Account":
    st.header("👤 ग्राहकाची माहिती")
    st.write("येथे तुमची प्रोफाईल आणि बुकिंग हिस्ट्री दिसेल (लवकरच).")
  
