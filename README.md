# ORT STEM Project Intelligence Platform (ORT-SPI)

A Streamlit prototype for consolidating and analysing STEM project information using Excel workbooks.

## Included modules
- Executive overview
- Project performance
- Beneficiary analytics
- Financial analytics
- Basic data-quality checks
- Downloadable Excel template

## Requirements
- Python 3.10 or newer recommended
- pip

## Run locally

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install dependencies and run:
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Excel workbook structure

The workbook must contain these worksheets:
1. `Projects`
2. `Beneficiaries`
3. `Performance`
4. `Finance`

Use the exact column names in the downloadable template. `Project_ID` links records across sheets.

## Important prototype limitations
- Uploaded workbook data is held in the Streamlit session; it is not a permanent central repository.
- There is no production authentication, role-based authorisation, audit logging or database integration.
- The sample records are illustrative and are not ORT South Africa data.
- KPI definitions must be approved by the STEM department before formal reporting.
- Financial figures are assumed to be in South African rand (ZAR).
- Validate data periods and avoid summing repeated cumulative reporting figures.

## Recommended next steps
1. Confirm the STEM data dictionary and KPI definitions.
2. Map existing ORT Excel reporting templates to the standard workbook.
3. Agree user roles and access permissions.
4. Obtain information governance and hosting approval.
5. Add a persistent database and authenticated access before production use.
