import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import time

open_api_key = st.sidebar.text_input('OpenAI API Key', type='password')


llm = ChatOpenAI(api_key=open_api_key)

prompt = ChatPromptTemplate.from_messages({
    ("system", "당신은 소설 해리포터의 주인공인 해리포터입니다. 해리포터가 되어서 답변해주세요."),
    ("user", "{input}")
})

output_parser = StrOutputParser()

chain = prompt | llm | output_parser

st.title("Chat with Harry Potter")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""
    assistant_response =  chain.invoke({"input": prompt})
    # Simulate stream of response with milliseconds delay
    for chunk in assistant_response.split():
        full_response += chunk + " "
        time.sleep(0.05)
        # Add a blinking cursor to simulate typing
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
# Add assistant response to chat history
st.session_state.messages.append({"role": "assistant", "content": full_response})