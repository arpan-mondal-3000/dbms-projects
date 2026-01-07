import streamlit as st
import pandas as pd
from sqlalchemy import text

conn = st.connection("mysql", type="sql")

st.title("Departments")


# READ
df = conn.query("SELECT * FROM Department", ttl=0)
st.dataframe(df, width='stretch')

# CREATE
st.subheader("Add a new department")
with st.form("add_department", clear_on_submit=True):
    name = st.text_input("Department Name")
    location = st.text_input("Location")
    submit = st.form_submit_button("Add")

if submit:
    with conn.session as session:
        session.execute(
            text("""
                INSERT INTO Department (name, location)
                VALUES (:name, :location)
            """),
            {"name": name, "location": location}
        )
        session.commit()
    st.toast("Department added")
    st.rerun()

# UPDATE
st.subheader("Update selected department")
with st.form("update_department", clear_on_submit=True):
    dept = st.selectbox("Select Department", df["name"])
    new_loc = st.text_input("New Location")
    submit = st.form_submit_button("Update")
    if submit:
        with conn.session as session:
            session.execute(
                text("""
                    UPDATE Department
                    SET location = :loc
                    WHERE name = :name
                """),
                {"loc": new_loc, "name": dept}
            )
            session.commit()
        st.toast(f"{dept} location updated")
        st.rerun()

# DELETE
if st.button("Delete"):
    with conn.session as session:
        session.execute(
            text("DELETE FROM Department WHERE name = :name"),
            {"name": dept}
        )
        session.commit()
    st.toast(f"{dept} deleted")
    st.rerun()