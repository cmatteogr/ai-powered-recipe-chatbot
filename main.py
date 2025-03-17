import uuid

from fastapi import FastAPI
from langgraph.graph.state import CompiledStateGraph
import os
from backend.graphs.graph_state import build_recipe_chatbot_graph
from backend.models.cooking_models import CookingRequest
from backend.tools.google_search import SerpAPIClient
from backend.tools.openai import OpenAIClient

# init Fast API service
app = FastAPI()

# init arguments
#openai_api_key = "YOUR_KEY"
openai_api_key = os.getenv("OPENAI_API_KEY")
OpenAIClient(api_key=openai_api_key)

#serpapi_api_key = "YOUR_KEY"
serpapi_api_key = os.getenv("SERPAPI_API_KEY")
SerpAPIClient(api_key=serpapi_api_key)

# build graph
graph: CompiledStateGraph = build_recipe_chatbot_graph()


@app.post("/api/cooking")
def create_cooking(request: CookingRequest):
    """
    Creates a new cooking item based on the given recipe details.
    """
    print("user query: {}".format(request))
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    response = ''
    for output in graph.stream(
            {"query": request.user_query}, config=config, stream_mode="updates"
    ):
        last_message_data = next(iter(output.values()))
        # return user response recipe
        if 'recipe' in last_message_data.keys():
            response = last_message_data['recipe']
        # return user response politely response
        if 'politely_response' in last_message_data.keys():
            response = last_message_data['politely_response']

    print("response: {}".format(response))
    return response
