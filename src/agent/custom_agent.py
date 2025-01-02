# -*- coding: utf-8 -*-
# @Time    : 2025/1/2
# @Author  : wenshao
# @ProjectName: browser-use-webui
# @FileName: custom_agent.py

import asyncio
import json
import logging
import os
import time
import uuid
from pathlib import Path
from typing import Any, Optional, Type, TypeVar

from dotenv import load_dotenv
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import (
    BaseMessage,
    SystemMessage,
)
from openai import RateLimitError
from pydantic import BaseModel, ValidationError

from browser_use.agent.message_manager.service import MessageManager
from browser_use.agent.prompts import AgentMessagePrompt, SystemPrompt
from browser_use.agent.views import (
    ActionResult,
    AgentError,
    AgentHistory,
    AgentHistoryList,
    AgentOutput,
    AgentStepInfo,
)
from browser_use.telemetry.views import (
    AgentEndTelemetryEvent,
    AgentRunTelemetryEvent,
    AgentStepErrorTelemetryEvent,
)
from browser_use.agent.service import Agent
from browser_use.utils import time_execution_async

from .custom_views import CustomAgentOutput

logger = logging.getLogger(__name__)


class CustomAgent(Agent):

    def _setup_action_models(self) -> None:
        """Setup dynamic action models from controller's registry"""
        # Get the dynamic action model from controller's registry
        self.ActionModel = self.controller.registry.create_action_model()
        # Create output model with the dynamic actions
        self.AgentOutput = CustomAgentOutput.type_with_custom_actions(self.ActionModel)

    def _log_response(self, response: CustomAgentOutput) -> None:
        """Log the model's response"""
        if 'Success' in response.current_state.evaluation_previous_goal:
            emoji = '👍'
        elif 'Failed' in response.current_state.evaluation_previous_goal:
            emoji = '⚠'
        else:
            emoji = '🤷'

        logger.info(f'{emoji} Eval: {response.current_state.evaluation_previous_goal}')
        logger.info(f'🧠 Memory: {response.current_state.memory}')
        logger.info(f'🎯 Next goal: {response.current_state.next_goal}')
        for i, action in enumerate(response.action):
            logger.info(
                f'🛠️  Action {i + 1}/{len(response.action)}: {action.model_dump_json(exclude_unset=True)}'
            )

    @time_execution_async('--step')
    async def step(self, step_info: Optional[AgentStepInfo] = None) -> None:
        """Execute one step of the task"""
        logger.info(f'\n📍 Step {self.n_steps}')
        state = None
        model_output = None
        result: list[ActionResult] = []

        try:
            state = await self.browser_context.get_state(use_vision=self.use_vision)
            self.message_manager.add_state_message(state, self._last_result, step_info)
            input_messages = self.message_manager.get_messages()
            model_output = await self.get_next_action(input_messages)
            self._save_conversation(input_messages, model_output)
            self.message_manager._remove_last_state_message()  # we dont want the whole state in the chat history
            self.message_manager.add_model_output(model_output)

            result: list[ActionResult] = await self.controller.multi_act(
                model_output.action, self.browser_context
            )
            self._last_result = result

            if len(result) > 0 and result[-1].is_done:
                logger.info(f'📄 Result: {result[-1].extracted_content}')

            self.consecutive_failures = 0

        except Exception as e:
            result = self._handle_step_error(e)
            self._last_result = result

        finally:
            if not result:
                return
            for r in result:
                if r.error:
                    self.telemetry.capture(
                        AgentStepErrorTelemetryEvent(
                            agent_id=self.agent_id,
                            error=r.error,
                        )
                    )
            if state:
                self._make_history_item(model_output, state, result)
