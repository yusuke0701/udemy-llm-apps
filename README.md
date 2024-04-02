# udemy-llm-apps

## はじめに

下記の Udemy 教材のサンプルアプリを作ってみました。

[ChatGPTのAPIで5つのアプリを作ってみよう！JSON生成、属性抽出、独自文書Q&A、SQL生成、AIエージェント](https://www.udemy.com/course/llm-apps)

## 個人メモ

### ChatGPTのAPIは過去のやりとりを保持する機能はない

ChatGPTのAPIは過去のやりとりは、APIの messages 引数に含めることで、やりとりを保持することができる。

実装例

assistant ロールで過去のやりとりを渡している。
```
from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
  ]
)
```

### トークナイザー

利用するトークンをカウントしたい場合には、tiktoken ツールなどがある。

[OpenAIのトークナイザー tiktoken の使い方](https://note.com/npaka/n/ncb4864df31c9)

### Function calling

Chat completions API の新機能。

利用可能な関数をLLMに伝えておくと、LLMが関数を使うかどうか判断してくれる。

### プロンプトで JSON 形式を出力する際の注意点

LLMの出力に余計な文字列が入る可能性があるので、正規表現などで、JSON の出力箇所だけを抽出する処理が必要になる。

また、JSONとして不正な文字列になることもある。

そこで、Function calling を使って、出力形式を指定する方法がある。

関数の使い方として、指定した形式で正しく応答するように、fine-tune されている。

Function calling の「JSON形式で引数を受け取れる「動作を、「LLMにJSON形式で出力させる機能」として使う。

### pydantic

JSON文字列を、Pythonのクラスとして定義できる。
