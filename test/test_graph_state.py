"""
Test cases. Google Search tool
"""
import os
import uuid

import pytest
from langgraph.graph.state import CompiledStateGraph
from backend.graphs.graph_state import build_recipe_chatbot_graph
from backend.tools.google_search import SerpAPIClient
from backend.tools.openai import OpenAIClient


@pytest.mark.parametrize(
    "query",
    [
        "How can I cook a hamburger?",
        "How can I cook a Krabby Patty?",
        "What is the current temperature?",
        "Hi, Hey",
    ]
)
def test_build_recipe_chatbot_graph(query):
    openai_api_key = os.getenv("OPENAI_API_KEY")
    OpenAIClient(api_key=openai_api_key)

    serpapi_api_key = os.getenv("SERPAPI_API_KEY")
    SerpAPIClient(api_key=serpapi_api_key)

    graph: CompiledStateGraph = build_recipe_chatbot_graph()

    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    response = ''
    for output in graph.stream(
            {"query": query}, config=config, stream_mode="updates"
    ):
        last_message_data = next(iter(output.values()))
        if 'recipe' in last_message_data.keys():
            response = last_message_data['recipe']

        if 'politely_response' in last_message_data.keys():
            response = last_message_data['politely_response']

    print(response)

