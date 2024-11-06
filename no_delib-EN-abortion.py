import streamlit as st
import os
from utils.session import session_setup, get_session_state, set_session_state
from utils.pages import show_chat_page, show_feedback_page
from utils.EN_labels import set_labels

# configuration
def setup():
    os.environ['topic'] = 'abortion'

    os.environ['intro_max_tokens'] = '512'
    os.environ['intro_system_instruction'] = ''
    os.environ['intro_text'] = f"""Let’s talk about {os.environ['topic']}! Start off by telling me something that puzzles you about {os.environ['topic']}."""

    os.environ['gen_max_tokens'] = '512'
    os.environ['gen_system_instruction'] = (f"""Engage in opinionated conversation on {os.environ['topic']}. You finish your response 
                                            within {os.environ['gen_max_tokens']} tokens. Avoid asking \"yes\"/\"no\" 
                                            questions.""")
    os.environ['shorter_system_instruction'] = (f"""Engage in opinionated conversation on {os.environ['topic']}. You provide shorter, 
                                            more conversational responses. Avoid asking \"yes\"/\"no\" questions.""")

# style
def chat_bubble_css():
    st.markdown(f"""
        <style>
        .chat-container {{
            display: flex;
            flex-direction: column;
            margin-bottom: 10px;
        }}
        .user-message, .bot-message {{
            padding: 10px;
            border-radius: 15px;
            max-width: 60%;
            margin: 5px;
            position: relative;
            margin-top: 15px;  /* Staggered positioning for each message */
        }}
        .user-message {{
            align-self: flex-end;
            background-color: {get_session_state('background_color_user')};
        }}
        .bot-message {{
            align-self: flex-start;
            background-color: {get_session_state('background_color_bot')};
        }}
        </style>
    """, unsafe_allow_html=True)


st.set_page_config(
    layout='wide',
    page_title=os.getenv('chatbot'),
    page_icon='🤖'
)


# start session and display chat or response page
def main():
    set_labels()
    setup()
    session_setup()
    chat_bubble_css()

    if st.session_state.get('next_page', False):
        set_session_state('current_page', 'feedback')

    current_page = st.session_state.get('current_page', "chat")

    if current_page == "feedback":
        show_feedback_page()
    else:
        show_chat_page()


if __name__ == '__main__':
    main()
