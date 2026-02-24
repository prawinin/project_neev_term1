from PIL import Image
import streamlit as st


def render_uploader():
    st.subheader("Upload Site Photo")
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Preview", use_container_width=True)
        return uploaded_file

    return None
