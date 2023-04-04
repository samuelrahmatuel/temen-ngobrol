import streamlit as st
import json
import random
import re

def load_knowledge_base(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_knowledge_base(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def match_keywords(user_input, questions):
    user_words = set(re.findall(r'\w+', user_input.lower()))
    best_match = None
    best_score = 0

    for question in questions:
        question_words = set(re.findall(r'\w+', question.lower()))
        score = len(user_words & question_words)

        if score > best_score:
            best_match = question
            best_score = score

    return best_match

st.title("Chatbot")

container = st.container()

user_input = st.text_input("Ask a question or use '// ' before your input to provide an answer (e.g. '// answer'):", key='input_box')
submit_button = st.button("Submit")

knowledge_base = load_knowledge_base('knowledge_base.json')
last_question = st.session_state.get("last_question", None)

if submit_button:
    if user_input.startswith("//"):
        new_answer = user_input[2:].strip()

        if last_question:
            knowledge_base["questions"].append({"question": last_question, "answer": new_answer})
            save_knowledge_base('knowledge_base.json', knowledge_base)
            st.write(f"Bot: Thank you! I've learned that the answer to '{last_question}' is '{new_answer}'.")
        else:
            st.write("Bot: I can't find the last question you asked. Please ask a question first.")

        st.session_state["last_question"] = None

    else:
        matched_question = match_keywords(user_input, [q["question"] for q in knowledge_base["questions"]])

        if matched_question:
            answer = next((q["answer"] for q in knowledge_base["questions"] if q["question"] == matched_question), None)
            container.markdown(f"<div style='text-align: right;'><strong>You:</strong> {user_input}</div>", unsafe_allow_html=True)
            container.markdown(f"<div><strong>Bot:</strong> {answer}</div>", unsafe_allow_html=True)
            st.session_state["last_question"] = None
        else:
            answer = "I don't know the answer. Can you teach me?"
            container.markdown(f"<div style='text-align: right;'><strong>You:</strong> {user_input}</div>", unsafe_allow_html=True)
            container.markdown(f"<div><strong>Bot:</strong> {answer}</div>", unsafe_allow_html=True)
            st.session_state["last_question"] = user_input
