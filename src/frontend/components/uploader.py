from PIL import Image
import streamlit as st


def render_uploader():
    st.markdown(
        """
        <div style='text-align: center; padding: 20px; border: 2px dashed #444; border-radius: 10px;'>
            <h4>📸 Upload Site Photo</h4>
            <p style='font-size: 12px; color: #888'>Supported: JPG, PNG</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Preview", use_container_width=True)
        return uploaded_file

    return None
