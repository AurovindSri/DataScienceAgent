import streamlit as st
import requests
import json

# API Endpoint
CHAT_API_URL = "http://localhost:8080/chat/"
CHAT_HISTORY_URL = "http://localhost:8080/chat_history/"
CLEAR_HISTORY_URL = "http://localhost:8080/clear_history/"

def send_message(thread_id, message):
    """Send a message to the chatbot."""
    response = requests.post(CHAT_API_URL, json={"thread_id": thread_id, "message": message})
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error: {response.json().get('detail', 'Failed to send message')}")
        return None

def get_chat_history(thread_id):
    """Fetch chat history for a user."""
    response = requests.get(f"{CHAT_HISTORY_URL}{thread_id}")
    if response.status_code == 200:
        return response.json()["chat_history"]
    else:
        st.warning("No chat history found.")
        return []

def clear_chat_history(thread_id):
    """Clear the chat history for a user."""
    response = requests.post(f"{CLEAR_HISTORY_URL}{thread_id}")
    if response.status_code == 200:
        st.success("Chat history cleared successfully.")
    else:
        st.error("Failed to clear chat history.")

# Streamlit UI
st.title("Data Science Chatbot")
st.sidebar.title("Settings")

# Thread ID input
thread_id = st.sidebar.text_input("Thread ID", value="5")

# Reset session state and chat history when the user ID changes
if "thread_id" not in st.session_state or st.session_state["thread_id"] != thread_id:
    st.session_state["thread_id"] = thread_id
    st.session_state["messages"] = get_chat_history(thread_id)

# Display chat history (Excluding system and tool messages)
st.subheader("Chat History")
for msg in st.session_state["messages"]:
    if msg['type'] == "human":
        st.markdown(f"<p><strong style='color: blue; font-size: 18px;'>You:</strong> <span style='font-size: 16px;'>{msg['content']}</span></p>", unsafe_allow_html=True)
    elif msg['type'] == "ai" and msg['content'].strip():
        st.markdown(f"<p><strong style='color: green; font-size: 18px;'>Bot:</strong> <span style='font-size: 16px;'>{msg['content']}</span></p>", unsafe_allow_html=True)

# Form for user message input with automatic send on Enter key
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Your message:")
    submit_button = st.form_submit_button(label="Send")

    if submit_button and user_input.strip():
        messages = send_message(thread_id, user_input)
        ai_response = messages[-1]
        if ai_response:
            # Update local session messages only if new message is sent and AI response is received
            if "messages" not in st.session_state:
                st.session_state["messages"] = []
            st.session_state["messages"].append({"type": "human", "content": user_input})
            st.session_state["messages"].append({"type": "ai", "content": ai_response['content']})
            st.rerun()

# Clear chat history button
if st.sidebar.button("Clear Chat History"):
    clear_chat_history(thread_id)
    st.session_state["messages"] = []
    st.rerun()
