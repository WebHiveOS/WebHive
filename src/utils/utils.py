# -*- coding: utf-8 -*-
# @Time    : 2025/1/1
# @Author  : wenshao
# @Email   : wenshaoguo1026@gmail.com
# @Project : browser-use-webui
# @FileName: utils.py

import base64
import os

from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama


def get_llm_model(provider: str, **kwargs):
    """
    获取LLM 模型
    :param provider: 模型类型
    :param kwargs:
    :return:
    """
    if provider == 'anthropic':
        if not kwargs.get("base_url", ""):
            base_url = "https://api.anthropic.com"
        else:
            base_url = kwargs.get("base_url")

        if not kwargs.get("api_key", ""):
            api_key = os.getenv("ANTHROPIC_API_KEY", "")
        else:
            api_key = kwargs.get("api_key")

        return ChatAnthropic(
            model_name=kwargs.get("model_name", 'claude-3-5-sonnet-20240620'),
            temperature=kwargs.get("temperature", 0.0),
            base_url=base_url,
            api_key=api_key
        )
    elif provider == 'openai':
        if not kwargs.get("base_url", ""):
            base_url = os.getenv("OPENAI_ENDPOINT", "https://api.openai.com/v1")
        else:
            base_url = kwargs.get("base_url")

        if not kwargs.get("api_key", ""):
            api_key = os.getenv("OPENAI_API_KEY", "")
        else:
            api_key = kwargs.get("api_key")

        return ChatOpenAI(
            model=kwargs.get("model_name", 'gpt-4o'),
            temperature=kwargs.get("temperature", 0.0),
            base_url=base_url,
            api_key=api_key
        )
    elif provider == 'deepseek':
        if not kwargs.get("base_url", ""):
            base_url = os.getenv("DEEPSEEK_ENDPOINT", "")
        else:
            base_url = kwargs.get("base_url")

        if not kwargs.get("api_key", ""):
            api_key = os.getenv("DEEPSEEK_API_KEY", "")
        else:
            api_key = kwargs.get("api_key")

        return ChatOpenAI(
            model=kwargs.get("model_name", 'deepseek-chat'),
            temperature=kwargs.get("temperature", 0.0),
            base_url=base_url,
            api_key=api_key
        )
    elif provider == 'gemini':
        if not kwargs.get("api_key", ""):
            api_key = os.getenv("GOOGLE_API_KEY", "")
        else:
            api_key = kwargs.get("api_key")
        return ChatGoogleGenerativeAI(
            model=kwargs.get("model_name", 'gemini-2.0-flash-exp'),
            temperature=kwargs.get("temperature", 0.0),
            google_api_key=api_key,
        )
    elif provider == 'ollama':
        return ChatOllama(
            model=kwargs.get("model_name", 'qwen2.5:7b'),
            temperature=kwargs.get("temperature", 0.0),
        )
    elif provider == "azure_openai":
        if not kwargs.get("base_url", ""):
            base_url = os.getenv("AZURE_OPENAI_ENDPOINT", "")
        else:
            base_url = kwargs.get("base_url")
        if not kwargs.get("api_key", ""):
            api_key = os.getenv("AZURE_OPENAI_API_KEY", "")
        else:
            api_key = kwargs.get("api_key")
        return AzureChatOpenAI(
            model=kwargs.get("model_name", 'gpt-4o'),
            temperature=kwargs.get("temperature", 0.0),
            api_version="2024-05-01-preview",
            azure_endpoint=base_url,
            api_key=api_key
        )
    else:
        raise ValueError(f'Unsupported provider: {provider}')

from openai import OpenAI, AzureOpenAI
from google.generativeai import configure, list_models
from langchain_anthropic import AnthropicLLM
from langchain_ollama.llms import OllamaLLM

def fetch_available_models(llm_provider: str, api_key: str = None, base_url: str = None) -> list[str]:
    try:
        if llm_provider == "anthropic":
            client = AnthropicLLM(api_key=api_key)
            # Handle model fetching appropriately for Anthropic
            return ["claude-3-5-sonnet-20240620"]  # Replace with actual model fetching logic

        elif llm_provider == "openai":
            client = OpenAI(api_key=api_key, base_url=base_url)
            models = client.models.list()
            return [model.id for model in models.data]

        elif llm_provider == "deepseek":
            # For Deepseek, we'll return the default model for now
            return ["deepseek-chat"]

        elif llm_provider == "gemini":
            configure(api_key=api_key)
            models = list_models()
            return [model.name for model in models]

        elif llm_provider == "ollama":
            client = OllamaLLM(model="default_model_name")  # Replace with the actual model name
            models = client.models.list()
            return [model.name for model in models]

        elif llm_provider == "azure_openai":
            client = AzureOpenAI(api_key=api_key, base_url=base_url)
            models = client.models.list()
            return [model.id for model in models.data]

        else:
            print(f"Unsupported LLM provider: {llm_provider}")
            return []

    except Exception as e:
        print(f"Error fetching models from {llm_provider}: {e}")
        return []

def encode_image(img_path):
    if not img_path:
        return None
    with open(img_path, "rb") as fin:
        image_data = base64.b64encode(fin.read()).decode("utf-8")
    return image_data
