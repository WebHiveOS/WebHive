# -*- coding: utf-8 -*-
# @Time    : 2025/1/1
# @Author  : wenshao
# @Email   : wenshaoguo1026@gmail.com
# @Project : browser-use-webui
# @FileName: utils.py

import base64
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI


def get_llm_model(provider: str, **kwargs):
    """
    获取LLM 模型
    :param provider: 模型类型
    :param kwargs:
    :return:
    """
    if provider == 'claude':
        return ChatAnthropic(
            model_name=kwargs.get("model_name", 'claude-3-5-sonnet-20240620'),
            temperature=kwargs.get("temperature", 0.0),
            base_url=kwargs.get("base_url", "https://api.anthropic.com"),
            api_key=kwargs.get("api_key", None)
        )
    elif provider == 'openai':
        return ChatOpenAI(
            model=kwargs.get("model_name", 'gpt-4o'),
            temperature=kwargs.get("temperature", 0.0),
            base_url=kwargs.get("base_url", "https://api.openai.com/v1/"),
            api_key=kwargs.get("api_key", None)
        )
    elif provider == 'gemini':
        return ChatGoogleGenerativeAI(
            model=kwargs.get("model_name", 'gemini-2.0-flash-exp'),
            temperature=kwargs.get("temperature", 0.0),
            google_api_key=kwargs.get("api_key", None),
        )
    elif provider == "azure_openai":
        return AzureChatOpenAI(
            model=kwargs.get("model_name", 'gpt-4o'),
            temperature=kwargs.get("temperature", 0.0),
            api_version="2024-05-01-preview",
            azure_endpoint=kwargs.get("base_url", ""),
            api_key=kwargs.get("api_key", None)
        )
    else:
        raise ValueError(f'Unsupported provider: {provider}')


def encode_image(img_path):
    if not img_path:
        return None
    with open(img_path, "rb") as fin:
        image_data = base64.b64encode(fin.read()).decode("utf-8")
    return image_data
