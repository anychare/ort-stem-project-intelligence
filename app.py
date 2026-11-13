import pandas as pd
import streamlit as st

#Rendering the ORT SA logo at the top left
st.logo("path/to/your/logo.png")

st.set_page_config(
    page_title="ORT STEM Project Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
.main {background-color: #F7F9FC;}
[data-testid="stSidebar"] {background-color: #123B68;}
[data-testid="stSidebar"] * {color: white !important;}
div[data-testid="stMetric"] {
    background: white; padding: 16px; border-radius: 10px;
    border: 1px solid #E5EAF1;
}
</style>
""",
    unsafe_allow_html=True,
)

st.title("ORT South Africa")
st.subheader("STEM Project Intelligence Platform")
st.caption("Project Monitoring • Data Analytics • Reporting")

with st.sidebar:
  st.markdown("## ORT-STEM Project Intelligence")
  st.caption("STEM Department Analytics")
  st.markdown("---")
  st.markdown("### Data source")
  uploaded = st.file_uploader(
      "Upload any Excel or CSV file",
      type=["xlsx", "xls", "xlsm", "xlsb", "ods", "csv"],
      help="Supports all standard Excel workbooks and CSV files.",
  )
  st.markdown("---")
  st.caption("IE Version 1.0 | Internal Evaluation")

# Load any uploaded Excel or CSV file into a dictionary of DataFrames
if uploaded is not None:
  try:
    if uploaded.name.lower().endswith(".csv"):
      data = {"Data": pd.read_csv(uploaded)}
    else:
      # sheet_name=None automatically loads every sheet in any Excel workbook
      data = pd.read_excel(uploaded, sheet_name=None)

    st.session_state["workbook_data"] = data
    st.session_state["file_name"] = uploaded.name
    st.success(f"Loaded '{uploaded.name}' successfully.")
  except Exception as exc:
    st.error(f"Unable to read file: {exc}")
    st.stop()

if "workbook_data" in st.session_state:
  data = st.session_state["workbook_data"]
  sheet_names = list(data.keys())
  current_file = st.session_state.get("file_name", "Uploaded File")

  st.markdown(f"### Executive Summary — {current_file}")

  # Dynamic sheet selector (automatically adapts to any workbook)
  if len(sheet_names) > 1:
    selected_sheet = st.selectbox("Select Worksheet to Analyse", sheet_names)
  else:
    selected_sheet = sheet_names[0]

  df = data[selected_sheet].copy()

  if df.empty:
    st.warning("The selected sheet contains no records.")
    st.stop()

  # Identify numeric and text/categorical columns dynamically
  numeric_cols = df.select_dtypes(include="number").columns.tolist()
  categorical_cols = df.select_dtypes(
      include=["object", "category", "string"]
  ).columns.tolist()

  # Dynamic KPIs based on whatever file is uploaded
  c1, c2, c3, c4 = st.columns(4)
  c1.metric("Total Sheets", f"{len(sheet_names):,}")
  c2.metric("Total Records", f"{len(df):,}")
  c3.metric("Total Columns", f"{len(df.columns):,}")

  if numeric_cols:
    primary_num = numeric_cols[0]
    c4.metric(f"Total {primary_num}", f"{df[primary_num].sum():,.2f}")
  else:
    missing_cells = int(df.isna().sum().sum())
    c4.metric("Missing Cells", f"{missing_cells:,}")

  st.markdown("---")
  left, right = st.columns(2)

  # Left Chart: Dynamic Category Breakdown
  with left:
    st.markdown("#### Category breakdown")
    if categorical_cols:
      cat_col = st.selectbox(
          "Group by category", categorical_cols, key="cat_select"
      )
      counts = df[cat_col].fillna("Not specified").value_counts().head(15)
      st.bar_chart(counts)
    else:
      st.info("No text or category columns found in this sheet.")

  # Right Chart: Dynamic Numeric Aggregation
  with right:
    st.markdown("#### Numeric analysis")
    if numeric_cols and categorical_cols:
      group_col = st.selectbox(
          "Group column", categorical_cols, key="group_select"
      )
      val_col = st.selectbox("Value column", numeric_cols, key="val_select")
      grouped_data = (
          df.groupby(group_col)[val_col]
          .sum()
          .sort_values(ascending=False)
          .head(15)
      )
      st.bar_chart(grouped_data)
    elif numeric_cols:
      val_col = st.selectbox(
          "Select metric to plot", numeric_cols, key="val_only_select"
      )
      st.bar_chart(df[val_col].head(50))
    else:
      st.info("No numeric columns available to plot.")

  st.markdown("---")
  st.markdown("#### Data register")
  st.dataframe(df, use_container_width=True, hide_index=True)

  if numeric_cols:
    st.markdown("#### Summary statistics")
    st.dataframe(df[numeric_cols].describe().T, use_container_width=True)

  st.markdown("#### Data quality notes")
  st.caption(
      "Figures are calculated dynamically from the file uploaded for this"
      " session. Confirm reporting periods, unique identifiers and definitions"
      " before using these figures for formal management reporting."
  )
else:
  st.info("Upload any Excel or CSV file in the sidebar to begin.")
  st.markdown("### Getting started")
  st.write(
      "Upload any spreadsheet using the panel on the left. "
      "The platform will automatically detect all sheets, columns, summary "
      "metrics, and charts for your dataset."
  )
