from openai import OpenAI
import pdb
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.globals import get_llm_cache
from langchain_core.language_models.base import (
    BaseLanguageModel,
    LangSmithParams,
    LanguageModelInput,
)
from langchain_core.load import dumpd, dumps
from langchain_core.messages import (
    AIMessage,
    SystemMessage,
    AnyMessage,
    BaseMessage,
    BaseMessageChunk,
    HumanMessage,
    convert_to_messages,
    message_chunk_to_message,
)
from langchain_core.outputs import (
    ChatGeneration,
    ChatGenerationChunk,
    ChatResult,
    LLMResult,
    RunInfo,
)
from langchain_core.output_parsers.base import OutputParserLike
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.tools import BaseTool

from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Literal,
    Optional,
    Union,
    cast,
)

class DeepSeekR1ChatOpenAI(ChatOpenAI):
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.client = OpenAI(
            base_url=kwargs.get("base_url"),
            api_key=kwargs.get("api_key")
        ) 
        
    async def ainvoke(
        self,
        input: LanguageModelInput,
        config: Optional[RunnableConfig] = None,
        *,
        stop: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> AIMessage:
        message_history = []
        messages = convert_to_messages(input)
        for message in messages:
            if isinstance(message, SystemMessage):
                message_history.append({"role": "system", "content": str(message.content)})
            elif isinstance(message, AIMessage):
                message_history.append({"role": "assistant", "content": str(message.content)})
            else:
                message_history.append({"role": "user", "content": str(message.content)})
        
        response = await self.client.chat.completions.create(
            model=self.model_name,
            messages=message_history
        )

        content = response.choices[0].message.content
        return AIMessage(content=content)
    
    def invoke(
        self,
        input: LanguageModelInput,
        config: Optional[RunnableConfig] = None,
        *,
        stop: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> AIMessage:
        message_history = []
        messages = convert_to_messages(input)
        for message in messages:
            if isinstance(message, SystemMessage):
                message_history.append({"role": "system", "content": str(message.content)})
            elif isinstance(message, AIMessage):
                message_history.append({"role": "assistant", "content": str(message.content)})
            else:
                message_history.append({"role": "user", "content": str(message.content)})
        
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=message_history
        )

        content = response.choices[0].message.content
        return AIMessage(content=content)

class DeepSeekR1ChatOllama(ChatOllama):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        
    async def ainvoke(
        self,
        input: LanguageModelInput,
        config: Optional[RunnableConfig] = None,
        *,
        stop: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> AIMessage:
        message_history = []
        messages = convert_to_messages(input)
        for message in messages:
            if isinstance(message, SystemMessage):
                message_history.append({"role": "system", "content": str(message.content)})
            elif isinstance(message, AIMessage):
                message_history.append({"role": "assistant", "content": str(message.content)})
            else:
                message_history.append({"role": "user", "content": str(message.content)})
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=message_history
        )

        content = response.choices[0].message.content
        return AIMessage(content=content)
    
    def invoke(
        self,
        input: LanguageModelInput,
        config: Optional[RunnableConfig] = None,
        *,
        stop: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> AIMessage:
        message_history = []
        messages = convert_to_messages(input)
        for message in messages:
            if isinstance(message, SystemMessage):
                message_history.append({"role": "system", "content": str(message.content)})
            elif isinstance(message, AIMessage):
                message_history.append({"role": "assistant", "content": str(message.content)})
            else:
                message_history.append({"role": "user", "content": str(message.content)})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=message_history
        )

        content = response.choices[0].message.content
        return AIMessage(content=content)