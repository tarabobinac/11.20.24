import streamlit as st
import os
from utils.session import session_setup, get_session_state, set_session_state
from utils.pages import show_chat_page, show_feedback_page
from utils.EN_labels import set_labels

# configuration
def setup():
    os.environ['country'] = 'Colombia'
    os.environ['topic'] = 'GMOs'
    os.environ['intro_max_tokens'] = '512'
    os.environ['intro_system_instruction'] = 'Respond with a list of pros and cons on the topic at hand.'
    os.environ['intro_text'] = f"""Imagine you are a person from {os.environ['country']} moderating a discussion about genetically modified organisms ({os.environ['topic']}). Based on the cultural values from {os.environ['country']}, provide your communication partner with stances why an average person from {os.environ['country']} would be pro/against {os.environ['topic']}. You should provide information in a casual style in English. Start the conversation with exactly the following prompt: 

\"Good afternoon. I will be your conversation partner today in a brief discussion about genetically modified organisms ({os.environ['topic']}). This discussion is an opportunity for you to learn about {os.environ['topic']} in {os.environ['country']}. I want to encourage you to speak freely. You are not expected to be an expert. Also, no consensus is necessary, you do not need to agree with the stances I provide. My role is to help you learn about how people in {os.environ['country']} perceive the pros and cons of {os.environ['topic']}.\"

And then provide relevant cultural information in a pros/cons list. 

Lastly, encourage conversation by ending with \"Please start off by telling us something that puzzles you about this topic.\"
"""
    os.environ['gen_max_tokens'] = '512'
    os.environ['gen_system_instruction'] = (f"""You finish your response within {os.environ['gen_max_tokens']} tokens.
                                            Avoid asking \"yes\"/\"no\" questions.""")
    os.environ['shorter_system_instruction'] = (f"""You provide shorter, more conversational responses. 
                                            Avoid asking \"yes\"/\"no\" questions.""")

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
