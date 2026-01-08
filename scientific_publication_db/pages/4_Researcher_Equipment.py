import streamlit as st
from sqlalchemy import text

conn = st.connection("mysql", type="sql")

st.title("Researcher ↔ Lab Equipment")

# READ
df = conn.query("""
    SELECT 
        re.EmpId,
        r.Name AS ResearcherName,
        re.EquipmentName
    FROM Researcher_Equipment re
    JOIN Researchers r ON re.EmpId = r.EmpId
    ORDER BY re.EmpId
""", ttl=0)

st.dataframe(df, width="stretch")

# Fetch researchers for dropdown
researcher_df = conn.query(
    "SELECT EmpId, Name FROM Researchers",
    ttl=0
)

# Fetch equipment for dropdown
equipment_df = conn.query(
    "SELECT EquipmentName FROM LabEquipment",
    ttl=0
)

researcher_map = {
    f"{row['EmpId']} - {row['Name']}": row["EmpId"]
    for _, row in researcher_df.iterrows()
}

equipment_list = equipment_df["EquipmentName"].tolist()

# CREATE
st.subheader("Assign equipment to researcher")

with st.form("add_researcher_equipment", clear_on_submit=True):
    researcher_label = st.selectbox(
        "Select Researcher",
        list(researcher_map.keys())
    )
    equipment = st.selectbox("Select Equipment", equipment_list)

    submit = st.form_submit_button("Assign")

if submit:
    with conn.session as session:
        session.execute(
            text("""
                INSERT INTO Researcher_Equipment (EmpId, EquipmentName)
                VALUES (:emp_id, :equipment)
            """),
            {
                "emp_id": researcher_map[researcher_label],
                "equipment": equipment
            }
        )
        session.commit()

    st.toast("Equipment assigned to researcher")
    st.rerun()

# DELETE
st.subheader("Remove equipment assignment")

with st.form("delete_researcher_equipment", clear_on_submit=True):
    selected_row = st.selectbox(
        "Select Assignment",
        df.apply(
            lambda row: f"{row.EmpId} - {row.ResearcherName} → {row.EquipmentName}",
            axis=1
        )
    )

    submit = st.form_submit_button("Remove")

if submit:
    emp_id = int(selected_row.split(" - ")[0])
    equipment_name = selected_row.split(" → ")[1]

    with conn.session as session:
        session.execute(
            text("""
                DELETE FROM Researcher_Equipment
                WHERE EmpId = :emp_id
                  AND EquipmentName = :equipment
            """),
            {
                "emp_id": emp_id,
                "equipment": equipment_name
            }
        )
        session.commit()

    st.toast("Assignment removed")
    st.rerun()
