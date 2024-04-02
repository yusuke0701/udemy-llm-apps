import streamlit as st
import json
import time

f = open("static/json/recipe.json", "r", encoding="UTF-8")
SAMPLE_JSON = f.read()
f.close()

st.title("レシピ生成AI")

dish = st.text_input(label="料理名")

if dish:
    with st.spinner(text="生成中..."):
        time.sleep(3)
        recipe = json.loads(SAMPLE_JSON)

        st.write("## 材料")
        st.table(recipe["ingredients"])

        # 以下のマークダウンの文字列を作成して表示する
        #
        # ## 手順
        # 1. 材料を切ります。
        # 2. 材料を炒めます。

        instruction_markdown = "## 手順\n"
        for i, instruction in enumerate(recipe["instructions"]):
            instruction_markdown += f"{i+1}. {instruction}\n"
        st.write(instruction_markdown)
