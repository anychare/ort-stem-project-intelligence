from io import BytesIO
import pandas as pd

SHEETS = {
    "Projects": [
        "Project_ID", "Project_Name", "Project_Type", "Province",
        "Start_Date", "End_Date", "Project_Manager", "Budget",
        "Project_Status"
    ],
    "Beneficiaries": [
        "Project_ID", "Reporting_Period", "School_ID", "District",
        "Number_of_Learners", "Male_Learners", "Female_Learners",
        "Number_of_Teachers"
    ],
    "Performance": [
        "Project_ID", "Reporting_Period", "Target_Learners",
        "Actual_Learners", "Planned_Activities", "Completed_Activities"
    ],
    "Finance": [
        "Project_ID", "Reporting_Period", "Allocated_Budget",
        "Actual_Expenditure"
    ]
}

def sample_data():
    projects = pd.DataFrame([
        ["STEM001", "Robotics Programme", "Robotics", "Gauteng", "2026-01-15", "2026-12-15", "Facilitator A", 250000, "Active"],
        ["STEM002", "Coding Clubs", "Coding", "Limpopo", "2026-02-01", "2026-11-30", "Facilitator B", 180000, "Active"],
        ["STEM003", "Science Outreach", "Science", "North West", "2026-03-01", "2026-10-31", "Facilitator C", 120000, "Completed"],
        ["STEM004", "Teacher Development", "Teacher Training", "Gauteng", "2026-04-01", "2026-12-01", "Facilitator D", 200000, "Active"],
    ], columns=SHEETS["Projects"])

    beneficiaries = pd.DataFrame([
        ["STEM001", "2026-Q3", "SCH001", "Johannesburg", 120, 65, 55, 5],
        ["STEM002", "2026-Q3", "SCH002", "Polokwane", 90, 42, 48, 4],
        ["STEM003", "2026-Q3", "SCH003", "Rustenburg", 75, 36, 39, 3],
        ["STEM004", "2026-Q3", "SCH004", "Johannesburg", 60, 20, 40, 12],
    ], columns=SHEETS["Beneficiaries"])

    performance = pd.DataFrame([
        ["STEM001", "2026-Q3", 150, 120, 10, 8],
        ["STEM002", "2026-Q3", 100, 90, 12, 10],
        ["STEM003", "2026-Q3", 80, 75, 8, 8],
        ["STEM004", "2026-Q3", 80, 60, 6, 5],
    ], columns=SHEETS["Performance"])

    finance = pd.DataFrame([
        ["STEM001", "2026-Q3", 250000, 175000],
        ["STEM002", "2026-Q3", 180000, 92000],
        ["STEM003", "2026-Q3", 120000, 110000],
        ["STEM004", "2026-Q3", 200000, 85000],
    ], columns=SHEETS["Finance"])

    return {
        "Projects": projects,
        "Beneficiaries": beneficiaries,
        "Performance": performance,
        "Finance": finance
    }

def demo_workbook_bytes():
    data = sample_data()
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for sheet, frame in data.items():
            frame.to_excel(writer, sheet_name=sheet, index=False)
    output.seek(0)
    return output.getvalue()

def load_workbook(file):
    if isinstance(file, bytes):
        file = BytesIO(file)
    return {
        sheet: pd.read_excel(file, sheet_name=sheet)
        for sheet in SHEETS
    }

def validate_workbook(data):
    errors, warnings = [], []
    for sheet, required in SHEETS.items():
        if sheet not in data:
            errors.append(f"Missing worksheet: {sheet}")
            continue
        missing = [c for c in required if c not in data[sheet].columns]
        if missing:
            errors.append(f"{sheet}: missing columns {', '.join(missing)}")

    if errors:
        return errors, warnings

    projects = data["Projects"]
    if projects["Project_ID"].isna().any():
        errors.append("Projects: Project_ID contains blank values.")
    if projects["Project_ID"].duplicated().any():
        errors.append("Projects: Project_ID must be unique in the project register.")

    valid_ids = set(projects["Project_ID"].dropna().astype(str))
    for sheet in ["Beneficiaries", "Performance", "Finance"]:
        ids = set(data[sheet]["Project_ID"].dropna().astype(str))
        unknown = ids - valid_ids
        if unknown:
            warnings.append(
                f"{sheet}: {len(unknown)} Project_ID value(s) do not match the project register."
            )

    for sheet, cols in {
        "Beneficiaries": ["Number_of_Learners", "Male_Learners", "Female_Learners", "Number_of_Teachers"],
        "Performance": ["Target_Learners", "Actual_Learners", "Planned_Activities", "Completed_Activities"],
        "Finance": ["Allocated_Budget", "Actual_Expenditure"],
        "Projects": ["Budget"]
    }.items():
        for col in cols:
            if (pd.to_numeric(data[sheet][col], errors="coerce").dropna() < 0).any():
                warnings.append(f"{sheet}.{col} contains negative values. Please verify.")

    return errors, warnings
