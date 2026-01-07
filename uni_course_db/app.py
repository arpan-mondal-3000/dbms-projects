import streamlit as st

st.set_page_config(
    page_title="University Course DB",
    layout="centered"
)

st.title("University Course Management System")

st.markdown("""
Welcome to the **University course database CRUD** implementation using:

- **Streamlit**
- **MySQL**
- **Relational Schema with Constraints**

### Tables included
- Course
- CourseClassification
- CourseFaculty
- Department
- DepartmentCourses
- Enrollments
- FinalProjects
- Instructor
- ProjectSubmission
- Student
- SubjectAreas
- User 
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
