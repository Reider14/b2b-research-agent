import os
from xmlrpc import client
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL = "gpt-4o-mini"

def structured_completion(system: str, user: str, schema):

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY nao encontrado no .env")

    client = OpenAI(api_key=api_key)





    completion = client.chat.completions.parse(
        model=MODEL,
        temperature=0,
        messages=[
            {"role": "system", content: system},
            {"role": "user", content: user}
        ],
        response_format=schema
    )

    message = completion.choices[0].message
    if message.refusal:
        raise RuntimeError(f"O modelo recusou a requisicao: {message.refusal}")
    if message.parsed is None:
        raise RuntimeError("A OpenAI retornou um resposta vazia.")
    return message.parsed