"""
Test cases. Google Search tool
"""
import os
import pytest

from backend.tools.google_search import SerpAPIClient


@pytest.mark.parametrize(
    "query",
    [
        "How can I cook a hamburger?",
        "How can I cook a Krabby Patty?",
        "What is the current temperature?",
        "Hi, Hey",
    ]
)
def test_search_by_query(query):
    # get serp API from environment variables
    serpapi_api_key = os.getenv("SERPAPI_API_KEY")
    serp_api_client = SerpAPIClient(api_key=serpapi_api_key)
    # search using Google Search
    results_search = serp_api_client.search_by_query(query=query)

    # check results is not empty
    assert results_search is not None

    # print results
    for idx, result in enumerate(results_search.get("organic_results", []), start=1):
        print(f"{idx}. {result.get('title')}")
        print(f"   Link: {result.get('link')}")
        print(f"   Snippet: {result.get('snippet')}\n")
