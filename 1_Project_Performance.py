import streamlit as st
import plotly.express as px
from utils.analytics import performance_summary

st.title("Project Performance")
st.caption("Compare learner targets and activity delivery.")

if "ort_data" not in st.session_state:
    st.info("Load a workbook from the main page first.")
    st.stop()

data = st.session_state["ort_data"]
performance = performance_summary(data["Performance"])
projects = data["Projects"][["Project_ID", "Project_Name"]]
frame = performance.merge(projects, on="Project_ID", how="left")

if frame.empty:
    st.info("No performance records found.")
    st.stop()

fig = px.bar(
    frame, x="Project_Name",
    y=["Target_Learners", "Actual_Learners"],
    barmode="group",
    title="Learner targets versus actual reach"
)
st.plotly_chart(fig, use_container_width=True)
st.dataframe(frame, use_container_width=True, hide_index=True)
