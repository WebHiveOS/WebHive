# -*- coding: utf-8 -*-
# @Time    : 2025/1/2
# @Author  : wenshao
# @ProjectName: browser-use-webui
# @FileName: custom_browser.py

import logging
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContextConfig, BrowserContext
from .custom_context import CustomBrowserContext

logger = logging.getLogger(__name__)

class CustomBrowser(Browser):
    async def new_context(
        self, 
        config: BrowserContextConfig = BrowserContextConfig(),
        context=None
    ) -> BrowserContext:
        """Create a browser context with custom implementation"""
        # First get/create the underlying Playwright browser
        playwright_browser = await self.get_playwright_browser()
        
        return CustomBrowserContext(
            browser=self,  # Pass self instead of playwright browser
            config=config,
            context=context
        )

    async def get_playwright_browser(self):
        """Ensure we have a Playwright browser instance"""
        if not self.playwright_browser:
            await self._init()
        return self.playwright_browser
