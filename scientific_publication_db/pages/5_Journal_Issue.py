import streamlit as st
from sqlalchemy import text

conn = st.connection("mysql", type="sql")

st.title("Journal Issues")

# READ
df = conn.query("""
    SELECT 
        j.VolumeIdentifier,
        j.Title,
        j.PublicationDate,
        j.Format,
        r.Name AS EditorInChief
    FROM JournalIssue j
    JOIN Researchers r ON j.EditorInChief = r.EmpId
    ORDER BY j.VolumeIdentifier
""", ttl=0)

st.dataframe(df, width="stretch")

# Fetch researchers for editor dropdown
researcher_df = conn.query(
    "SELECT EmpId, Name FROM Researchers",
    ttl=0
)

editor_map = {
    f"{row['EmpId']} - {row['Name']}": row["EmpId"]
    for _, row in researcher_df.iterrows()
}

# CREATE
st.subheader("Add journal issue")

with st.form("add_journal_issue", clear_on_submit=True):
    volume_id = st.number_input("Volume Identifier", min_value=1, step=1)
    title = st.text_input("Journal Title")
    pub_date = st.date_input("Publication Date")
    format_type = st.selectbox("Format", ["Print", "Online"])
    editor_label = st.selectbox("Editor-in-Chief", list(editor_map.keys()))

    submit = st.form_submit_button("Add")

if submit:
    with conn.session as session:
        session.execute(
            text("""
                INSERT INTO JournalIssue
                (VolumeIdentifier, Title, PublicationDate, Format, EditorInChief)
                VALUES (:vol, :title, :date, :format, :editor)
            """),
            {
                "vol": volume_id,
                "title": title,
                "date": pub_date,
                "format": format_type,
                "editor": editor_map[editor_label]
            }
        )
        session.commit()

    st.toast("Journal issue added")
    st.rerun()

# UPDATE
st.subheader("Update journal issue")

with st.form("update_journal_issue", clear_on_submit=True):
    selected_vol = st.selectbox("Select Volume", df["VolumeIdentifier"])
    current_title = df[df["VolumeIdentifier"] == selected_vol]["Title"].iloc[0]
    new_title = st.text_input("New Title")
    new_date = st.date_input("New Publication Date")
    new_format = st.selectbox("New Format", ["Print", "Online"])
    new_editor_label = st.selectbox("New Editor-in-Chief", list(editor_map.keys()))

    submit = st.form_submit_button("Update")

if submit:
    if new_title.strip() == "":
        new_title = current_title
    with conn.session as session:
        session.execute(
            text("""
                UPDATE JournalIssue
                SET Title = :title,
                    PublicationDate = :date,
                    Format = :format,
                    EditorInChief = :editor
                WHERE VolumeIdentifier = :vol
            """),
            {
                "title": new_title,
                "date": new_date,
                "format": new_format,
                "editor": editor_map[new_editor_label],
                "vol": selected_vol
            }
        )
        session.commit()

    st.toast("Journal issue updated")
    st.rerun()

# DELETE
st.subheader("Delete journal issue")

with st.form("delete_journal_issue", clear_on_submit=True):
    selected_vol = st.selectbox("Select Volume", df["VolumeIdentifier"])
    submit = st.form_submit_button("Delete")

if submit:
    with conn.session as session:
        session.execute(
            text("""
                DELETE FROM JournalIssue
                WHERE VolumeIdentifier = :vol
            """),
            {"vol": selected_vol}
        )
        session.commit()

    st.toast("Journal issue deleted")
    st.rerun()
