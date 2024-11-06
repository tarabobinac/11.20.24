import streamlit as st
import os
from utils.session import session_setup, get_session_state, set_session_state
from utils.pages import show_chat_page, show_feedback_page
from utils.PR_labels import set_labels

def setup():
    os.environ['topic'] = 'o aborto'
    os.environ['intro_max_tokens'] = '512'
    os.environ['intro_system_instruction'] = 'Responda com uma lista de prós e contras sobre o tema em questão.'
    os.environ['intro_text'] = f'''Imagine que você é uma pessoa do Brasil moderando uma discussão sobre {os.environ['topic']}. Com base nos valores culturais do Brasil, forneça ao seu companheiro de comunicação argumentos sobre por que uma pessoa média do Brasil estaria a favor ou contra {os.environ['topic']}. Você deve fornecer informações em um estilo casual em português. Comece a conversa exatamente com o seguinte aviso:

"Boa tarde. Serei seu companheiro de conversa hoje em uma breve discussão sobre {os.environ['topic']}. Esta discussão é uma oportunidade para você aprender sobre {os.environ['topic']} no Brasil. Quero encorajá-lo a falar livremente. Não se espera que você seja um especialista. Além disso, não é necessário chegar a um consenso, você não precisa concordar com as posturas que eu fornecer. Meu papel é te ajudar a aprender como as pessoas no Brasil percebem os prós e os contras d{os.environ['topic']}."

E então forneça informações culturalmente relevantes em uma lista de prós e contras.

Por último, incentive a conversa terminando com "Por favor, comece nos contando algo que você considera controverso sobre este tema."
'''
    os.environ['gen_max_tokens'] = '512'
    os.environ['gen_system_instruction'] = (f"""Termine a sua resposta dentro de {os.environ['gen_max_tokens']} tokens.
                                            Evite perguntas de \"sim\"/\"não\".""")
    os.environ['shorter_system_instruction'] = 'Use respostas curtas e casuais. Evite perguntas de \"sim\"/\"não\".'

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
    page_title='AI chatbot',
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
