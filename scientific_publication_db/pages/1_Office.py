import streamlit as st
from sqlalchemy import text

conn = st.connection("mysql", type="sql")

st.title("Office")


# READ
df = conn.query("SELECT * FROM Office", ttl=0)
st.dataframe(df, width='stretch')

# CREATE
st.subheader("Add a new office")
with st.form("add_office", clear_on_submit=True):
    office_address = st.text_input("Office address")
    phone_extension= st.text_input("Phone extension")
    submit = st.form_submit_button("Add")

if submit:
    with conn.session as session:
        session.execute(
            text("""
                INSERT INTO Office (OfficeAddress, PhoneExtension)
                VALUES (:office_address, :phone_extension)
            """),
            {"office_address": office_address, "phone_extension": phone_extension}
        )
        session.commit()
    st.toast("Office address")
    st.rerun()

# UPDATE
st.subheader("Update selected office")
with st.form("update_office", clear_on_submit=True):
    office = st.selectbox("Select office", df["OfficeAddress"])
    new_phone_extension = st.text_input("New phone extension")
    submit = st.form_submit_button("Update")
    if submit:
        with conn.session as session:
            session.execute(
                text("""
                    UPDATE Office
                    SET PhoneExtension = :phone_extension
                    WHERE OfficeAddress = :office_address
                """),
                {"phone_extension": new_phone_extension, "office_address": office}
            )
            session.commit()
        st.toast(f"{office} phone extension updated")
        st.rerun()

# DELETE
st.subheader("Delete selected office")
with st.form("delete_office", clear_on_submit=True):
    office = st.selectbox("Select office", df["OfficeAddress"])
    submit = st.form_submit_button("Delete")
    if submit:
        with conn.session as session:
            session.execute(
                text("DELETE FROM Office WHERE OfficeAddress = :office_address"),
                {"office_address": office}
            )
            session.commit()
        st.toast(f"{office} deleted")
        st.rerun()