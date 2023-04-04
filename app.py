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

st.set_page_config(page_title="Chatbot", page_icon=":robot_face:")

st.title("Self Learning Teman-Bicara")
st.write("Halo, saya adalah Teman-Bicara. Saya adalah project iseng yand dibuat dengan bahasa Python, walaupun simple saya bisa belajar sendiri loh, kaget kan?")
st.write("Kamu bisa tanya apa saja tergantung apakah saya sudah tau atau belum. Kalau belum tau saya akan bertanya dan kamu mengajarkan saya dengan kode (// jawaban).")
st.write("Lalu saya akan mengingatnya secara permanen untuk kedepan dan untuk penanya lain, keren kan?. ps ; maaf ya hapusnya masih manual, hehe")

knowledge_base = load_knowledge_base('knowledge_base.json')
faq_questions = [q['question'] for q in knowledge_base['questions']]
random.shuffle(faq_questions)

with st.expander("Frequently Asked Questions"):
    selected_faq = st.selectbox("", faq_questions[:10])

    if selected_faq:
        answer = next((q["answer"] for q in knowledge_base["questions"] if q["question"] == selected_faq), None)
        st.write(f"Q: {selected_faq}")
        st.write(f"A: {answer}")

with st.expander("Chat History"):
    chat_history = st.session_state.get("chat_history", [])
    for chat in chat_history:
        user_input = chat["user_input"]
        bot_response = chat["bot_response"]

        if user_input:
            st.write(f"User: {user_input}")
        if bot_response:
            st.write(bot_response)

with st.container():
    st.write("Tanyakan saya sesuatu disini, kalau saya belum tau gunakan ini setelah bertanya '// '")
    user_input = st.text_input("", key='input_box')
    submit_button = st.button("Submit")

    last_question = st.session_state.get("last_question", None)

    if submit_button:
        if user_input.startswith("//"):
            new_answer = user_input[2:].strip()

            if last_question:
                knowledge_base["questions"].append({"question": last_question, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                st.write(f"Bot: Makasih Loh udah ngajarin! Saya jadi ngerti kalo jawaban pertanyaan '{last_question}' itu tuh ini '{new_answer}' okedehh.")
            else:
                st.write("Bot: Hmmm, kamu belum nanya deh kayaknya atau udah kujawab kalii")

            st.session_state["last_question"] = None

            chat_history.append({"user_input": user_input, "bot_response": f"Bot: Makasih Loh udah ngajarin! Saya jadi ngerti kalo jawaban pertanyaan '{last_question}' itu tuh ini '{new_answer}' okedehh."})

        else:
            matched_question = match_keywords(user_input, [q["question"] for q in knowledge_base["questions"]])

            if matched_question:
                answer = next((q["answer"] for q in knowledge_base["questions"] if q["question"] == matched_question), None)
                st.write(f"User: {user_input}")
                st.write(f"Bot: {answer}")
                st.session_state["last_question"] = None

                chat_history.append({"user_input": user_input, "bot_response": f"Bot: {answer}"})
            
            else:
                answer = "Gatauu jawabannya bingung euy, ajarin dong (// jawaban benernya)"
                st.write(f"User: {user_input}")
                st.write(f"Bot: {answer}")
                st.session_state["last_question"] = user_input

                chat_history.append({"user_input": user_input, "bot_response": f"Bot: {answer}"})

        st.session_state["chat_history"] = chat_history

st.write("Next Progress : Better UI, Better Algorithms, Implementing Deep Learning for recommendation, Add more features")
st.markdown("<p style='text-align: right; font-style: italic;'>Created by: <a href='https://rahmatuelsamuel.com'>Rahmatuel Samuel</a></p>", unsafe_allow_html=True)
