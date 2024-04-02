import streamlit as st
import json
from openai import OpenAI
from pydantic import BaseModel, Field


class Ingredient(BaseModel):
    ingredient: str = Field(description="材料", examples=["鶏肉"])
    quantity: str = Field(description="分量", examples=["300g"])


class Recipe(BaseModel):
    ingredients: list[Ingredient]
    instructions: list[str] = Field(
        description="手順", examples=[["材料を切ります。", "材料を炒めます。"]]
    )


f = open("static/prompt/recipe.txt", "r", encoding="UTF-8")
PROMPT_TEMPLATE = f.read()
f.close()

OUTPUT_RECIPE_FUNCTION = {
    "name": "output_recipe",
    "description": "レシピを出力する",
    "parameters": Recipe.schema(),
}

st.title("レシピ生成AI")

dish = st.text_input(label="料理名")

client = OpenAI()

if dish:
    with st.spinner(text="生成中..."):
        messages = [
            {
                "role": "user",
                "content": PROMPT_TEMPLATE.format(dish=dish),
            }
        ]
        tools = [{"type": "function", "function": OUTPUT_RECIPE_FUNCTION}]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            for tool_call in tool_calls:
                recipe = json.loads(tool_call.function.arguments)

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
