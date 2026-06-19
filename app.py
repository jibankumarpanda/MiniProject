import streamlit as st

st.set_page_config(
    page_title="Chess Puzzle Solver",
    page_icon="♟️",
    layout="wide"
)

st.title("♟️ Chess Puzzle Solver")

st.write("Upload a chess puzzle dataset (.txt)")

uploaded_file = st.file_uploader(
    "Choose a TXT file",
    type=["txt"]
)

if uploaded_file:
    content = uploaded_file.read().decode("utf-8")

    st.success("File uploaded successfully!")

    st.subheader("File Content")

    st.code(content)