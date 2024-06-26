# udemy-llm-apps

## はじめに

下記の Udemy 教材のサンプルアプリを作ってみました。

[ChatGPTのAPIで5つのアプリを作ってみよう！JSON生成、属性抽出、独自文書Q&A、SQL生成、AIエージェント](https://www.udemy.com/course/llm-apps)

## 個人メモ

### zip化コマンド

`zip -r udemy-llm-apps/ udemy-llm-apps`

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

### Stable Diffusion

自然言語から画像を生成する機械学習モデル。

公開されているモデルをダウンロードして使用するか、Stability AI 社の DreamStudio といったWebサービスで使用できる。

### LangChain

LLMを使ったアプリ開発のフレームワーク。

大きく二つの使い方がある。

1. LLMを使った様々なアプリで部品として使えるコンポーネントの提供
2. LLMを使った特定のユースケースに特化した実装例を提供

### 属性抽出の応用例

PDFなどのファイルから属性を抽出することも考えられる。

OCRと組み合わせることで、画像から属性を抽出することも考えられる。

### LLMを使った独自データへのQ＆Aの基本

1. PDFのチャンク化(適当なサイズに分割)
2. ベクトル化して、Vector Store に保存
3. 質問文と近いテキストを検索
4. 検索結果をプロンプトに含めて、LLMを呼び出す

検索結果をプロンプトに含めてLLMに返答させる手法を、RAG(Retrieval Argumented Generation)と呼ぶ。

### LlamaIndex

LlamaIndex は、LLMを外部データに接続して使うためのフレームワーク。

LLM -> LlamaIndex -> Local File(PDFなど), Notion, Google Docs, Wikipedia

### AIエージェント

目的に対して、自律的に判断して動くプログラム。

### Make

#### 概要

Webサービスと、Webサービスを連携できる IPaaS の一つ。

似たようなサービスとして、IFTTT, Zapier などがある。

### シナリオ

Webサービスをシナリオとして、連携する。

コーディングなしでできる。

### LLMとMakeの連携

LLMが生成した指示をもとに、MakeのWebhookを呼び出すこともできる。
