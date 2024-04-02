import streamlit as st
import tempfile

st.title("PDFへのQ&A")

index = st.session_state.get("index")


def on_change_file():
    if "index" in st.session_state:
        st.session_state.pop("index")


uploaded_file = st.file_uploader(label="Q&A対象のファイル", type="PDF")

if uploaded_file and index is None:
    with st.spinner(text="準備中..."):
        with tempfile.NamedTemporaryFile() as f:
            f.write(uploaded_file.getbuffer())
            st.write(f"ファイル名: {f.name}")

            # TODO: 文章をベクトル化して、Q&Aの準備を実施

            index = "index"
            st.session_state["index"] = index

if index is not None:
    question = st.text_input(label="質問")

    if question:
        with st.spinner(text="考え中..."):
            answer = "回答"
            st.write(answer)
