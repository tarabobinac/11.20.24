import streamlit as st
import os
from utils.session import session_setup
from streamlit_theme import st_theme
from utils.components import (show_response_count, finish_button, done_button, show_finish_status,
                              add_reaction_buttons, get_input_and_gen_response, comments)
def setup():
    os.environ['country'] = 'Mexico'
    os.environ['topic'] = 'gun control'

    os.environ['intro_temp'] = '0.7'
    os.environ['intro_top_p'] = '0.9'
    os.environ['intro_rep_pen'] = '1'
    os.environ['intro_max_tokens'] = '512'

    os.environ['intro_system_instruction'] = "Respond with a list of pros and cons on the topic at hand."
    os.environ['intro_text'] = f"""Imagine you are a person from {os.environ['country']} moderating a discussion about {os.environ['topic']}. Based on the cultural values from {os.environ['country']}, provide your communication partner with stances why an average person from {os.environ['country']} would be pro/against {os.environ['topic']}. You should provide information in a casual style in English. Start the conversation with exactly the following prompt: 

    \"Good afternoon. I will be your conversation partner today in a brief discussion about {os.environ['topic']}. This discussion is an opportunity for you to learn about {os.environ['topic']}. I want to encourage you to speak freely. You are not expected to be an expert. Also, no consensus is necessary, you do not need to agree with the stances I provide. My role is to help you learn about how people in {os.environ['country']} perceive the pros and cons of {os.environ['topic']}.\"

    And then provide relevant cultural information in a pros/cons list. 

    Lastly, encourage conversation by ending with \"Please start off by telling us something that puzzles you about this topic.\"
    """

    os.environ['gen_temp'] = '0.7'
    os.environ['gen_top_p'] = '0.9'
    os.environ['gen_rep_pen'] = '1'
    os.environ['gen_max_tokens'] = '512'
    os.environ['gen_system_instruction'] = f"You finish your response within {os.environ['gen_max_tokens']} tokens."


def chat_bubble_css():
    if st.session_state['current_theme'] == "dark":
        background_color_user = "#027148"
        background_color_bot = "#434343"
    else:
        background_color_user = "#dcf8c6"
        background_color_bot = "#f1f0f0"

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
            background-color: {background_color_user};
        }}
        .bot-message {{
            align-self: flex-start;
            background-color: {background_color_bot};
        }}
        </style>
    """, unsafe_allow_html=True)


st.set_page_config(
    layout='wide',
    page_title='AI chatbot',
    page_icon='🤖'
)


def main():
    setup()
    session_setup()
    chat_bubble_css()

    if st.session_state.get('next_page', False):
        st.session_state.current_page = "feedback"  # Set the current page in session state

    current_page = st.session_state.get('current_page', "chat")

    if current_page == "feedback":
        show_feedback_page()
    else:
        show_chat_page()


def show_chat_page():
    st.title('AI chatbot')
    introduction = st.session_state['introduction']
    st.info(introduction)

    # Display chat history
    for i, exchange in enumerate(st.session_state.get('chat_history', [])):
        user_message = exchange['user_input']
        bot_response = exchange['response']

        st.markdown(f"""
            <div class="chat-container">
                <div class="user-message">{user_message}</div>
                <div class="bot-message">{bot_response}</div>
            </div>
        """, unsafe_allow_html=True)

        add_reaction_buttons(i)

    get_input_and_gen_response()
    show_response_count()
    finish_button()
    show_finish_status()


def show_feedback_page():
    st.subheader("Chatbot Responses for Feedback")
    st.write("""
    On this page, you can provide feedback on the chatbot's responses.
    
    Below, you will see a list of input / response pairs from your chat. Your input is in ***green***, while the 
    chatbot's response is in ***gray***.
    
    To the right of a response, you can click **Yes** under **Give feedback?** if you want to provide feedback on that 
    response, or you can click **No** if not. 
    
    If you choose to provide feedback on a response, you can specify the type by choosing from the categories in the 
    dropdown menu. You can choose more than one. Then, fill out the comment box with your thoughts on the response.
    
    You must provide feedback for at least two responses, at which point a **Submit** button will appear at the bottom
    of the page.
    
    Click **Submit** when you are finished, then click **Go to post-survey** to take the post-survey.
    """)

    with st.expander("Click to learn what each category means"):
        st.markdown("""
        - **Balanced / biased towards certain perspective**: ...
        - **Morally + ethically sound / morally + ethically questionable**: ...
        - **Factually incorrect**: ...
        - **Respectful / disrespectful**: ...
        - **Culturally relevant / culturally irrelevant**: ...
        - **Other**: Any other feedback that doesn't fit into the above categories.
        <br><br>
        """, unsafe_allow_html=True)

    comments()
    #done_button()

    if 'done_pressed' in st.session_state and st.session_state['done_pressed']:
        st.success("Comments submitted! Click **Go to post-survey** to start the post-survey.")


if __name__ == '__main__':
    main()
