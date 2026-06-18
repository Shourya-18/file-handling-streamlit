import streamlit as st
from pathlib import Path
import os

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="File Manager Pro",
    page_icon="📂",
    layout="wide"
)

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}

.title {
    text-align:center;
    color:#4CAF50;
    font-size:45px;
    font-weight:bold;
}

.subtitle {
    text-align:center;
    color:gray;
    font-size:18px;
}

.card {
    background-color:#1E1E1E;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 0px 15px rgba(255,255,255,0.1);
}
</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown("<div class='title'>📂 File Manager Pro</div>",
            unsafe_allow_html=True)

st.markdown(
    "<div class='subtitle'>Create • Read • Update • Delete Files Easily</div>",
    unsafe_allow_html=True
)

st.write("")

# ------------------ SIDEBAR ------------------
st.sidebar.title("📁 Files Explorer")

files = [f for f in os.listdir() if os.path.isfile(f)]

if files:
    selected_file = st.sidebar.selectbox(
        "Available Files",
        files
    )
else:
    selected_file = None
    st.sidebar.info("No files found")

# ------------------ MENU ------------------
operation = st.selectbox(
    "Choose Operation",
    [
        "Create File",
        "Read File",
        "Update File",
        "Delete File"
    ]
)

# ==================================================
# CREATE FILE
# ==================================================
if operation == "Create File":

    st.subheader("➕ Create New File")

    filename = st.text_input("File Name")

    content = st.text_area("Write Content")

    if st.button("Create File"):

        path = Path(filename)

        if path.exists():
            st.error("File already exists")
        else:
            with open(path, "w") as f:
                f.write(content)

            st.success("File Created Successfully")

# ==================================================
# READ FILE
# ==================================================
elif operation == "Read File":

    st.subheader("📖 Read File")

    filename = st.text_input(
        "Enter File Name",
        value=selected_file if selected_file else ""
    )

    if st.button("Read"):

        path = Path(filename)

        if path.exists():

            with open(path, "r") as f:
                content = f.read()

            st.code(content)

        else:
            st.error("File Not Found")

# ==================================================
# UPDATE FILE
# ==================================================
elif operation == "Update File":

    st.subheader("✏️ Update File")

    filename = st.text_input(
        "Enter File Name",
        value=selected_file if selected_file else ""
    )

    update_option = st.radio(
        "Choose Action",
        [
            "Rename",
            "Append",
            "Overwrite"
        ]
    )

    path = Path(filename)

    # Rename
    if update_option == "Rename":

        new_name = st.text_input("New File Name")

        if st.button("Rename File"):

            if path.exists():

                new_path = Path(new_name)

                if new_path.exists():
                    st.error("Target file already exists")

                else:
                    path.rename(new_path)
                    st.success("File Renamed Successfully")

            else:
                st.error("File Not Found")

    # Append
    elif update_option == "Append":

        append_text = st.text_area("Content to Append")

        if st.button("Append Data"):

            if path.exists():

                with open(path, "a") as f:
                    f.write("\n" + append_text)

                st.success("Content Appended")

            else:
                st.error("File Not Found")

    # Overwrite
    elif update_option == "Overwrite":

        overwrite_text = st.text_area("New Content")

        if st.button("Overwrite File"):

            if path.exists():

                with open(path, "w") as f:
                    f.write(overwrite_text)

                st.success("File Overwritten")

            else:
                st.error("File Not Found")

# ==================================================
# DELETE FILE
# ==================================================
elif operation == "Delete File":

    st.subheader("🗑️ Delete File")

    filename = st.text_input(
        "Enter File Name",
        value=selected_file if selected_file else ""
    )

    if st.button("Delete File"):

        path = Path(filename)

        if path.exists():

            path.unlink()

            st.success("File Deleted Successfully")

        else:
            st.error("File Not Found")

# ==================================================
# FILE STATS
# ==================================================
st.markdown("---")
st.subheader("📊 Project Statistics")

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Files", len(files))

with col2:
    total_size = sum(
        os.path.getsize(f)
        for f in files
    ) if files else 0

    st.metric(
        "Storage Used",
        f"{round(total_size/1024,2)} KB"
    )
