import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

with open(
    "outputs/articles.json",
    "r",
    encoding="utf-8"
) as f:

    papers = json.load(f)

paper = papers[0]

abstract = paper["abstract"]

prompt = f"""
Extract the following from this abstract.

Return JSON only.

Fields:
- rnas
- genes
- diseases
- key_finding

Abstract:

{abstract}
"""

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print(response.choices[0].message.content)