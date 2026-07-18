import streamlit as st
import segno
import io
@st.dialog(title="Share Subject Code")
def share_sub_dialogue(subject_code, subject_name):
    app_domain = "http://localhost:8501"  # Replace with your actual app domain
    join_url = f"{app_domain}?join-code={subject_code}"
    
    st.write(f"Scan to join")
    
    qr = segno.make(join_url)
    out = io.BytesIO()
    qr.save(out, kind='png', scale=10)
    
    col1, col2= st.columns(2, gap="small")
    with col1:
        st.markdown(f"**Copy Link** {subject_code}")
        st.code(join_url, language="text")
        st.code(f"Subject Code : {subject_code}", language="text")
        st.info("Share this link or code with your students via whatsapp or email", icon="ℹ️")
    with col2:
        st.markdown(f"**Scan QR Code**")
        st.image(out.getvalue(), caption="Scan to join", use_container_width=True)
