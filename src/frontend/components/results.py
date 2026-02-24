import base64
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def render_results(data):
    vision = data["vision"]
    legal = data["legal"]
    finance = data["finance"]

    with st.expander("👁️ Developer Mode: Computer Vision Internals"):
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.info("Detection Metrics")
            st.write(f"Detected: {vision['width_ft']}ft x {vision['length_ft']}ft")
            st.write(f"Confidence: {int(vision.get('confidence', 0) * 100)}%")
        with col_d2:
            st.info("Edge Detection Layer")
            if "debug_xray" in vision:
                try:
                    img_bytes = base64.b64decode(vision["debug_xray"])
                    st.image(img_bytes, caption="Canny Edge Output", use_container_width=True)
                except Exception:
                    st.warning("Could not decode debug image.")

    st.subheader("📐 Site Analysis")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Plot Area", f"{vision['area_sqft']} sq.ft")
    c2.metric("Dimensions", f"{vision['width_ft']} x {vision['length_ft']} ft")
    c3.metric("Buildable Area", f"{legal['max_buildable_area']} sq.ft")

    status_color = "green" if legal["is_buildable"] else "red"
    status_text = "PASSED" if legal["is_buildable"] else "FAILED"
    c4.markdown(
        f"**Status**<br><span style='color:{status_color}; font-size:24px; font-weight:bold'>{status_text}</span>",
        unsafe_allow_html=True,
    )

    if "compliance_breakdown" in legal:
        st.caption("📝 Compliance Logic:")
        for rule in legal["compliance_breakdown"]:
            st.markdown(f"- {rule}")

    st.divider()
    st.subheader("💰 Financial Estimation")
    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.info("Approximate Total Cost")
        st.markdown(
            f"<h1 style='color:#00C851'>₹ {finance['total_cost'] / 100000:.2f} Lakhs</h1>",
            unsafe_allow_html=True,
        )
        floors = finance.get("floors_calculated", 2)
        st.markdown(f"**Based on Construction of {floors} Floors (G+{floors - 1})**")

    with col_right:
        labels = ["Material", "Labor"]
        values = [finance["material_cost"], finance["labor_cost"]]
        fig = go.Figure(
            data=[go.Pie(labels=labels, values=values, hole=0.5, marker_colors=["#33b5e5", "#ffbb33"])]
        )
        fig.update_layout(height=250, margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("🏗️ Bill of Materials (BOM)")
    bom_data = finance["bill_of_materials"]
    df = pd.DataFrame(list(bom_data.items()), columns=["Material", "Estimated Quantity"])
    st.dataframe(df, use_container_width=True, hide_index=True)

    report_content = f"""
PROJECT NEEV - TERM 1 FEASIBILITY REPORT
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
-------------------------------------------
CITY: {legal.get('city', 'Unknown')}
PLOT AREA: {vision['area_sqft']} sq.ft
DIMENSIONS: {vision['width_ft']}ft x {vision['length_ft']}ft
-------------------------------------------
LEGAL STATUS: {'PASSED' if legal['is_buildable'] else 'FAILED'}
MAX BUILDABLE AREA: {legal['max_buildable_area']} sq.ft
-------------------------------------------
ESTIMATED COST: Rs. {finance['total_cost']:,.2f}
CALCULATED FOR: {finance.get('floors_calculated', 2)} Floors

MATERIAL BREAKDOWN:
"""
    for item, qty in bom_data.items():
        report_content += f"- {item}: {qty}\n"

    st.download_button(
        label="📄 Download Term 1 Report",
        data=report_content,
        file_name="neev_term1_report.txt",
        mime="text/plain",
    )
