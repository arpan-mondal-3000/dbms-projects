import streamlit as st
from sqlalchemy import text

conn = st.connection("mysql", type="sql")

st.title("Research Papers")

# READ
df = conn.query("""
    SELECT
        rp.PaperId,
        rp.Title,
        rp.VolumeIdentifier,
        ji.Title AS JournalTitle,
        r.Name AS LeadAuthor
    FROM ResearchPaper rp
    JOIN JournalIssue ji ON rp.VolumeIdentifier = ji.VolumeIdentifier
    JOIN Researchers r ON rp.LeadAuthor = r.EmpId
    ORDER BY rp.PaperId
""", ttl=0)

st.dataframe(df, width="stretch")

# Fetch journal issues
journal_df = conn.query(
    "SELECT VolumeIdentifier, Title FROM JournalIssue",
    ttl=0
)

journal_map = {
    f"{row['VolumeIdentifier']} - {row['Title']}": row["VolumeIdentifier"]
    for _, row in journal_df.iterrows()
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

# CREATE
st.subheader("Add research paper")

with st.form("add_research_paper", clear_on_submit=True):
    title = st.text_input("Paper Title")
    journal_label = st.selectbox("Journal Issue", list(journal_map.keys()))
    lead_author_label = st.selectbox("Lead Author", list(researcher_map.keys()))

    submit = st.form_submit_button("Add")

if submit:
    with conn.session as session:
        session.execute(
            text("""
                INSERT INTO ResearchPaper (Title, VolumeIdentifier, LeadAuthor)
                VALUES (:title, :volume, :author)
            """),
            {
                "title": title,
                "volume": journal_map[journal_label],
                "author": researcher_map[lead_author_label]
            }
        )
        session.commit()

    st.toast("Research paper added")
    st.rerun()

# UPDATE
st.subheader("Update research paper")

with st.form("update_research_paper", clear_on_submit=True):
    paper_id = st.selectbox("Select Paper ID", df["PaperId"])
    new_title = st.text_input("New Title")
    new_journal_label = st.selectbox("New Journal Issue", list(journal_map.keys()))
    new_lead_author_label = st.selectbox("New Lead Author", list(researcher_map.keys()))

    submit = st.form_submit_button("Update")

if submit:
    with conn.session as session:
        session.execute(
            text("""
                UPDATE ResearchPaper
                SET Title = :title,
                    VolumeIdentifier = :volume,
                    LeadAuthor = :author
                WHERE PaperId = :paper_id
            """),
            {
                "title": new_title,
                "volume": journal_map[new_journal_label],
                "author": researcher_map[new_lead_author_label],
                "paper_id": paper_id
            }
        )
        session.commit()

    st.toast("Research paper updated")
    st.rerun()

# DELETE
st.subheader("Delete research paper")

with st.form("delete_research_paper", clear_on_submit=True):
    paper_id = st.selectbox("Select Paper ID", df["PaperId"])
    submit = st.form_submit_button("Delete")

if submit:
    with conn.session as session:
        session.execute(
            text("""
                DELETE FROM ResearchPaper
                WHERE PaperId = :paper_id
            """),
            {"paper_id": paper_id}
        )
        session.commit()

    st.toast("Research paper deleted")
    st.rerun()
