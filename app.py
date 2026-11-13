import streamlit as st
from utils.data import load_workbook, demo_workbook_bytes, validate_workbook
from utils.analytics import calculate_kpis

st.set_page_config(
    page_title="ORT STEM Project Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.main {background-color: #F7F9FC;}
[data-testid="stSidebar"] {background-color: #123B68;}
[data-testid="stSidebar"] * {color: white !important;}
div[data-testid="stMetric"] {
    background: white; padding: 16px; border-radius: 10px;
    border: 1px solid #E5EAF1;
}
</style>
""", unsafe_allow_html=True)

st.title("ORT South Africa")
st.subheader("STEM Project Intelligence Platform")
st.caption("Project monitoring • Data analytics • Management reporting")

with st.sidebar:
    st.markdown("## ORT-SPI")
    st.caption("STEM Department Analytics")
    st.markdown("---")
    st.markdown("### Data source")
    uploaded = st.file_uploader(
        "Upload the standard Excel workbook",
        type=["xlsx"],
        help="Expected sheets: Projects, Beneficiaries, Performance and Finance."
    )
    st.download_button(
        "Download Excel template",
        data=demo_workbook_bytes(),
        file_name="ORT_STEM_Data_Template.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )
    st.markdown("---")
    st.caption("Prototype version 0.1 | Internal evaluation")

if uploaded:
    try:
        data = load_workbook(uploaded)
        errors, warnings = validate_workbook(data)
        for warning in warnings:
            st.warning(warning)
        if errors:
            for error in errors:
                st.error(error)
            st.stop()
        st.session_state["ort_data"] = data
        st.success("Workbook loaded and validated for this session.")
    except Exception as exc:
        st.error(f"Unable to read workbook: {exc}")
        st.stop()
elif "ort_data" not in st.session_state:
    st.info("Upload an Excel workbook in the sidebar, or use the sample dataset below.")
    if st.button("Load illustrative sample data", type="primary"):
        st.session_state["ort_data"] = load_workbook(demo_workbook_bytes())
        st.rerun()

if "ort_data" in st.session_state:
    data = st.session_state["ort_data"]
    projects = data["Projects"].copy()
    perf = data["Performance"].copy()
    beneficiaries = data["Beneficiaries"].copy()
    finance = data["Finance"].copy()

    st.markdown("### Executive overview")
    if projects.empty:
        st.warning("The workbook contains no project records.")
        st.stop()

    kpis = calculate_kpis(data)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Projects", f'{kpis["projects"]:,}')
    c2.metric("Active projects", f'{kpis["active_projects"]:,}')
    c3.metric("Learners reached", f'{kpis["learners"]:,}')
    c4.metric("Target achievement", f'{kpis["achievement"]:.1f}%')

    st.markdown("---")
    left, right = st.columns(2)
    with left:
        st.markdown("#### Project status")
        status = projects["Project_Status"].fillna("Not specified").value_counts()
        st.bar_chart(status)
    with right:
        st.markdown("#### Learners reached by project")
        if not beneficiaries.empty:
            learner_by_project = beneficiaries.groupby("Project_ID")["Number_of_Learners"].sum()
            names = projects.set_index("Project_ID")["Project_Name"]
            learner_by_project.index = learner_by_project.index.map(
                lambda x: names.get(x, x)
            )
            st.bar_chart(learner_by_project)
        else:
            st.info("No beneficiary records available.")

    st.markdown("---")
    st.markdown("#### Project register")
    st.dataframe(projects, use_container_width=True, hide_index=True)

    st.markdown("#### Data quality notes")
    st.caption(
        "Figures are calculated from the workbook uploaded for this session. "
        "Confirm reporting periods, unique identifiers and definitions before "
        "using these figures for formal management reporting."
    )
else:
    st.markdown("### Getting started")
    st.write(
        "Use the Excel template to organise project information. "
        "The template contains illustrative records that should be replaced "
        "with approved ORT project data."
    )
