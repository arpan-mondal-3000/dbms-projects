import streamlit as st
from sqlalchemy import text

conn = st.connection("mysql", type="sql")

st.title("Researchers")

# ===============================
# READ
# ===============================
df = conn.query("SELECT * FROM Researchers", ttl=0)
st.dataframe(df, width="stretch")

# Fetch offices for dropdown
office_df = conn.query(
    "SELECT OfficeAddress FROM Office",
    ttl=0
)

office_list = office_df["OfficeAddress"].tolist()

# ===============================
# CREATE
# ===============================
st.subheader("Add a new researcher")

with st.form("add_researcher", clear_on_submit=True):
    emp_id = st.number_input("Employee ID", min_value=1, step=1)
    name = st.text_input("Researcher Name")
    office = st.selectbox("Office Address", office_list)

    submit = st.form_submit_button("Add")

if submit:
    with conn.session as session:
        session.execute(
            text("""
                INSERT INTO Researchers (EmpId, Name, OfficeAddress)
                VALUES (:emp_id, :name, :office)
            """),
            {
                "emp_id": emp_id,
                "name": name,
                "office": office
            }
        )
        session.commit()

    st.toast("Researcher added successfully")
    st.rerun()

# ===============================
# UPDATE
# ===============================
st.subheader("Update researcher")

with st.form("update_researcher", clear_on_submit=True):
    researcher_id = st.selectbox("Select Researcher ID", df["EmpId"])
    new_name = st.text_input("New Name")
    new_office = st.selectbox("New Office Address", office_list)

    submit = st.form_submit_button("Update")

if submit:
    with conn.session as session:
        session.execute(
            text("""
                UPDATE Researchers
                SET Name = :name,
                    OfficeAddress = :office
                WHERE EmpId = :emp_id
            """),
            {
                "name": new_name,
                "office": new_office,
                "emp_id": researcher_id
            }
        )
        session.commit()

    st.toast("Researcher updated")
    st.rerun()

# ===============================
# DELETE
# ===============================
st.subheader("Delete researcher")

with st.form("delete_researcher", clear_on_submit=True):
    researcher_id = st.selectbox("Select Researcher ID", df["EmpId"])
    submit = st.form_submit_button("Delete")

if submit:
    with conn.session as session:
        session.execute(
            text("""
                DELETE FROM Researchers
                WHERE EmpId = :emp_id
            """),
            {"emp_id": researcher_id}
        )
        session.commit()

    st.toast("Researcher deleted")
    st.rerun()
