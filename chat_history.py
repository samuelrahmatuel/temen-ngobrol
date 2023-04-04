import streamlit as st

def add_chat_history(user_input, bot_response):
    chat_history = st.session_state.get("chat_history", [])
    chat_history.append({"user_input": user_input, "bot_response": bot_response})
    st.session_state["chat_history"] = chat_history

def display_chat_history():
    chat_history = st.session_state.get("chat_history", [])
    st.write("Chat History:")
    with st.expander("Expand to view chat history"):
        for chat in chat_history:
            user_input = chat["user_input"]
            bot_response = chat["bot_response"]
            if user_input:
                st.write(f"User: {user_input}")
            if bot_response:
                st.write(bot_response)
