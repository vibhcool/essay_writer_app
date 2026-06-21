from typing import TypedDict, Annotated, List
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

from process_flow import ProcessFlow
from agent_manager import AgentManager

class EssayWriter:


    def __init__(self):
        agent_map = AgentManager().init_agents()
        self.app = self.build_flow(agent_map)

    def write(self, title: str, words: int = 500, hint_list: List[str] | None = []):
        result = self.app.invoke(
            {
                "messages": [
                    HumanMessage(
                        content = 'title: ' + title + ' , max word count: ' + str(words)
                                + ' . Use following hints which are as follows: ' + ','.join(hint_list)
                    )
                ]
            }
        )
        return result

    def build_flow(self, agent_map):
        self.process_flow = ProcessFlow()
        return self.process_flow.build(agent_map)

    @tool
    def search_internet(query: str):
        """Search the internet"""
        return f"Search result for: {query}"

    @tool
    def search_ai_internet(expression: str):
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
        

if '__main__' == __name__:
    title = 'LLM: boon or bane'
    hint_list = ['Alan Turing', 'Anthropic', 'Deepseek', 'Job cuts by Tech companies']
    essay_writer = EssayWriter()
    result = essay_writer.write(title, words = 1000, hint_list = hint_list)
    print('\nRESULT:\n\n')
    print(result['messages'][-1])
    '''
                                               |------------------------|
                                               V                        |
        PLAN -> SEARCH INTERNET -> WRITE -> CRITIC -> [IS FINE?] -> SEARCH INTERNET
                                                          |                        
                                                          |-------> END
    '''