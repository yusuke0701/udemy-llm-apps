import streamlit as st

st.title("タグ付け")

text = st.text_area(label="タグ付けするテキスト")

if text:
    with st.spinner("タグ付け中..."):
        attr = {"language": "ja", "tags": ["Python", "Streamlit"]}
        st.write(attr)
