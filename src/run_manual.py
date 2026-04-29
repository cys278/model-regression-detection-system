from src.prompt_loader import load_prompt_config
from src.classifier import classify_email


if __name__ == "__main__":
    prompt = load_prompt_config("prompts/classifier_v1.yaml")

    email = """
    Hi, I cannot log into my account even after resetting my password.
    Can someone help me get access again?
    """

    result = classify_email(email, prompt)

    print(result.model_dump_json(indent=2))