"""
Test cases. Kitchen tool
"""
import sqlite3
from backend.tools.kitchen import list_available_cookware


def test_list_available_cookware():
    # connect to SQLite database
    conn = sqlite3.connect('../recipe_chatbot.db')

    # query available cookware
    cookware_items = list_available_cookware(conn)

    # check results is not empty
    assert len(cookware_items)>0
