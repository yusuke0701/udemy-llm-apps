import streamlit as st
from openai import OpenAI

st.title("simple chat")

client = OpenAI()

user_message = st.text_input(label="どうしましたか？")

if user_message:
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message},
        ],
    )

    print(completion.choices[0].message)
    st.write(completion)
