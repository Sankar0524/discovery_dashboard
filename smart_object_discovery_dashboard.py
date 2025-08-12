import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Smart Object Discovery Dashboard", layout="wide")

st.title("🔍 Smart Object Discovery Dashboard for Snowflake")
st.markdown("**Contributors:** B A, Amreeza, Chappa, Sankara Rao")

# Simulated metadata for demonstration
data = [
    {"Database": "SALES_DB", "Schema": "PUBLIC", "Object_Type": "TABLE", "Object_Name": "CUSTOMERS", "Usage_Status": "Used"},
    {"Database": "SALES_DB", "Schema": "PUBLIC", "Object_Type": "TABLE", "Object_Name": "ORDERS", "Usage_Status": "Used"},
    {"Database": "SALES_DB", "Schema": "ARCHIVE", "Object_Type": "TABLE", "Object_Name": "OLD_ORDERS", "Usage_Status": "Unused"},
    {"Database": "HR_DB", "Schema": "PUBLIC", "Object_Type": "VIEW", "Object_Name": "EMPLOYEE_VIEW", "Usage_Status": "Used"},
    {"Database": "HR_DB", "Schema": "PUBLIC", "Object_Type": "STAGE", "Object_Name": "EMP_STAGE", "Usage_Status": "Orphaned"},
    {"Database": "HR_DB", "Schema": "PUBLIC", "Object_Type": "PROCEDURE", "Object_Name": "UPDATE_SALARIES", "Usage_Status": "Used"},
    {"Database": "FINANCE_DB", "Schema": "PUBLIC", "Object_Type": "TABLE", "Object_Name": "TRANSACTIONS", "Usage_Status": "Used"},
    {"Database": "FINANCE_DB", "Schema": "PUBLIC", "Object_Type": "VIEW", "Object_Name": "SUMMARY_VIEW", "Usage_Status": "Unused"},
    {"Database": "FINANCE_DB", "Schema": "PUBLIC", "Object_Type": "STAGE", "Object_Name": "TRANS_STAGE", "Usage_Status": "Orphaned"},
]

df = pd.DataFrame(data)

# Filters
st.sidebar.header("Filters")
object_types = st.sidebar.multiselect("Select Object Types", df["Object_Type"].unique(), default=list(df["Object_Type"].unique()))
usage_statuses = st.sidebar.multiselect("Select Usage Status", df["Usage_Status"].unique(), default=list(df["Usage_Status"].unique()))

filtered_df = df[df["Object_Type"].isin(object_types) & df["Usage_Status"].isin(usage_statuses)]

# Display filtered data
st.subheader("Filtered Metadata")
st.dataframe(filtered_df)

# Sunburst chart
fig = px.sunburst(
    filtered_df,
    path=["Database", "Schema", "Object_Type", "Object_Name"],
    color="Usage_Status",
    color_discrete_map={"Used": "green", "Unused": "orange", "Orphaned": "red"},
    title="Smart Object Discovery Sunburst Chart"
)
st.plotly_chart(fig, use_container_width=True)

# Export options
st.subheader("Export Metadata")
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "snowflake_metadata.csv", "text/csv")

excel_file = "snowflake_metadata.xlsx"
filtered_df.to_excel(excel_file, index=False)
with open(excel_file, "rb") as f:
    st.download_button("Download Excel", f.read(), excel_file, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")