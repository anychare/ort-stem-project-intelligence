import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Financial Analytics")
st.caption("Review allocated budgets and reported expenditure.")

if "ort_data" not in st.session_state:
    st.info("Load a workbook from the main page first.")
    st.stop()

data = st.session_state["ort_data"]
finance = data["Finance"].copy()
projects = data["Projects"][["Project_ID", "Project_Name"]]
frame = finance.merge(projects, on="Project_ID", how="left")

if frame.empty:
    st.info("No financial records found.")
    st.stop()

for col in ["Allocated_Budget", "Actual_Expenditure"]:
    frame[col] = pd.to_numeric(frame[col], errors="coerce").fillna(0)

frame["Variance"] = frame["Allocated_Budget"] - frame["Actual_Expenditure"]
frame["Expenditure_Pct"] = (
    frame["Actual_Expenditure"] / frame["Allocated_Budget"].replace(0, pd.NA) * 100
)

a, b, c = st.columns(3)
a.metric("Allocated budget", f'R {frame["Allocated_Budget"].sum():,.0f}')
b.metric("Expenditure", f'R {frame["Actual_Expenditure"].sum():,.0f}')
c.metric("Balance", f'R {frame["Variance"].sum():,.0f}')

fig = px.bar(
    frame, x="Project_Name",
    y=["Allocated_Budget", "Actual_Expenditure"],
    barmode="group", title="Budget versus expenditure (ZAR)"
)
st.plotly_chart(fig, use_container_width=True)
st.dataframe(frame, use_container_width=True, hide_index=True)
