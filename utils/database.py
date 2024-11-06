from pymongo import MongoClient
import streamlit as st
import os

from utils.session import get_session_state


# MongoDB Setup
def get_mongo_client():
    mongo_uri = st.secrets["mongo_uri"]
    client = MongoClient(mongo_uri)
    return client

# Insert data function
def insert_data_to_db(data):
    client = get_mongo_client()
    db = client['latinx-nlp']  # Replace with your database name
    collection = db['user_data']  # Replace with your collection name
    collection.insert_one(data)
    client.close()

# Submission handler
def handle_submission():
    data = {
        "id": get_session_state('respondent_id'),
        "system_instruction": get_session_state("system_instruction"),
        "shorter_system_instruction": get_session_state("shorter_system_instruction"),
        "introduction": get_session_state('introduction'),
        "intro_reaction": get_session_state('intro_reaction'),
        "chat_history": get_session_state("chat_history"),
        "reaction_history": get_session_state("reaction_history"),
        "comments": get_session_state("comments")
    }
    insert_data_to_db(data)
