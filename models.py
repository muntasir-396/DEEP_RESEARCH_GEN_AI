import os

from langchain_mistralai import ChatMistralAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_xai import ChatXAI


def get_model(model_name):

    if model_name == "Mistral":

        return ChatMistralAI(
            model="mistral-small-latest",
            mistral_api_key=os.getenv("MISTRAL_API_KEY"),
            temperature=0
        )

    elif model_name == "Gemini":

        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0
        )

    elif model_name == "Grok":

        return ChatXAI(
            model="grok-3-mini",
            xai_api_key=os.getenv("XAI_API_KEY"),
            temperature=0
        )

    else:

        raise ValueError(
            f"Unsupported model: {model_name}"
        )