import streamlit as st
import plotly.express as px
import pandas as pd

st.title("Beneficiary Analytics")
st.caption("Explore learner, teacher and geographical reach.")

if "ort_data" not in st.session_state:
    st.info("Load a workbook from the main page first.")
    st.stop()

data = st.session_state["ort_data"]
beneficiaries = data["Beneficiaries"].copy()
projects = data["Projects"][["Project_ID", "Project_Name", "Province"]]
frame = beneficiaries.merge(projects, on="Project_ID", how="left")

if frame.empty:
    st.info("No beneficiary records found.")
    st.stop()

c1, c2, c3 = st.columns(3)
c1.metric("Learners", f'{pd.to_numeric(frame["Number_of_Learners"], errors="coerce").fillna(0).sum():,.0f}')
c2.metric("Teachers", f'{pd.to_numeric(frame["Number_of_Teachers"], errors="coerce").fillna(0).sum():,.0f}')
c3.metric("Schools", f'{frame["School_ID"].nunique():,}')

by_province = frame.groupby("Province", dropna=False)["Number_of_Learners"].sum().reset_index()
fig = px.bar(by_province, x="Province", y="Number_of_Learners", title="Learners reached by province")
st.plotly_chart(fig, use_container_width=True)
st.dataframe(frame, use_container_width=True, hide_index=True)
