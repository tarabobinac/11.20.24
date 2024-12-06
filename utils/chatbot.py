
import streamlit as st
from utils.session import set_session_state, get_session_state
import requests
import os
import json

maximum_responses = 15

DEEPINFRA_TOKEN = os.getenv('DEEPINFRA_TOKEN', st.secrets['llama_api_key'])

url = 'https://api.deepinfra.com/v1/openai/chat/completions'
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {DEEPINFRA_TOKEN}'
}


# communicate with API for stream response
def request_response(user_input, system_instruction, callback):
    if os.getenv('intro_system_instruction') == '':
        messages = [{'role': 'assistant', 'content': get_session_state('introduction')}]
    else:
        messages = [{'role': 'system', 'content': os.getenv('intro_system_instruction')},
                    {'role': 'user', 'content': os.getenv('intro_text')},
                    {'role': 'assistant', 'content': get_session_state('introduction')}]

    chat_history = get_session_state('chat_history')
    for IO_pair in chat_history:
        messages.extend(
            [
                {
                    'role': 'system',
                    'content': IO_pair['system_instruction'],
                },
                {
                    'role': 'user',
                    'content': IO_pair['user_input'],
                },
                {
                    'role': 'assistant',
                    'content': IO_pair['response']
                }
            ]
        )

    messages.extend(
        [
            {
                'role': 'system',
                'content': system_instruction,
            },
            {
                'role': 'user',
                'content': user_input + ' ' + get_session_state('system_instruction'),
            }
        ]
    )

    if os.getenv('country') == '':
        temperature = 0.7
        repetition_penalty = 1
    else:
        temperature = 0.8
        repetition_penalty = 1.2
    
    data = {
        'model': 'meta-llama/Meta-Llama-3.1-70B-Instruct',
        'messages': messages,
        'temperature': temperature,
        'stream': 'true',
        'top_p': 0.9,
        'repetition_penalty': repetition_penalty,
        'max_tokens': os.getenv('gen_max_tokens')
    }

    response = requests.post(url, headers=headers, json=data, stream=True)
    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8').strip()

            if decoded_line == '[DONE]':
                break

            try:
                parsed_data = json.loads(decoded_line.strip('data: '))
            except json.JSONDecodeError:
                continue

            if 'choices' in parsed_data and parsed_data['choices']:
                stop = parsed_data['choices'][0].get('finish_reason')
                if stop is None:
                    text = parsed_data['choices'][0]['delta'].get('content', '')
                    if text:
                        callback(text)
                else:
                    callback(None)
                    break

# filter input before requesting from API
def get_response(user_input, system_instruction, callback):
    if get_session_state('response_count') >= maximum_responses:
        return None

    if get_session_state('survey_finished'):
        return None

    request_response(user_input, system_instruction, callback)
