import streamlit as st
import os
import string
import requests
import random
from streamlit_theme import st_theme

DEEPINFRA_TOKEN = os.getenv("DEEPINFRA_TOKEN", st.secrets["llama_api_key"])

url = "https://api.deepinfra.com/v1/openai/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {DEEPINFRA_TOKEN}"
}

# generate a 10 characters ID of pattern:
#   0     1     2     3     4     5     6     7     8     9
# [0-9] [0-9] [A-Z] [A-Z] [A-Z] [0-9] [0-9] [A-Z] [0-9] [A-Z]
def get_survey_id():
    survey_id = ''
    survey_id = survey_id + str(random.randint(0, 9))
    survey_id = survey_id + str(random.randint(0, 9))
    survey_id = survey_id + random.choice(string.ascii_letters)
    survey_id = survey_id + random.choice(string.ascii_letters)
    survey_id = survey_id + random.choice(string.ascii_letters)
    survey_id = survey_id + str(random.randint(0, 9))
    survey_id = survey_id + str(random.randint(0, 9))
    survey_id = survey_id + random.choice(string.ascii_letters)
    survey_id = survey_id + str(random.randint(0, 9))
    survey_id = survey_id + random.choice(string.ascii_letters)
    return survey_id


# set up the state of this streamlit app session
def session_setup():
    if get_session_state('chat_history') is None:
        set_session_state('chat_history', [])

    if get_session_state('reaction_history') is None:
        set_session_state('reaction_history', [])

    if get_session_state('response_count') is None:
        set_session_state('response_count', 0)

    if get_session_state('next_page') is None:
        set_session_state('next_page', False)

    if get_session_state('current_page') is None:
        set_session_state('current_page', 'chat')

    if get_session_state('current_theme') is None:
        set_session_state('current_theme', st_theme()['base'])

    if get_session_state('background_color_user') is None:
        if get_session_state('current_theme') == 'dark':
            set_session_state('background_color_user', '#027148')
        else:
            set_session_state('background_color_user', '#dcf8c6')

    if get_session_state('background_color_bot') is None:
        if get_session_state('current_theme') == 'dark':
            set_session_state('background_color_bot', '#434343')
        else:
            set_session_state('background_color_bot', '#f1f0f0')

    if get_session_state('survey_id') is None:
        set_session_state('survey_id', get_survey_id())

    if get_session_state('survey_finished') is None:
        set_session_state('survey_finished', False)

    if get_session_state('submitted_to_database') is None:
        set_session_state('submitted_to_database', False)

    if get_session_state('system_instruction') is None:
        set_session_state('system_instruction', os.getenv('gen_system_instruction'))

    if get_session_state('shorter_system_instruction') is None:
        set_session_state('shorter_system_instruction', os.getenv('shorter_system_instruction'))

    if get_session_state('introduction') is None:
        if os.getenv('intro_system_instruction') == '':
            set_session_state('introduction', os.getenv('intro_text'))
        else:
            with st.spinner(os.getenv('intro_wait')):
                set_session_state('introduction', intro_response())

    if get_session_state('next_page') is None:
        set_session_state('next_page', False)

    if get_session_state('submitted_input') is None:
        set_session_state('submitted_input', False)

        if get_session_state('intro_reaction') is None:
            set_session_state('intro_reaction', None)

    if get_session_state('user_input') is None:
        set_session_state('user_input', None)

    if get_session_state('stream_text') is None:
        set_session_state('stream_text', '')

    if get_session_state('streaming') is None:
        set_session_state('streaming', False)

    if get_session_state('done_pressed') is None:
        set_session_state('done_pressed', False)

    if get_session_state('response_placeholder') is None:
        set_session_state('response_placeholder', st.empty())


# save chat history
def modify_chat_history(user_input, response, system_instruction):
    chat_history = get_session_state('chat_history')
    chat_history.append({
        'user_input': user_input,
        'system_instruction': system_instruction,
        'response': response
    })
    set_session_state('chat_history', chat_history)


# get session state value at key
def get_session_state(key):
    if key in st.session_state:
        return st.session_state[key]
    else:
        return None


# set session state value at key
def set_session_state(key, value):
    st.session_state[key] = value


# generate introduction
def intro_response():
    data = {
        "model": "meta-llama/Meta-Llama-3.1-70B-Instruct",
        "messages": [
            {
                "role": "system",
                "content": os.getenv("intro_system_instruction")
            },
            {
                "role": "user",
                "content": os.getenv("intro_text") + " " + st.session_state['system_instruction']
            }
        ],
        "temperature": 0.7,
        "top_p": 0.9,
        "repetition_penalty": 1,
        "max_tokens": os.getenv("intro_max_tokens")
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']