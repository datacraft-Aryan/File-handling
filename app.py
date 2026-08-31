import streamlit as st
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------
# Config
# ---------------------------------------------------------------
st.set_page_config(
    page_title="FileDesk | File Manager",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="expanded",
)

WORKSPACE = Path("workspace")
WORKSPACE.mkdir(exist_ok=True)

# ---------------------------------------------------------------
# Styling
# ---------------------------------------------------------------
st.markdown("""
<style>
    .main { background-color: #0e1117; }

    .filedesk-header {
        padding: 1.6rem 2rem;
        border-radius: 16px;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #06b6d4 100%);
        margin-bottom: 1.5rem;
    }
    .filedesk-header h1 {
        color: white;
        margin: 0;
        font-size: 2rem;
        font-weight: 800;
    }
    .filedesk-header p {
        color: rgba(255,255,255,0.9);
        margin: 0.3rem 0 0 0;
        font-size: 1rem;
    }

    .stat-card {
        background: #1a1c24;
        border: 1px solid #2d2f3a;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        text-align: center;
    }
    .stat-card h2 { margin: 0; color: #a78bfa; font-size: 1.8rem; }
    .stat-card p { margin: 0; color: #9ca3af; font-size: 0.85rem; }

    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
        border: none;
    }

    .file-row {
        background: #1a1c24;
        border: 1px solid #2d2f3a;
        border-radius: 10px;
        padding: 0.6rem 1rem;
        margin-bottom: 0.4rem;
    }

    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------
# Header
# ---------------------------------------------------------------
st.markdown("""
<div class="filedesk-header">
    <h1>📁 FileDesk</h1>
    <p>A simple, safe file management app — Create · Read · Update · Delete — built with Python & Streamlit</p>
</div>
""", unsafe_allow_html=True)


def safe_path(filename: str) -> Path:
    """Keep every operation confined to the workspace folder."""
    filename = filename.strip()
    candidate = (WORKSPACE / filename).resolve()
    if WORKSPACE.resolve() not in candidate.parents and candidate != WORKSPACE.resolve():
        raise ValueError("Invalid file name / path.")
    return candidate


def list_files():
    return sorted([p for p in WORKSPACE.iterdir() if p.is_file()])


# ---------------------------------------------------------------
# Sidebar - stats + file browser
# ---------------------------------------------------------------
with st.sidebar:
    st.markdown("### 📊 Workspace overview")
    files = list_files()
    total_size = sum(f.stat().st_size for f in files)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="stat-card"><h2>{len(files)}</h2><p>Files</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat-card"><h2>{total_size}</h2><p>Bytes</p></div>', unsafe_allow_html=True)

    st.markdown("###  ")
    st.markdown("### 🗂️ Files in workspace")
    if files:
        for f in files:
            size = f.stat().st_size
            modified = datetime.fromtimestamp(f.stat().st_mtime).strftime("%d %b, %H:%M")
            st.markdown(
                f'<div class="file-row"><b>{f.name}</b><br>'
                f'<span style="color:#9ca3af;font-size:0.8rem;">{size} bytes • {modified}</span></div>',
                unsafe_allow_html=True,
            )
    else:
        st.info("No files yet. Create one to get started!")

    st.markdown("---")
    st.caption("All operations are sandboxed to a local `workspace/` folder for safety.")

# ---------------------------------------------------------------
# Main tabs
# ---------------------------------------------------------------
tab_create, tab_read, tab_update, tab_delete = st.tabs(
    ["✨ Create", "📖 Read", "✏️ Update", "🗑️ Delete"]
)

# ---------------- CREATE ----------------
with tab_create:
    st.subheader("Create a new file")
    with st.form("create_form", clear_on_submit=False):
        name = st.text_input("File name", placeholder="e.g. notes.txt")
        content = st.text_area("File content", placeholder="Write something...", height=180)
        submitted = st.form_submit_button("🚀 Create file", use_container_width=True)

    if submitted:
        if not name.strip():
            st.error("Please enter a file name.")
        else:
            try:
                path = safe_path(name)
                if path.exists():
                    st.error(f"⚠️ A file named **{path.name}** already exists.")
                else:
                    path.write_text(content, encoding="utf-8")
                    st.success(f"✅ File **{path.name}** created successfully!")
                    st.balloons()
                    st.rerun()
            except Exception as err:
                st.error(f"An error occurred: {err}")

# ---------------- READ ----------------
with tab_read:
    st.subheader("Read a file")
    files = list_files()
    if not files:
        st.info("No files available to read yet. Create one first.")
    else:
        chosen = st.selectbox("Choose a file", [f.name for f in files])
        if chosen:
            path = WORKSPACE / chosen
            try:
                content = path.read_text(encoding="utf-8")
                st.code(content if content else "(this file is empty)", language=None)
                st.download_button(
                    "⬇️ Download file",
                    data=content,
                    file_name=chosen,
                    use_container_width=True,
                )
            except Exception as err:
                st.error(f"An error occurred: {err}")

# ---------------- UPDATE ----------------
with tab_update:
    st.subheader("Update a file")
    files = list_files()
    if not files:
        st.info("No files available to update yet. Create one first.")
    else:
        chosen = st.selectbox("Choose a file", [f.name for f in files], key="update_select")
        operation = st.radio(
            "What would you like to do?",
            ["✏️ Rename", "➕ Append content", "♻️ Overwrite content"],
            horizontal=True,
        )
        path = WORKSPACE / chosen

        if operation == "✏️ Rename":
            new_name = st.text_input("New file name")
            if st.button("Rename", use_container_width=True):
                try:
                    new_path = safe_path(new_name)
                    if new_path.exists():
                        st.error("⚠️ A file with that name already exists.")
                    elif not new_name.strip():
                        st.error("Please enter a new file name.")
                    else:
                        path.rename(new_path)
                        st.success(f"✅ Renamed to **{new_path.name}**")
                        st.rerun()
                except Exception as err:
                    st.error(f"An error occurred: {err}")

        elif operation == "➕ Append content":
            extra = st.text_area("Content to append", height=140)
            if st.button("Append", use_container_width=True):
                try:
                    with open(path, "a", encoding="utf-8") as fs:
                        fs.write("\n" + extra)
                    st.success("✅ Content appended successfully!")
                    st.rerun()
                except Exception as err:
                    st.error(f"An error occurred: {err}")

        elif operation == "♻️ Overwrite content":
            new_content = st.text_area("New content (replaces everything)", height=180)
            if st.button("Overwrite", type="primary", use_container_width=True):
                try:
                    path.write_text(new_content, encoding="utf-8")
                    st.success("✅ File overwritten successfully!")
                    st.rerun()
                except Exception as err:
                    st.error(f"An error occurred: {err}")

# ---------------- DELETE ----------------
with tab_delete:
    st.subheader("Delete a file")
    files = list_files()
    if not files:
        st.info("No files available to delete.")
    else:
        chosen = st.selectbox("Choose a file to delete", [f.name for f in files], key="delete_select")
        st.warning(f"This will permanently delete **{chosen}**. This action cannot be undone.")
        confirm = st.checkbox("I understand, delete this file")
        if st.button("🗑️ Delete file", type="primary", disabled=not confirm, use_container_width=True):
            try:
                (WORKSPACE / chosen).unlink()
                st.success(f"✅ **{chosen}** deleted successfully.")
                st.rerun()
            except Exception as err:
                st.error(f"An error occurred: {err}")

st.markdown("---")
st.caption("Built with ❤️ using Python & Streamlit — a beginner-friendly file handling CRUD project.")