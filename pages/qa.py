import streamlit as st
import tempfile
from pathlib import Path
from langchain.chat_models import ChatOpenAI
from llama_index.core import VectorStoreIndex
from llama_index.core.callbacks import CallbackManager
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.readers.file.docs import PDFReader
import logging

logging.basicConfig(level=logging.DEBUG)

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

            documents = PDFReader().load_data(file=Path(f.name))

            # ドキュメントをベクトル化して、ベクトルストアに保存する
            embed_model = OpenAIEmbedding()
            callback_manager = CallbackManager()
            index = VectorStoreIndex.from_documents(
                documents, embed_model=embed_model, callback_manager=callback_manager
            )
            st.session_state["index"] = index

if index is not None:
    question = st.text_input(label="質問")

    if question:
        with st.spinner(text="考え中..."):
            llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
            query_engine = index.as_query_engine(llm=llm)
            answer = query_engine.query(question)
            st.write(answer.response)
            st.info(answer.source_nodes)
