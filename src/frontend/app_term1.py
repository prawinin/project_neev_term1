import requests
import streamlit as st
from components.uploader import render_uploader
from components.results import render_results

API_BASE = "http://127.0.0.1:8000/api/v1"


def main():
    st.set_page_config(page_title="Project Neev - Term 1", page_icon="🏗️", layout="wide")

    st.title("🏗️ Project Neev - Term 1")
    st.caption("Public build: Scan + Compliance + Cost Estimation")

    col1, col2 = st.columns([2, 1])

    with col1:
        uploaded_file = render_uploader()

    with col2:
        st.subheader("Project Inputs")
        city = st.selectbox("City", ["Bangalore", "Delhi", "Pune", "Bokaro"])
        use_manual_dims = st.checkbox("Use manual dimensions")
        manual_width = None
        manual_length = None
        if use_manual_dims:
            manual_width = st.number_input("Width (ft)", min_value=10.0, max_value=500.0, value=40.0)
            manual_length = st.number_input("Length (ft)", min_value=10.0, max_value=500.0, value=30.0)

        manual_fsi = st.number_input("Manual FSI (optional)", min_value=0.5, max_value=5.0, value=1.5)
        manual_floors = st.number_input("Manual Floors (optional)", min_value=1, max_value=10, value=2)

    if uploaded_file and st.button("Analyze Plot", type="primary"):
        with st.spinner("Analyzing..."):
            try:
                files = {
                    "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
                }
                data = {
                    "city": city,
                    "manual_fsi": str(manual_fsi),
                    "manual_floors": str(manual_floors),
                }

                if use_manual_dims and manual_width and manual_length:
                    data["manual_width"] = str(manual_width)
                    data["manual_length"] = str(manual_length)

                response = requests.post(f"{API_BASE}/analyze", files=files, data=data, timeout=120)
                if response.status_code == 200:
                    st.success("Analysis complete")
                    render_results(response.json())
                else:
                    st.error(f"API error: {response.status_code} - {response.text}")
            except Exception as exc:
                st.error(f"Request failed: {exc}")


if __name__ == "__main__":
    main()
