import os
import streamlit as st
from utils.components import (add_reaction_buttons, get_input_and_gen_response, show_response_count,
                              finish_button, show_finish_status, comments)
from utils.session import get_session_state, set_session_state


def show_chat_page():
    st.title(os.getenv('chatbot'))

    introduction = get_session_state('introduction')
    st.info(introduction)
    st.warning(os.getenv('convo_limit'))

    intro_emoji = st.radio(
        os.getenv('react_intro'),
        ["❤️", "😂", "😮", "😢", "😡", "👍", "👎"],
        key="intro_reaction",
        index=None,
        horizontal=True,
        disabled=get_session_state('intro_reaction') is not None and get_session_state('user_input') is not None
    )

    if intro_emoji and get_session_state('intro_reaction') is None:
        set_session_state('intro_reaction', intro_emoji)
        st.success("Thank you for reacting to the introduction!")
        st.experimental_rerun()

    if not get_session_state('intro_reaction'):
        st.warning(os.getenv('intro_emoji'))
        st.stop()

    for i, exchange in enumerate(get_session_state('chat_history')):
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
    st.subheader(os.getenv('feedback_page'))
    st.write(os.getenv('comment_outline'))

    with st.expander(os.getenv('categories')):
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
