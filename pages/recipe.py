import streamlit as st
import json
from openai import OpenAI
from pydantic import BaseModel, Field
import io
import os
from PIL import Image
from stability_sdk import client as stability_client


class Ingredient(BaseModel):
    ingredient: str = Field(description="材料", examples=["鶏肉"])
    quantity: str = Field(description="分量", examples=["300g"])


class Recipe(BaseModel):
    ingredients: list[Ingredient]
    instructions: list[str] = Field(
        description="手順", examples=[["材料を切ります。", "材料を炒めます。"]]
    )
    in_english: str = Field(description="料理名の英語")


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

        # 画像生成
        stability_api = stability_client.StabilityInference(
            key=os.environ["STABILITY_KEY"], engine="stable-diffusion-xl-1024-v1-0"
        )

        answers = stability_api.generate(
            prompt=recipe["in_english"], height=512, width=512, samples=1
        )

        for answer in answers:
            for artifact in answer.artifacts:
                if artifact.finish_reason == stability_client.generation.FILTER:
                    st.warning("画像を生成できませんでした")
                if artifact.type == stability_client.generation.ARTIFACT_IMAGE:
                    img = Image.open(io.BytesIO(artifact.binary))
                    st.image(img)
