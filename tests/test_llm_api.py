# -*- coding: utf-8 -*-
# @Time    : 2025/1/1
# @Author  : wenshao
# @Email   : wenshaoguo1026@gmail.com
# @Project : browser-use-webui
# @FileName: test_llm_api.py
import os
import pdb

from dotenv import load_dotenv

load_dotenv()

import sys

sys.path.append(".")


def test_gemini_model():
    # you need to enable your api key first: https://ai.google.dev/palm_docs/oauth_quickstart
    from langchain_core.messages import HumanMessage
    from src.utils import utils

    llm = utils.get_llm_model(
        provider="gemini",
        model_name="gemini-2.0-flash-exp",
        temperature=0.8,
        api_key=os.getenv("GOOGLE_API_KEY", "")
    )

    image_path = "assets/examples/test.png"
    image_data = utils.encode_image(image_path)
    message = HumanMessage(
        content=[
            {"type": "text", "text": "describe this image"},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
            },
        ]
    )
    ai_msg = llm.invoke([message])
    print(ai_msg.content)


def test_azure_openai_model():
    from langchain_core.messages import HumanMessage
    from src.utils import utils

    llm = utils.get_llm_model(
        provider="azure_openai",
        model_name="gpt-4o",
        temperature=0.8,
        base_url=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
        api_key=os.getenv("AZURE_OPENAI_KEY", "")
    )
    image_path = "assets/examples/test.png"
    image_data = utils.encode_image(image_path)
    message = HumanMessage(
        content=[
            {"type": "text", "text": "describe this image"},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
            },
        ]
    )
    ai_msg = llm.invoke([message])
    print(ai_msg.content)


if __name__ == '__main__':
    test_gemini_model()
    # test_azure_openai_model()
