import os
import json

from dotenv import load_dotenv
from groq import Groq

from src.schemas import PromptConfig, ClassifierOutput


load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def classify_email(
    email_text: str,
    prompt_config: PromptConfig,
    model: str = "llama-3.1-8b-instant",
) -> ClassifierOutput:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": prompt_config.system_prompt,
            },
            {
                "role": "user",
                "content": email_text,
            },
        ],
        temperature=0,
    )

    raw_output = response.choices[0].message.content

    try:
        parsed = json.loads(raw_output)
    except json.JSONDecodeError as error:
        raise ValueError(f"Model did not return valid JSON: {raw_output}") from error

    return ClassifierOutput(**parsed)