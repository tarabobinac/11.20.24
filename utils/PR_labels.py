import os

def set_labels():
    os.environ['chatbot'] = 'Chatbot de IA'
    os.environ['yes'] = 'Sim'
    os.environ['no'] = 'Não'
    os.environ[
        'convo_limit'] = 'Deve completar pelo menos 10 rodadas de conversa, mas você pode completar até 15.'
    os.environ['intro_wait'] = 'Iniciando o chatbot, isso pode levar até 20 segundos...'
    os.environ['react_intro'] = 'Reação à introdução:'
    os.environ['intro_emoji'] = 'Selecione um emoji para continuar conversando.'
    os.environ['you'] = 'Você'
    os.environ['enter'] = 'Pressione Enter para enviar'
    os.environ['enter_button'] = 'Enviar'
    os.environ['emoji_prompt'] = 'Reaja à resposta'
    os.environ['finish_chat'] = 'Finalizar chat'
    os.environ['next_page'] = 'Próxima página'
    os.environ['feedback_page'] = 'Respostas do chatbot para comentários'
    os.environ['categories'] = 'Clique para saber o que significa cada categoria'
    os.environ['response'] = 'Resposta'
    os.environ['user'] = 'Usuário'
    os.environ['give_feedback'] = 'Fazer comentários?'
    os.environ['categories_for_response'] = 'Categorias para a resposta'
    os.environ['comments'] = 'Comentário para a resposta'
    os.environ['options'] = 'Escolha uma opção'
    os.environ['comment_prompt'] = 'Adicione seu comentário aqui'
    os.environ['submit'] = 'Enviar'
    os.environ[
        'submitted'] = '**Comentários enviados!** Clique em **Ir para a enquete** para começar a enquete.'

    os.environ['emoji_warning_1'] = 'Por favor, selecione um emoji para a resposta'
    os.environ['emoji_warning_2'] = ' para continuar.'
    os.environ['convo_update_1'] = 'Você completou'
    os.environ['convo_update_2'] = 'rodada(s) de conversa. '
    os.environ['convo_warning_1'] = 'Você só pode fazer mais'
    os.environ['convo_warning_2'] = 'pergunta(s) ao chatbot.'
    os.environ['category_1'] = 'Respeitoso'
    os.environ['category_2'] = 'Desrespeitoso'
    os.environ['category_3'] = 'Com conhecimento cultural'
    os.environ['category_4'] = 'Sem conhecimento cultural'
    os.environ['category_5'] = 'Objetivamente correto'
    os.environ['category_6'] = 'Objetivamente incorrecto'
    os.environ['category_7'] = 'Aberto para ouvir o usuário'
    os.environ['category_8'] = 'Não aberto para ouvir o usuário'
    os.environ['category_9'] = 'Outro'
    os.environ['other_category'] = 'Outra categoria'
    os.environ['remove'] = 'Remover'
    os.environ['specify_categories'] = 'Especificar categoria:'
    os.environ['add_category'] = 'Adicionar categoria'
    os.environ['post_survey_message'] = 'Ir para a enquete'
    os.environ[
        'chat_complete'] = "**Chat finalizado**, obrigado por conversar com o chatbot! Às vezes, os chatbots geram respostas que são imprecisas de diversas maneiras. Pressione **Próxima página** para revisar as respostas do chatbot deste chat e fornecer feedback sobre elas."
    os.environ['comment_outline'] = """
                    Nesta página, você pode fornecer feedback sobre as respostas do chatbot.

                    Abaixo, você verá uma lista de pares de mensagens e respostas do seu chat. Sua mensagem está em ***verde***, enquanto a resposta do chatbot está em ***cinza***.

                    À direita de uma resposta, você pode clicar em **Sim** em **Fazer comentários?** se quiser fornecer feedback sobre essa resposta, ou pode clicar em **Não** se não quiser. 

                    Se você decidir dar feedback sobre uma resposta, pode especificar o tipo escolhendo entre as categorias no menu suspenso. Você pode escolher mais de uma. Em seguida, preencha a caixa de comentários com suas considerações sobre a resposta.

                    **Você deve fornecer feedback para pelo menos duas respostas, selecionando pelo menos uma categoria e escrevendo um comentário para cada uma**, momento em que o botão **Enviar** será habilitado.

                    Clique em **Enviar** quando terminar, depois clique em **Ir para a enquete** para começar a enquete.
                    """
