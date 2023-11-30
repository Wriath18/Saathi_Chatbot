# from langchain import PromptTemplate, LLMChain
# import chainlit as cl
# from langchain import HuggingFaceHub
# import PySimpleGUI as sg
# from translate import Translator as TextTranslator

# a = []  # Create a list to store the selected language

# def select_language(window, event, values):
#     selected_language = values['-LANGUAGE-']
#     a.append(selected_language)  # Append the selected language to the 'a' list
#     window.close()

# sg.theme('DefaultNoMoreLines')

# layout = [[sg.Text('Select Language'), sg.Combo(['English', 'Spanish', 'French'], key='-LANGUAGE-')],
#           [sg.Button('OK', key='-OK-')]]

# window = sg.Window('Language Selector', layout)

# while True:
#     event, values = window.read()
#     if event == sg.WINDOW_CLOSED:
#         break
#     elif event == '-OK-':
#         select_language(window, event, values)

# # window.close()

# repo_id = "tiiuae/falcon-7b-instruct"
# # Create the HuggingFaceHub object
# llm = HuggingFaceHub(
# huggingfacehub_api_token='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',
# repo_id=repo_id,
# model_kwargs={"temperature":0.3, "max_new_tokens":1024}
# )


# template = """ Task: write a specific answer to question related to education only, giving reference to the textbooks.
# Topic: education
# Style: Academic
# Tone: Curious
# Audience: 5-10 year olds
# Length: 1 paragraph
# Format: Text
# Here's the question. {question}
# """


# @cl.on_chat_start
# def main():
#     # Instantiate the chain for that user session
#     prompt = PromptTemplate(template=template, input_variables=["question"])
#     llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=True)

#     # Store the chain in the user session
#     cl.user_session.set("llm_chain", llm_chain)


# @cl.on_message
# async def main(message: cl.Message):
#     # Retrieve the chain from the user session
#     llm_chain = cl.user_session.get("llm_chain")  # type: LLMChain

#     # Call the chain asynchronously
#     res = await llm_chain.acall(message.content, callbacks=[cl.AsyncLangchainCallbackHandler()])
#     # english = res["text"]
#     if(a[0]=="Spanish"):
#         translator = TextTranslator(to_lang="es")
#     elif(a[0]=="French"):
#         translator = TextTranslator(to_lang="fr")
#     else:
#         translator = TextTranslator(to_lang="en")

#     # translator = TextTranslator(to_lang="es")
#     # translation = translator.translate(english)
#     # res["text"] = translation
#     # Do any post processing here

#     # "res" is a Dict. For this chain, we get the response by reading the "text" key.
#     # This varies from chain to chain, you should check which key to read.
#     await cl.Message(content=translator.translate(res["text"])).send()
#     print(translator)


from langchain import PromptTemplate, LLMChain
import chainlit as cl
from langchain import HuggingFaceHub
import PySimpleGUI as sg
from translate import Translator as TextTranslator

a = []  # Language selection list

def select_language(window, event, values):
    a.append(values['-LANGUAGE-'])
    window.close()

# GUI for language selection
sg.theme('DefaultNoMoreLines')
layout = [[sg.Text('Select Language'), sg.Combo(['English', 'Spanish', 'French'], key='-LANGUAGE-')],
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

@cl.on_chat_start
def main():
    prompt = PromptTemplate(template=template, input_variables=["user_input"])
    llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=True)
    cl.user_session.set("llm_chain", llm_chain)

@cl.on_message
async def main(message: cl.Message):
    llm_chain = cl.user_session.get("llm_chain")
    
    # Debugging: Print the user input to ensure it's captured correctly
    print("User input:", message.content)
    
    # Ensure that the 'user_input' variable is used correctly
    res = await llm_chain.acall({"user_input": message.content}, callbacks=[cl.AsyncLangchainCallbackHandler()])

    # Print the response from the model to debug
    print("Model response before translation:", res["text"])

    language = a[0] if a else "en"
    translator = TextTranslator(to_lang=language)
    
    # Translate the response
    translated_response = translator.translate(res["text"])
    
    # Debugging: Print the translated response
    print("Translated response:", translated_response)
    
    # Send the translated response back to the user
    await cl.Message(content=res['text']).send()

if __name__ == "__main__":
    main()
