import json
from openai import OpenAI

from src.schemas import PromptConfig, ClassifierOutput


client = OpenAI()


def classify_email(email_text: str, prompt_config: PromptConfig, model: str = "gpt-4o-mini") -> ClassifierOutput:
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