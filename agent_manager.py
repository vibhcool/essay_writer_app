from typing import TypedDict, Annotated
import operator
import os
from langgraph.graph import StateGraph, END

from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    ToolMessage
)
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
import requests

from agent_state import AgentState

from nodes_manager import (
    search,
    ai_search
)
from agents import (
    Planner,
    Writer,
    Critic,
    CriticResearcher,
    ContentResearcher
)

class AgentManager:

    LLM_AGENT_MAP = {}

    def init_agents(self):
        self.LLM_AGENT_MAP['PLANNER'] = Planner()
        
        writer_tools = [search]
        self.LLM_AGENT_MAP['CONTENT_RESEARCHER'] = ContentResearcher(tools = writer_tools)
        self.LLM_AGENT_MAP['CONTENT_RESEARCHER']

        self.LLM_AGENT_MAP['WRITER'] = Writer()
        
        self.LLM_AGENT_MAP['CRITIC'] = Critic()
        
        critic_tools = [ai_search]
        self.LLM_AGENT_MAP['CRITIC_RESEARCHER'] = CriticResearcher(tools = critic_tools)
        self.LLM_AGENT_MAP['CRITIC_RESEARCHER']

        return self.LLM_AGENT_MAP
