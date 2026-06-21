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

def plan_node(state: AgentState, llm):
    print("plan_node starts")
    response = llm.invoke(
        state["messages"]
    )
    print("plan_node\t\t\t", state["messages"])
    print("response\t\t\t", response)
    return {
        "messages": [response]
    }

def content_researcher_node(state: AgentState, llm):
    print("content_researcher_node starts")
    response = llm.invoke(
        state["messages"]
    )
    print("content_researcher_node\t\t", state["messages"])
    print("response\t\t\t", response)
    return {
        "messages": [response]
    }

def search_node(state: AgentState):
    print("search_node starts")
    tool_call = state["messages"][-1].tool_calls[0]

    result = search.invoke(
        tool_call["args"]
    )
    print("search_node\t\t\t", state["messages"])
    return {
        "messages": [
            ToolMessage(
                content=result,
                tool_call_id=tool_call["id"]
            )
        ]
    }

def writer_node(state: AgentState, llm):
    print("writer_node starts")
    response = llm.invoke(
        state["messages"]
    )
    print("writer_node\t\t\t", state["messages"])
    print("response\t\t\t", response)
    return {
        "messages": [response]
    }

def critic_researcher_node(state: AgentState, llm):
    print("critic_researcher_node starts")
    response = llm.invoke(
        state["messages"]
    )
    print("critic_researcher_node\t\t", state["messages"])
    print("response\t\t\t", response)
    return {
        "messages": [response]
    }

def critic_node(state: AgentState, llm):
    print("critic_node starts")
    response = llm.invoke(
        state["messages"]
    )
    print("critic_node\t\t\t", state["messages"])
    print("response\t\t\t", response)
    return {
        "messages": [response]
    }

def ai_search_node(state: AgentState):
    print("ai_search starts")
    tool_call = state["messages"][-1].tool_calls[0]
    result = ai_search.invoke(
        tool_call["args"]
    )
    print("ai_search\t\t\t", state["messages"])
    return {
        "messages": [
            ToolMessage(
                content=result,
                tool_call_id=tool_call["id"]
            )
        ]
    }

# def is_api_valid_node(state: AgentState):

#     tool_call = state["messages"][-1].tool_calls[0]

#     result = is_api_valid.invoke(
#         tool_call["args"]
#     )
#     print("is_api_valid_node\t\t\t", state["messages"])
#     return {
#         "messages": [
#             ToolMessage(
#                 content=result,
#                 tool_call_id=tool_call["id"]
#             )
#         ]
#     }

@tool
def search(query: str):
    """Search the internet"""
    return f"Search result for: {query}"

@tool
def ai_search(query: str):
    """AI-based search internet"""
    return f"Search result for: {query}"

@tool
def is_api_valid(url_str: str):
    """Check whether a URL returns a successful HTTP response."""
    # import pdb; pdb.set_trace()
    try:
        response = requests.get(url_str)
        status_code = response.status_code
    except:
        return 'False'
    if (status_code >= 200 and status_code < 300):
        return 'True'
    else:
        return 'False'