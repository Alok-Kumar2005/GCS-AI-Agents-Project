import streamlit as st
import requests
from datetime import datetime

# Configure backend URL
BACKEND_URL = "http://localhost:8000/process-query"

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Page configuration
st.set_page_config(page_title="Support Agent Chat", page_icon="🤖")
st.title("Customer Support Chatbot")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "timestamp" in message:
            st.caption(f"_{message['timestamp']}_")

# Chat input
if prompt := st.chat_input("How can I help you today?"):
    # Add user message to chat history
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(f"_{st.session_state.messages[-1]['timestamp']}_")

    # Get assistant response
    with st.spinner("Analyzing your query..."):
        try:
            response = requests.post(
                BACKEND_URL,
                json={"query": prompt},
                headers={"Content-Type": "application/json"}
            ).json()
            
            if response["success"]:
                answer = response["response"]
            else:
                answer = "Sorry, there was an error processing your request."
        except Exception as e:
            answer = f"Connection error: {str(e)}"

    # Add assistant response to chat history
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(answer)
        st.caption(f"_{st.session_state.messages[-1]['timestamp']}_")