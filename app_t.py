from langchain import PromptTemplate, LLMChain
import chainlit as cl
from langchain import HuggingFaceHub
import PySimpleGUI as sg
#from translate import Translator as TextTranslator
from deep_translator import GoogleTranslator



language_options = {
    'English': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Italian': 'it',
    'Portuguese': 'pt',
    'Dutch': 'nl',
    'Russian': 'ru',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Chinese': 'zh-cn',
    'Arabic': 'ar'
}


a = []  # Language selection list
def select_language(window, event, values):
    a.append(language_options[values['-LANGUAGE-']])
    window.close()


# GUI for language selection
sg.theme('DefaultNoMoreLines')
layout = [[sg.Text('Select Language'), sg.Combo(list(language_options.keys()), key='-LANGUAGE-')],
          [sg.Button('OK', key='-OK-')]]
window = sg.Window('Language Selector', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == '-OK-':
        select_language(window, event, values)

repo_id = "tiiuae/falcon-7b-instruct"
llm = HuggingFaceHub(
    huggingfacehub_api_token='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',
    repo_id=repo_id,
    model_kwargs={"temperature":0.3, "max_new_tokens":1024}
)

# Chatbot prompt template
template = """ Task: Chat with the user in a friendly and conversational manner.
Style: Conversational
Tone: Friendly
Audience: General public
User says: "{user_input}"
How should the chatbot respond?"""

def translate_text(text, target_language_code):
    translator = GoogleTranslator(source='auto', target=target_language_code)
    return translator.translate(text)

@cl.on_chat_start
def main():
    prompt = PromptTemplate(template=template, input_variables=["user_input"])
    llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=True)
    cl.user_session.set("llm_chain", llm_chain)

@cl.on_message
async def main(message: cl.Message):
    llm_chain = cl.user_session.get("llm_chain")
    print("User input:", message.content)
    
    # Default to English if no language has been selected
    target_language_code = 'en'
    if a:  # if language selection list is not empty
        target_language_code = a[0]  # 'a' now contains the language code directly

    res = await llm_chain.acall({"user_input": message.content}, callbacks=[cl.AsyncLangchainCallbackHandler()])
    print("Model response before translation:", res["text"])

    translated_response = translate_text(res['text'], target_language_code)
    print("Translated response:", translated_response)
    await cl.Message(content=translated_response).send()

if __name__ == "__main__":
    main()
