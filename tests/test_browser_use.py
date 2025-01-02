# -*- coding: utf-8 -*-
# @Time    : 2025/1/2
# @Author  : wenshao
# @ProjectName: browser-use-webui
# @FileName: test_browser_use.py
from dotenv import load_dotenv

load_dotenv()

import os
import sys
from pprint import pprint

import asyncio
from browser_use import Agent
from browser_use.agent.views import AgentHistoryList

from src.utils import utils


async def test_browser_use_org():
    from browser_use.browser.browser import Browser, BrowserConfig
    from browser_use.browser.context import (
        BrowserContext,
        BrowserContextConfig,
        BrowserContextWindowSize,
    )
    llm = utils.get_llm_model(
        provider="azure_openai",
        model_name="gpt-4o",
        temperature=0.8,
        base_url=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
        api_key=os.getenv("AZURE_OPENAI_API_KEY", "")
    )

    window_w, window_h = 1920, 1080

    browser = Browser(
        config=BrowserConfig(
            headless=False,
            disable_security=True,
            extra_chromium_args=[f'--window-size={window_w},{window_h}'],
        )
    )
    async with await browser.new_context(
            config=BrowserContextConfig(
                trace_path='./tmp/traces',
                save_recording_path="./tmp/record_videos",
                no_viewport=False,
                browser_window_size=BrowserContextWindowSize(width=window_w, height=window_h),
            )
    ) as browser_context:
        agent = Agent(
            task="go to google.com and type 'OpenAI' click search and give me the first url",
            llm=llm,
            browser_context=browser_context,
        )
        history: AgentHistoryList = await agent.run(max_steps=10)

        print('Final Result:')
        pprint(history.final_result(), indent=4)

        print('\nErrors:')
        pprint(history.errors(), indent=4)

        # e.g. xPaths the model clicked on
        print('\nModel Outputs:')
        pprint(history.model_actions(), indent=4)

        print('\nThoughts:')
        pprint(history.model_thoughts(), indent=4)
    # close browser
    await browser.close()


async def test_browser_use_custom():
    from src.browser.custom_browser import CustomBrowser, BrowserConfig
    from src.browser.custom_context import BrowserContext, BrowserContextConfig
    from src.controller.custom_controller import CustomController

    from browser_use.browser.context import BrowserContextWindowSize

    window_w, window_h = 1920, 1080

    # llm = utils.get_llm_model(
    #     provider="azure_openai",
    #     model_name="gpt-4o",
    #     temperature=0.8,
    #     base_url=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
    #     api_key=os.getenv("AZURE_OPENAI_API_KEY", "")
    # )

    llm = utils.get_llm_model(
        provider="gemini",
        model_name="gemini-2.0-flash-exp",
        temperature=0.8,
        api_key=os.getenv("GOOGLE_API_KEY", "")
    )

    browser = CustomBrowser(
        config=BrowserConfig(
            headless=False,
            disable_security=True,
            extra_chromium_args=[f'--window-size={window_w},{window_h}'],
        )
    )
    controller = CustomController()

    async with await browser.new_context(
            config=BrowserContextConfig(
                trace_path='./tmp/traces',
                save_recording_path="./tmp/record_videos",
                no_viewport=False,
                browser_window_size=BrowserContextWindowSize(width=window_w, height=window_h),
            )
    ) as browser_context:
        agent = Agent(
            task="go to google.com and type 'OpenAI' click search and give me the first url",
            llm=llm,
            browser_context=browser_context,
            controller=controller,
        )
        history: AgentHistoryList = await agent.run(max_steps=10)

        print('Final Result:')
        pprint(history.final_result(), indent=4)

        print('\nErrors:')
        pprint(history.errors(), indent=4)

        # e.g. xPaths the model clicked on
        print('\nModel Outputs:')
        pprint(history.model_actions(), indent=4)

        print('\nThoughts:')
        pprint(history.model_thoughts(), indent=4)
    # close browser
    await browser.close()


if __name__ == '__main__':
    # asyncio.run(test_browser_use_org())
    asyncio.run(test_browser_use_custom())
