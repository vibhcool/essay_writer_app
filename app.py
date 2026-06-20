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


# -----------------------------------------
# Tools
# -----------------------------------------

@tool
def search(query: str):
    """Search the internet"""
    return f"Search result for: {query}"


@tool
def calculator(expression: str):
    """Evaluate arithmetic expression"""
    return str(eval(expression))

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


tools = [calculator, is_api_valid]


# -----------------------------------------
# State
# -----------------------------------------

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]


# -----------------------------------------
# LLM
# -----------------------------------------

client = ChatOpenAI(
    model="anthropic/claude-sonnet-4.6",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

llm = client.bind_tools(tools)


# -----------------------------------------
# LLM Node
# -----------------------------------------

def llm_node(state: AgentState):

    response = llm.invoke(
        state["messages"]
    )
    print("llm_node\t\t\t", state["messages"])
    return {
        "messages": [response]
    }


# -----------------------------------------
# Router
# -----------------------------------------

def route_by_tool(state: AgentState):

    last_message = state["messages"][-1]

    # No tool requested
    if not last_message.tool_calls:
        return "end"

    tool_name = last_message.tool_calls[0]["name"]
    print("route_by_tool\t\t\t", state["messages"])
    if tool_name == "calculator":
        return "calculator"
    elif tool_name == "is_api_valid":
        return "is_api_valid"
    return "end"

def route_for_search(state: AgentState):

    last_message = state["messages"][-1]

    # No tool requested
    print("route_for_search\t\t\t", state["messages"])
    if last_message.content == 'False':
        return "end"
    else:
        return "search"



# -----------------------------------------
# Search Node
# -----------------------------------------

def search_node(state: AgentState):

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


# -----------------------------------------
# Calculator Node
# -----------------------------------------

def calculator_node(state: AgentState):

    tool_call = state["messages"][-1].tool_calls[0]

    result = calculator.invoke(
        tool_call["args"]
    )
    print("calculator_node\t\t\t", state["messages"])
    return {
        "messages": [
            ToolMessage(
                content=result,
                tool_call_id=tool_call["id"]
            )
        ]
    }

def is_api_valid_node(state: AgentState):

    tool_call = state["messages"][-1].tool_calls[0]

    result = is_api_valid.invoke(
        tool_call["args"]
    )
    print("is_api_valid_node\t\t\t", state["messages"])
    return {
        "messages": [
            ToolMessage(
                content=result,
                tool_call_id=tool_call["id"]
            )
        ]
    }


# -----------------------------------------
# Graph
# -----------------------------------------

graph = StateGraph(AgentState)

graph.add_node("llm", llm_node)

graph.add_node(
    "search",
    search_node
)

graph.add_node(
    "calculator",
    calculator_node
)

graph.add_node(
    "is_api_valid",
    is_api_valid_node
)

graph.set_entry_point("llm")

graph.add_conditional_edges(
    "llm",
    route_by_tool,
    {
        "calculator": "calculator",
        "is_api_valid": "is_api_valid",
        "end": END
    }
)

graph.add_edge(
    "search",
    "llm"
)

graph.add_edge(
    "calculator",
    "llm"
)

graph.add_conditional_edges(
    "is_api_valid",
    route_for_search,
    {
        "search": "search",
        "end": END
    }
)


def calculate(query: str):
    result = app.invoke(
        {
            "messages": [
                HumanMessage(
                    content = query
                )
            ]
        }
    )
    print('final messages list\t\t', result)
    print(
        'result', result["messages"][-1].content
    )


def search_results(message: str):
    result = app.invoke(
        {
            "messages": [
                HumanMessage(
                    content = message
                )
            ]
        }
    )
    print('search final messages list\t\t', result)
    print(
        'result', result["messages"][-1].content
    )

def is_valid_url(url_message: str):
    result = app.invoke(
        {
            "messages": [
                HumanMessage(
                    content = url_message
                )
            ]
        }
    )
    print('url final messages list\t\t', result)
    print(
        'result', result["messages"][-1].content
    )

app = graph.compile()

class EssayWriter:

    def write(title: str, words = 500: int, hint_list = []: list<str>):
        essay_writer_agent = build_graph()
        essay_writer_graph.compile()

if '__main__' == __name__:
    title = 'LLM: boon or bane'
    hint_list = ['Alan Turing', 'Anthropic', 'Deepseek', 'Job cuts by Tech companies']
    essay_writer = EssayWriter().write(title, words = 1000, hints = hint_list)
