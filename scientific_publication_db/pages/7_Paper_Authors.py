import streamlit as st
from sqlalchemy import text

conn = st.connection("mysql", type="sql")

st.title("Paper Authors")

# ===============================
# READ
# ===============================
df = conn.query("""
    SELECT
        pa.PaperId,
        rp.Title AS PaperTitle,
        r.EmpId,
        r.Name AS AuthorName
    FROM Paper_Authors pa
    JOIN ResearchPaper rp ON pa.PaperId = rp.PaperId
    JOIN Researchers r ON pa.EmpId = r.EmpId
    ORDER BY pa.PaperId, r.EmpId
""", ttl=0)

st.dataframe(df, width="stretch")

# Fetch papers
paper_df = conn.query(
    "SELECT PaperId, Title FROM ResearchPaper",
    ttl=0
)

paper_map = {
    f"{row['PaperId']} - {row['Title']}": row["PaperId"]
    for _, row in paper_df.iterrows()
}

# Fetch researchers
researcher_df = conn.query(
    "SELECT EmpId, Name FROM Researchers",
    ttl=0
)

researcher_map = {
    f"{row['EmpId']} - {row['Name']}": row["EmpId"]
    for _, row in researcher_df.iterrows()
}

# ===============================
# CREATE
# ===============================
st.subheader("Add author to paper")

with st.form("add_paper_author", clear_on_submit=True):
    paper_label = st.selectbox("Select Paper", list(paper_map.keys()))
    author_label = st.selectbox("Select Author", list(researcher_map.keys()))
    submit = st.form_submit_button("Add Author")

if submit:
    with conn.session as session:
        session.execute(
            text("""
                INSERT INTO Paper_Authors (PaperId, EmpId)
                VALUES (:paper_id, :emp_id)
            """),
            {
                "paper_id": paper_map[paper_label],
                "emp_id": researcher_map[author_label]
            }
        )
        session.commit()

    st.toast("Author added to paper")
    st.rerun()

# ===============================
# DELETE
# ===============================
st.subheader("Remove author from paper")

with st.form("delete_paper_author", clear_on_submit=True):
    selected_entry = st.selectbox(
        "Select Paper-Author entry",
        df.apply(
            lambda row: f"{row.PaperId} - {row.PaperTitle} → {row.AuthorName}",
            axis=1
        )
    )
    submit = st.form_submit_button("Remove Author")

if submit:
    paper_id = int(selected_entry.split(" - ")[0])
    author_name = selected_entry.split(" → ")[1]

    # Get EmpId from name (safe because dropdown came from joined data)
    emp_id = df[df["AuthorName"] == author_name]["EmpId"].iloc[0]

    with conn.session as session:
        session.execute(
            text("""
                DELETE FROM Paper_Authors
                WHERE PaperId = :paper_id
                  AND EmpId = :emp_id
            """),
            {
                "paper_id": paper_id,
                "emp_id": emp_id
            }
        )
        session.commit()

    st.toast("Author removed from paper")
    st.rerun()
