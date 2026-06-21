from typing import TypedDict, Annotated
import operator
import os
from langgraph.graph import StateGraph, END

from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    ToolMessage,
    SystemMessage
)

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

import requests

class Agent:

    client = None
    default_prompt = ''

    def __init__(self, default_prompt: str, tools = None):
        self.init()
        self.default_prompt = default_prompt
        if tools is not None:
            self.client = self.client.bind_tools(tools)

    def init(self):
        self.client = ChatOpenAI(
            model="anthropic/claude-sonnet-4.6",
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL")
        )
    
    def get_init_message(self):
        return SystemMessage(self.default_prompt)

    def invoke(self, message_list):
        message_list[-1] = HumanMessage(content=self.default_prompt + '\n\n' + message_list[-1].content)
        return self.client.invoke([
                    self.get_init_message()
                ] + message_list
        )