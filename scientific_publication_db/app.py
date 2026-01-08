import streamlit as st

st.set_page_config(
    page_title="University Course DB",
    layout="centered"
)

st.title("Scientific Publication Database")

st.markdown("""
Welcome to the **Scientific publication database CRUD** implementation using:

- **Streamlit**
- **MySQL**
- **Relational Schema with Constraints**

### Tables included
    - Office
    - Researchers
    - LabEquipment
    - Researcher_Equipment
    - JournalIssue
    - ResearchPaper
    - Paper_Authors
""")

st.divider()

# DB connection check
try:
    conn = st.connection("mysql", type="sql")
    conn.query("SELECT 1")
    st.success("Database connected successfully")
except Exception as e:
    st.error("Database connection failed")
    st.code(e)
