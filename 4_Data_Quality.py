import streamlit as st

st.title("Data Quality")
st.caption("Basic checks on the currently loaded Excel workbook.")

if "ort_data" not in st.session_state:
    st.info("Load a workbook from the main page first.")
    st.stop()

data = st.session_state["ort_data"]
for sheet, frame in data.items():
    with st.expander(f"{sheet} — {len(frame):,} rows", expanded=True):
        st.write("Duplicate rows:", int(frame.duplicated().sum()))
        st.write("Missing values by column:")
        st.dataframe(
            frame.isna().sum().rename("Missing values"),
            use_container_width=True
        )
