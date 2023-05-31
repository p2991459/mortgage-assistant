import difflib

def get_best_match(user_input, predefined_questions, threshold=0.6):
    matches = difflib.get_close_matches(user_input, predefined_questions, n=1, cutoff=threshold)
    if matches:
        return matches[0]
    else:
        return None