import os
import streamlit as st
import json
from utils.session import get_session_state, set_session_state
from utils.EN_labels import set_labels
from streamlit_theme import st_theme


def comments(user, background_color_user, background_color_bot):
    chat_history = user['chat_history']
    comments_history = user['comments']
    reaction_history = user['reaction_history']
    introduction = user['introduction']
    intro_reaction = user['intro_reaction']

    st.title("Post-experiment Review")

    st.markdown("## Introduction")
    st.markdown(f"""
            <div style='background-color: {background_color_user}; padding: 10px; border-radius: 10px; margin-bottom: 10px;'>
                <strong>Introduction:</strong> {introduction}
            </div>
        """, unsafe_allow_html=True)

    st.write(f"**Reaction to Introduction:** {intro_reaction}")

    st.markdown("<hr>", unsafe_allow_html=True)


    for i, (exchange, feedback, reaction) in enumerate(zip(chat_history, comments_history, reaction_history)):
        st.markdown(f"<h5><b>Response {i + 1}</b></h5>", unsafe_allow_html=True)

        col1, col2 = st.columns([3, 2])

        with col1:
            st.markdown(f"""
                <div style='background-color: {background_color_user}; padding: 10px; border-radius: 10px; margin-bottom: 10px;'>
                    <strong>User:</strong> {exchange['user_input']}
                </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
                <div style='background-color: {background_color_bot}; padding: 10px; border-radius: 15px; margin-bottom: 10px;'>
                    <strong>Bot:</strong> {exchange['response']}
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("### Feedback Summary")

            st.write(f"**Reaction:** {reaction}")

            feedback_status = "Yes" if feedback['feedback'] == 'yes' else "No"
            st.write(f"**Feedback Provided:** {feedback_status}")

            categories = feedback.get('categories', [])
            if categories:
                st.write(f"**Categories:** {', '.join(categories)}")

            other_categories = feedback.get('other_categories', [])
            if other_categories:
                st.write(f"**Other Categories:** {', '.join(other_categories)}")

            comment = feedback.get('comment', "")
            if comment:
                st.write(f"**Comment:** {comment}")

        st.markdown("<hr>", unsafe_allow_html=True)


def main():
    set_labels()
    theme = st_theme()['base']
    background_color_user = '#dcf8c6'
    background_color_bot = '#f1f0f0'
    if theme == 'dark':
        background_color_user = '#027148'
        background_color_bot = '#434343'

    query_params = st.query_params
    user_id = query_params.get("id", [None])

    with open('analysis/data.json', 'r') as file:
        data = json.load(file)

    user = {}
    for datum in data:
        if datum['id'] == user_id:
            user = datum
    if user:
        comments(user, background_color_user, background_color_bot)


if __name__ == '__main__':
    main()
