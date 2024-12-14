from langchain_openai import ChatOpenAI
from openai import OpenAI
import os
import streamlit as st

id_assistant = "asst_LbT2H79ZcPIxru0vxdqLT6iC"


os.environ["OPENAI_API_KEY"] = "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"
client = OpenAI()

def get_response(thread, prompt):

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=id_assistant
    )

    messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
    ans = messages[0].content[0].text.value

    return ans

def main():

    st.title("Test Chatbot")

    # Initialize thread and chat history
    if "thread_id" not in st.session_state:
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id
    else:
        thread = client.beta.threads.retrieve(st.session_state.thread_id)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        if message['role'] == 'user':
            with st.chat_message("user"):
                st.markdown(message['content'])
        elif message['role'] == 'assistant':
            with st.chat_message("assistant"):  # Path to avatar image
                st.markdown(message['content'])

    # React to user input
    if prompt := st.chat_input("Ask me any question!"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(f'**You**: {prompt}')
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get response from the assistant
        response = get_response(thread, prompt)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(f'**Assistant**: {response}')
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()