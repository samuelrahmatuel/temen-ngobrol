import re

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
