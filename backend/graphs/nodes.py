"""

"""
from typing import TypedDict, Optional

from backend.tools.google_search import SerpAPIClient
from backend.tools.openai import OpenAIClient


class State(TypedDict):
    """
    Defines the structure of the chatbot state.
    """
    query: Optional[str]
    is_cooking_related: Optional[bool]
    is_researching_enough: Optional[bool]
    results_search_recipe: Optional[str]
    recipe: Optional[str]
    politely_response: Optional[str]


def query_classification(state: State):
    """
    Classifies whether the user's query is related to cooking.
    :param state: The chatbot's current state containing the query.
    :return: Updated state with the classification result.
    """
    print("query classification state")
    query = state.get("query")
    open_ai_client = OpenAIClient()
    # classify query
    system_content = "Classify if the following question is cooking-related (yes/no):"
    response = open_ai_client.query_to_chatgpt(system_content=system_content, user_content=query)
    # set is cooking query related
    state["is_cooking_related"] = 'yes' if 'yes' in response.lower() else 'no'
    return state


def non_relevant(state: State):
    """
    Handles non-relevant queries by generating a polite response.
    :param state: The chatbot's current state containing the query.
    :return: Updated state with the classification result.
    """
    print("non relevant state")
    # get input request
    query = state.get("query")
    open_ai_client = OpenAIClient()
    system_content = f"Politely but clearly explain that you only answer cooking-related queries, the query provided '{query}' is not cooking-related"
    response = open_ai_client.query_to_chatgpt(system_content=system_content, user_content=query)
    state["politely_response"] = response
    return state


def research(state: State):
    """
    Conducts research using an external search API to find cooking-related information.
    :param state: The chatbot's current state containing the query.
    :return: Updated state with the classification result.
    """
    print("research state")
    # get input request
    query = state.get("query")
    serp_api_client = SerpAPIClient()
    # search using Google Search
    results_search = serp_api_client.search_by_query(query=query)
    state["results_search_recipe"] = str(results_search['organic_results'][:3])
    return state


def response_decision(state: State):
    """
    Constructs and compiles a state graph for a recipe chatbot.
    :param state: The chatbot's current state containing the query.
    :return: Updated state with the classification result.
    """
    print("response state")
    # get input request
    results_search_recipe = state.get("results_search_recipe")
    query = state.get("query")
    # use the following
    open_ai_client = OpenAIClient()
    system_content = f"Generate if it is possible a cooking recipe given the user content for the following query '{query}':"
    response = open_ai_client.query_to_chatgpt(system_content=system_content, user_content=results_search_recipe)
    state['recipe'] = response
    return state
