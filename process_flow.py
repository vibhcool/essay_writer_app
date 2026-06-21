from typing import TypedDict, Annotated
import operator
import os
from functools import partial
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
    plan_node,
    search_node,
    writer_node,
    critic_node,
    ai_search_node,
    content_researcher_node,
    critic_researcher_node 
)

class ProcessFlow:

    def build(self, agent_map):
        self.build_graph(agent_map)
        return self.graph.compile()

    def build_graph(self, agent_map):
        self.graph = StateGraph(AgentState)

        self.graph.add_node("PLANNER", partial(plan_node, llm=agent_map.get('PLANNER')))
        self.graph.add_node("CONTENT_RESEARCHER", partial(content_researcher_node, llm=agent_map.get('CONTENT_RESEARCHER')))
        self.graph.add_node("SEARCH_INTERNET", search_node)
        
        self.graph.add_node("WRITE", partial(writer_node, llm=agent_map.get('WRITER')))
        
        self.graph.add_node("CRITIC", partial(critic_node, llm=agent_map.get('CRITIC')))
        self.graph.add_node("CRITIC_RESEARCHER", partial(critic_researcher_node, llm=agent_map.get('CRITIC_RESEARCHER')))
        self.graph.add_node("CRITIC_SEARCH_INTERNET", ai_search_node)
        # self.graph.add_node("END", END)

        self.graph.set_entry_point("PLANNER")

        self.graph.add_conditional_edges(
            "CRITIC",
            self.is_essay_valid,
            {
                "CRITIC_RESEARCHER": "CRITIC_RESEARCHER",
                "END": END
            }
        )

        self.graph.add_edge(
            "PLANNER",
            "CONTENT_RESEARCHER"
        )
        
        self.graph.add_edge(
            "CONTENT_RESEARCHER",
            "SEARCH_INTERNET"
        )

        self.graph.add_edge(
            "SEARCH_INTERNET",
            "WRITE"
        )

        self.graph.add_edge(
            "WRITE",
            "CRITIC"
        )

        self.graph.add_edge(
            "CRITIC_RESEARCHER",
            "CRITIC_SEARCH_INTERNET"
        )
        self.graph.add_edge(
            "CRITIC_SEARCH_INTERNET",
            "WRITE"
        )

    def is_essay_valid(self, state: AgentState):
        last_message = state["messages"][-1]

        tool_calls = getattr(last_message, "tool_calls", None)
        if not tool_calls:
            return "END"

        tool_name = last_message.tool_calls[0]["name"]
        print("is_essay_valid\t\t\t", state["messages"])
        if tool_name == "CRITIC_SEARCH_INTERNET":
            return "CRITIC_SEARCH_INTERNET"
        return "END"

