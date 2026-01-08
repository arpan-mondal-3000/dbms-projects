import streamlit as st
from sqlalchemy import text

conn = st.connection("mysql", type="sql")

st.title("Lab Equipment")

# READ
df = conn.query("SELECT * FROM LabEquipment", ttl=0)
st.dataframe(df, width="stretch")

# CREATE
st.subheader("Add new lab equipment")

with st.form("add_equipment", clear_on_submit=True):
    equipment_name = st.text_input("Equipment Name")
    calibration = st.text_input("Primary Calibration Standard")
    submit = st.form_submit_button("Add")

if submit:
    with conn.session as session:
        session.execute(
            text("""
                INSERT INTO LabEquipment (EquipmentName, PrimaryCalibrationStandard)
                VALUES (:name, :calibration)
            """),
            {
                "name": equipment_name,
                "calibration": calibration
            }
        )
        session.commit()

    st.toast("Lab equipment added")
    st.rerun()

# UPDATE
st.subheader("Update lab equipment")

with st.form("update_equipment", clear_on_submit=True):
    equipment = st.selectbox("Select Equipment", df["EquipmentName"])
    new_calibration = st.text_input("New Calibration Standard")
    submit = st.form_submit_button("Update")

if submit:
    with conn.session as session:
        session.execute(
            text("""
                UPDATE LabEquipment
                SET PrimaryCalibrationStandard = :calibration
                WHERE EquipmentName = :name
            """),
            {
                "calibration": new_calibration,
                "name": equipment
            }
        )
        session.commit()

    st.toast(f"{equipment} updated")
    st.rerun()

# DELETE
st.subheader("Delete lab equipment")

with st.form("delete_equipment", clear_on_submit=True):
    equipment = st.selectbox("Select Equipment", df["EquipmentName"])
    submit = st.form_submit_button("Delete")

if submit:
    with conn.session as session:
        session.execute(
            text("""
                DELETE FROM LabEquipment
                WHERE EquipmentName = :name
            """),
            {"name": equipment}
        )
        session.commit()

    st.toast(f"{equipment} deleted")
    st.rerun()
