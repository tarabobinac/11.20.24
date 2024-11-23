
import streamlit as st
import os
from utils.chatbot import get_response
from utils.session import modify_chat_history, get_session_state, set_session_state
from utils.database import handle_submission
import random

minimum_responses = 10
warning_responses = 10
maximum_responses = 15


# display value of current round of conversation
def show_response_count():
    response_count = get_session_state('response_count')

    if response_count == 0:
        return

    response_count_message = f"{os.getenv('convo_update_1')} {response_count} {os.getenv('convo_update_2')}"

    if response_count < warning_responses:
        st.info(response_count_message)

    if warning_responses <= response_count < maximum_responses:
        convo_warning_1 = os.getenv('convo_warning_1')
        convo_warning_2 = os.getenv('convo_warning_2')
        extra_count = maximum_responses - response_count
        response_count_message += f"{convo_warning_1} {extra_count} {convo_warning_2}"
        st.warning(response_count_message)

    if maximum_responses <= response_count:
        st.success(response_count_message)


# display done button for comments to responses
def done_button(submit_button_disabled):
    if st.button(os.getenv('submit'), disabled=submit_button_disabled or get_session_state('done_pressed')):
        set_session_state('done_pressed', True)
        handle_submission()
        st.rerun()

    if get_session_state('done_pressed'):
        st.success(os.getenv('submitted'))

        # Display "Go to Post Survey" button after submission
        st.markdown(
            """
            <style>
                .survey-button {
                    display: flex;
                    justify-content: flex-start;  /* Align button to the left */
                    align-items: center;
                }
            </style>
            """, unsafe_allow_html=True)

        link = os.getenv('post_survey') + '?ID=' + get_session_state('respondent_id')
        st.markdown(
            f"""
            <div class="survey-button">
                <a href="{link}" target="_blank">
                    <button style="padding: 10px 20px; font-size: 16px; background-color: #027148; color: #f1f0f0; border: none; border-radius: 5px; cursor: pointer;">
                        {os.getenv('post_survey_message')}
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)


# show message and next page button if chat conversation is done
def show_finish_status():
    if get_session_state('survey_finished') is False:
        return

    if get_session_state('next_page'):
        st.button(os.getenv('next_page'), disabled=True)
        return

    st.success(os.getenv('chat_complete'))

    if st.button(os.getenv('next_page')):
        set_session_state('next_page', True)
        st.rerun()


# enable reactions for each response
def add_reaction_buttons(response_index):
    emojis = ["😄", "🙂", "😐", "🙁", "😡"]

    chat_history_length = len(get_session_state('chat_history'))
    is_latest_response = (response_index == chat_history_length - 1)
    disabled = not is_latest_response

    selected_emoji = st.radio(
        f"{os.getenv('emoji_prompt')} {response_index + 1}:",
        emojis,
        key=f"reaction_{response_index}",
        index=None,  # No default selection
        horizontal=True,
        disabled=disabled
    )

    reaction_history = get_session_state('reaction_history')
    reaction_history_length = len(reaction_history)
    if reaction_history_length == response_index:
        reaction_history.append(selected_emoji)
    elif reaction_history[response_index] != selected_emoji:
        reaction_history[response_index] = selected_emoji

    set_session_state('reaction_history', reaction_history)

    if is_latest_response and selected_emoji is None:
        st.warning(f"{os.getenv('emoji_warning_1')} {response_index + 1}{os.getenv('emoji_warning_2')}")
        st.stop()


# enable feedback to responses functionality
def comments():
    feedback_enabled_count = 0  # Track how many responses have feedback enabled
    valid_comments_count = 0    # Track how many valid comments (with categories) have been provided

    if get_session_state('comments') == []:
        comment_storage = [{'feedback': 'no', 'categories': [], 'other_categories': [], 'comment': ''} for _ in range(len(get_session_state('chat_history')))]
        set_session_state('comments', comment_storage)

    comment_storage = get_session_state('comments')

    for i, exchange in enumerate(get_session_state('chat_history')):
        st.markdown(f"<h5><b>{os.getenv('response')} {i + 1}</b></h5>", unsafe_allow_html=True)
        col1, col2 = st.columns([3, 2])

        with col1:
            st.markdown(f"""
                <div style='background-color: {get_session_state('background_color_user')}; padding: 10px; border-radius: 10px; margin-bottom: 10px;'>
                    <strong>{os.getenv('user')}:</strong> {exchange['user_input']}
                </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
                <div style='background-color: {get_session_state('background_color_bot')}; padding: 10px; border-radius: 15px; margin-bottom: 10px;
                min-height: 298px; display: block;'>
                    <strong>{os.getenv('response')}:</strong> {exchange['response']}
                </div>
            """, unsafe_allow_html=True)

        with col2:
            feedback_option = st.radio(os.getenv('give_feedback'), [os.getenv('no'), os.getenv('yes')], index=0,
                                       key=f"feedback_{i}",
                                       horizontal=True, disabled=get_session_state('done_pressed'))

            if feedback_option == os.getenv('yes'):
                feedback_enabled_count += 1
                comment_storage[i]['feedback'] = 'yes'
            else:
                comment_storage[i]['feedback'] = 'no'

            categories = st.multiselect(
                f"{os.getenv('categories_for_response')} {i + 1}",
                [os.getenv('category_1'), os.getenv('category_2'), os.getenv('category_3'), os.getenv('category_4'),
                 os.getenv('category_5'), os.getenv('category_6'), os.getenv('category_7'), os.getenv('category_8'),
                 os.getenv('category_9')],
                key=f"categories_{i}",
                placeholder=os.getenv('options'),
                disabled=feedback_option != os.getenv('yes') or get_session_state('done_pressed')
            )
            comment_storage[i]['categories'] = categories

            other_categories = comment_storage[i].get('other_categories', [])
            if os.getenv('category_9') in categories:
                new_other_category = st.text_input(
                    f"{os.getenv('specify_categories')}",
                    key=f"new_other_category_{i}",
                    disabled=feedback_option != os.getenv('yes') or get_session_state('done_pressed')
                )

                if st.button(f"{os.getenv('add_category')}", key=f"add_other_category_{i}",
                             disabled=feedback_option != os.getenv('yes') or get_session_state('done_pressed')):
                    if new_other_category.strip():
                        other_categories.append(new_other_category.strip())
                        comment_storage[i]['other_categories'] = other_categories

                # Display existing "Other" categories with remove buttons
                for j, other in enumerate(other_categories):
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.write(f"**{os.getenv('other_category')} {j + 1}**: {other}")
                    with col2:
                        if st.button(f"{os.getenv('remove')}", key=f"remove_other_{i}_{j}",
                                     disabled=feedback_option != os.getenv('yes') or get_session_state('done_pressed')):
                            other_categories.pop(j)
                            comment_storage[i]['other_categories'] = other_categories
                            st.rerun()

            else:
                comment_storage[i]['other_categories'] = []

            # Comment box and Enter button in the same column
            comment = st.text_area(
                f"{os.getenv('comments')} {i + 1}",
                key=f'comment_{i}',
                disabled=feedback_option != os.getenv('yes') or get_session_state('done_pressed'),
                placeholder=os.getenv('comment_prompt')
            )
            comment_storage[i]['comment'] = comment

            # Place the Enter button directly below the text area
            enter_button = st.button(
                f'''{os.getenv('enter_button')}''',
                key=f"enter_button_{i}",
                disabled=feedback_option != os.getenv('yes') or get_session_state('done_pressed')
            )

            # A valid comment requires a text comment and at least one category (including 'Other' if specified)
            if feedback_option == os.getenv('yes') and comment.strip() and (categories or other_categories):
                valid_comments_count += 1

    # Update 'comments' session state with the modified comment storage
    set_session_state('comments', comment_storage)

    submit_button_disabled = valid_comments_count < 2
    done_button(submit_button_disabled)




# accept or decline user input
def submit_user_input():
    if get_session_state('survey_finished'):
        st.text_input(os.getenv('you') + ':', value='', placeholder=os.getenv('enter'), key=str(get_session_state('response_count')), disabled=True)
        return None
    else:
        return st.text_input(os.getenv('you') + ':', value='', placeholder=os.getenv('enter'), key=str(get_session_state('response_count')))


# get input from the user and generate a response
def get_input_and_gen_response():
    if get_session_state('response_count') == maximum_responses:
        return

    if not get_session_state('submitted_input'):
        user_input = submit_user_input()
        if user_input:
            set_session_state('user_input', user_input)
            set_session_state('submitted_input', True)
            st.rerun()

    else:
        st.markdown(f"""
            <div class="chat-container">
                <div class="user-message">{get_session_state('user_input')}</div>
            </div>
        """, unsafe_allow_html=True)

        instruction = random.randint(0, 1)

        if instruction == 0:
            system_instruction = get_session_state('system_instruction')
        else:
            system_instruction = get_session_state('shorter_system_instruction')

        set_session_state('response_placeholder', st.empty())
        set_session_state('stream_text', '')

        get_response(get_session_state('user_input'), system_instruction, text_received)

        set_session_state('submitted_input', False)
        modify_chat_history(get_session_state('user_input'), get_session_state('stream_text'), system_instruction)

        response_count = get_session_state('response_count')
        response_count += 1
        set_session_state('response_count', response_count)
        st.rerun()


# get text stream response and draw the response box
def text_received(text):
    if text:
        stream_text = get_session_state('stream_text')
        stream_text += text
        set_session_state('stream_text', stream_text)

        get_session_state('response_placeholder').markdown(
            f"<div class='bot-message'>{get_session_state('stream_text')}</div>",
            unsafe_allow_html=True
        )
    else:
        get_session_state('response_placeholder').markdown(
            f"<div class='bot-message'>{get_session_state('stream_text')}</div>",
            unsafe_allow_html=True
        )
    return

def finish_button():
    response_count = get_session_state('response_count')

    # Hide the finish button if the maximum number of responses is reached
    if response_count >= maximum_responses:
        set_session_state('survey_finished', True)
        return  # Do not render the button

    # Disable the finish button if the survey is already marked as finished
    if get_session_state('survey_finished'):
        st.button(os.getenv('finish_chat'), disabled=True)
        return

    # Show the finish button only if the minimum number of responses has been met
    if response_count >= minimum_responses:
        if st.button(os.getenv('finish_chat')):
            set_session_state('survey_finished', True)
            st.rerun()
