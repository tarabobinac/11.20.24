import streamlit as st
import os
from utils.session import session_setup, get_session_state, set_session_state
from utils.pages import show_chat_page, show_feedback_page


# configuration
def setup():
    os.environ['country'] = 'Brazil'
    os.environ['topic'] = 'the death penalty'

    os.environ['intro_max_tokens'] = '512'
    os.environ['intro_system_instruction'] = 'Respond with a list of pros and cons on the topic at hand.'
    os.environ['intro_text'] = f"""Imagine you are a person from {os.environ['country']} moderating a discussion about {os.environ['topic']}. Based on the cultural values from {os.environ['country']}, provide your communication partner with stances why an average person from {os.environ['country']} would be pro/against {os.environ['topic']}. You should provide information in a casual style in English. Start the conversation with exactly the following prompt: 

\"Good afternoon. I will be your conversation partner today in a brief discussion about {os.environ['topic']}. This discussion is an opportunity for you to learn about {os.environ['topic']}. I want to encourage you to speak freely. You are not expected to be an expert. Also, no consensus is necessary, you do not need to agree with the stances I provide. My role is to help you learn about how people in {os.environ['country']} perceive the pros and cons of {os.environ['topic']}.\"

And then provide relevant cultural information in a pros/cons list. 

Lastly, encourage conversation by ending with \"Please start off by telling us something that puzzles you about this topic.\"
"""

    os.environ['gen_max_tokens'] = '512'
    os.environ['gen_system_instruction'] = (f"""You finish your response within {os.environ['gen_max_tokens']} tokens.
                                            If you ask a question, you make it open-ended.""")
    os.environ['shorter_system_instruction'] = (f"""You provide shorter, more conversational responses. If you ask a 
                                            question, you make it open-ended.""")
    os.environ['chatbot'] = 'AI chatbot'
    os.environ['yes'] = 'Yes'
    os.environ['no'] = 'No'
    os.environ['convo_limit'] = 'You must complete at least 5 rounds of conversation, but can complete up to 15.'
    os.environ['intro_wait'] = 'Launching chatbot, this can take up to 20 seconds...'
    os.environ['react_intro'] = "React to the introduction:"
    os.environ['you'] = 'You'
    os.environ['enter'] = 'Press Enter to send'
    os.environ['emoji_prompt'] = 'React to response'
    os.environ['finish_chat'] = 'Finish chat'
    os.environ['next_page'] = 'Next page'
    os.environ['feedback_page'] = 'Chatbot Responses for Feedback'
    os.environ['categories'] = 'Click to learn what each category means'
    os.environ['response'] = 'Response'
    os.environ['user'] = 'User'
    os.environ['give_feedback'] = 'Give feedback?'
    os.environ['categories_for_response'] = 'Categories for response'
    os.environ['comments'] = 'Comment for response'
    os.environ['options'] = 'Choose an option'
    os.environ['comment_prompt'] = 'Add your comment here'
    os.environ['submit'] = 'Submit'
    os.environ['submitted'] = 'Comments submitted! Click **Go to post-survey** to start the post-survey.'

    os.environ['emoji_warning_1'] = 'Please select an emoji for response '
    os.environ['emoji_warning_2'] = ' to proceed.'
    os.environ['convo_update_1'] = 'You have finished'
    os.environ['convo_update_2'] = 'round(s) of conversation.'
    os.environ['convo_warning_1'] = 'You can only ask'
    os.environ['convo_warning_2'] = 'more question(s) to the chatbot.'
    os.environ[
        'chat_complete'] = "**Chat complete**, thank you for chatting with the chatbot! Sometimes, chatbots produce responses that are inaccurate in a few different ways. Press **Next page** to review the chatbot's responses from this chat and provide feedback on them."
    os.environ['comment_outline'] = """
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
        """

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
