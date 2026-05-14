import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="HR Analytics Dashboard",
    layout="wide"
)

# ---------------- LOAD DATA ---------------- #

df = pd.read_csv("employee_data.csv")

# ---------------- TITLE ---------------- #

st.title("HR Analytics Dashboard")

st.markdown("Employee Attrition & Workforce Insights")

# ---------------- SIDEBAR ---------------- #

st.sidebar.header("Filter Data")

department = st.sidebar.multiselect(
    "Select Department",
    options=df["Department"].unique(),
    default=df["Department"].unique()
)

filtered_df = df[df["Department"].isin(department)]

# ---------------- KPI CARDS ---------------- #

total_employees = filtered_df.shape[0]

attrition_count = filtered_df[filtered_df["Attrition"] == "Yes"].shape[0]

avg_income = int(filtered_df["MonthlyIncome"].mean())

attrition_rate = round((attrition_count / total_employees) * 100, 2)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Employees", total_employees)

col2.metric("Attrition Count", attrition_count)

col3.metric("Attrition Rate", f"{attrition_rate}%")

col4.metric("Average Income", f"${avg_income}")

# ---------------- ATTRITION CHART ---------------- #

st.subheader("Attrition by Department")

attrition_chart = px.histogram(
    filtered_df,
    x="Department",
    color="Attrition",
    barmode="group"
)

st.plotly_chart(attrition_chart, use_container_width=True)

# ---------------- JOB SATISFACTION ---------------- #

st.subheader("Job Satisfaction by Role")

job_satisfaction = filtered_df.groupby("JobRole")["JobSatisfaction"].mean().reset_index()

satisfaction_chart = px.bar(
    job_satisfaction,
    x="JobRole",
    y="JobSatisfaction",
    color="JobSatisfaction"
)

st.plotly_chart(satisfaction_chart, use_container_width=True)

# ---------------- SALARY DISTRIBUTION ---------------- #

st.subheader("Monthly Income Distribution")

income_chart = px.histogram(
    filtered_df,
    x="MonthlyIncome",
    nbins=30
)

st.plotly_chart(income_chart, use_container_width=True)

# ---------------- OVERTIME ANALYSIS ---------------- #

st.subheader("Overtime vs Attrition")

overtime_chart = px.histogram(
    filtered_df,
    x="OverTime",
    color="Attrition",
    barmode="group"
)

st.plotly_chart(overtime_chart, use_container_width=True)

# ---------------- DATA PREVIEW ---------------- #

st.subheader("Employee Data Preview")

st.dataframe(filtered_df.head())