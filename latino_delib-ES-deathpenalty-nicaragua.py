import streamlit as st
import os
from utils.session import session_setup, get_session_state, set_session_state
from utils.pages import show_chat_page, show_feedback_page
from utils.ES_labels import set_labels

def setup():
    os.environ['country'] = 'Nicaragua'
    os.environ['topic'] = 'la pena de muerte'
    os.environ['intro_max_tokens'] = '512'

    os.environ['intro_system_instruction'] = "Responde con una lista de pros y contras sobre el tema en cuestión."
    os.environ['intro_text'] = f'''Imagine que es una persona de {os.environ['country']} moderando una discusión sobre {os.environ['topic']}. Basado en los valores culturales de {os.environ['country']}, dele a su compañero de conversación argumentos sobre por qué una persona promedio de {os.environ['country']} estaría a favor/en contra de {os.environ['topic']}. Debe darle la información en un estilo coloquial en español. Comience la conversación usando exactamente este mensaje:

"Buenas tardes. Seré su compañero de conversación hoy en una breve discusión sobre {os.environ['topic']}. Esta conversación es una oportunidad para que aprenda sobre {os.environ['topic']} en {os.environ['country']}. Quiero animarle a que hable libremente. No se espera que sea un experto. Además, no es necesario llegar a un consenso, no necesita estar de acuerdo con mis posturas. Mi papel es ayudarle a aprender cómo las personas en {os.environ['country']} perciben los pros y los contras de {os.environ['topic']}."

Luego comporte información culturalmente relevante en una lista de pros y contras.

Por último, fomente la conversación terminando con "Por favor, comience contándonos algo que encuentre controversial sobre este tema". 
'''

    os.environ['gen_max_tokens'] = '512'
    os.environ['gen_system_instruction'] = (f"""Termina tu respuesta dentro de {os.environ['gen_max_tokens']} tokens. No cambies de tema. Evite preguntas de \"sí\"/\"no\".""")
    os.environ[
        'shorter_system_instruction'] = "Proporciona respuestas más breves y casuales. No cambies de tema. Evite preguntas de \"sí\"/\"no\"."
    os.environ['post_survey'] = 'https://uwmadison.co1.qualtrics.com/jfe/form/SV_8pnDcNM6g9vhsvY'

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
