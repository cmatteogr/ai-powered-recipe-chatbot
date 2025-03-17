"""
Graph state
"""
# import libraries
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, END
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph

from backend.graphs.nodes import State, query_classification, non_relevant, research, response_decision
from backend.tools.openai import OpenAIClient


def build_recipe_chatbot_graph() -> CompiledStateGraph:
    """
    Constructs and compiles a state graph for a recipe chatbot.

    The graph consists of nodes that classify user queries, determine relevance,
    conduct research, and decide on responses. Conditional edges define the logic
    for transitioning between states based on input data.

    :return: CompiledStateGraph
    """
    print("Constructing state graph")
    # init memory saver to keep query processing progress
    memory = MemorySaver()
    # init graph workflow
    graph_workflow = StateGraph(State)

    print("Adding graph nodes")
    # Add nodes representing different stages of chatbot processing
    graph_workflow.add_node("query_classification_node", query_classification)
    graph_workflow.add_node("non_relevant_node", non_relevant)
    graph_workflow.add_node("research_node", research)
    graph_workflow.add_node("response_decision_node", response_decision)

    # define edge conditions
    def is_cooking_related_condition(state: State):
        """
        Determines whether the user query is related to cooking.
        :param state: The current state containing user query information.
        :return: 'yes' if cooking-related, 'no' otherwise.
        """
        is_cooking_related = state.get("is_cooking_related")
        # check if response is 'yes' or 'no'
        if is_cooking_related != 'yes' and is_cooking_related != 'no':
            raise Exception("'is_cooking_related' should be 'yes' or 'no'")
        # return yes or no
        return is_cooking_related

    def is_research_enough_condition(state: State):
        """
        Determines if the research conducted provides a sufficient answer.
        :param state: The current state containing research results.
        :return: 'yes' if the research is sufficient, 'no' otherwise.
        """
        recipe = state.get("recipe")
        query = state.get("query")
        # query in the research was good enough
        open_ai_client = OpenAIClient()
        system_content = f"Evaluate if the recipe provided by the user is good enough to explain how to cook '{query}', just reply (yes/no):"
        response = open_ai_client.query_to_chatgpt(system_content=system_content, user_content=recipe)

        # format answer
        return 'yes' if 'yes' in response.lower() else 'no'

    print("Adding graph edges")
    # add the edges
    graph_workflow.add_edge(START, 'query_classification_node')
    graph_workflow.add_conditional_edges('query_classification_node', is_cooking_related_condition,
                                         {'yes': 'research_node', 'no': 'non_relevant_node'})
    graph_workflow.add_edge('non_relevant_node', END)
    graph_workflow.add_edge('research_node', 'response_decision_node')
    graph_workflow.add_conditional_edges('response_decision_node', is_research_enough_condition,
                                         {'yes': END, 'no': 'research_node'})

    # compile graph
    print("Compiling state graph")
    graph = graph_workflow.compile(checkpointer=memory)

    print("Plot state graph")
    # plot graph to ensure correct transitions
    image_data = graph.get_graph().draw_mermaid_png()
    with open("graph.png", "wb") as f:
        f.write(image_data)

    # return graph
    return graph
