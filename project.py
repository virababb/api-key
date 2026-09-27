import html
import random
import urllib.request
import json

API_URL = "https://opentdb.com/api.php?amount=5&type=multiple"


def fetch_questions():
    with urllib.request.urlopen(API_URL) as response:
        data = json.loads(response.read().decode())

    if data.get("response_code") != 0 or not data.get("results"):
        raise RuntimeError("Could not fetch trivia questions from the API.")

    questions = []
    for item in data["results"]:
        question_text = html.unescape(item["question"])
        correct_answer = html.unescape(item["correct_answer"])
        incorrect_answers = [html.unescape(a) for a in item["incorrect_answers"]]

        options = incorrect_answers + [correct_answer]
        random.shuffle(options)

        questions.append({
            "question": question_text,
            "options": options,
            "correct": correct_answer,
        })

    return questions


def ask_question(number, total, q):
    print(f"\nQuestion {number} of {total}")
    print(q["question"])
    for i, option in enumerate(q["options"], start=1):
        print(f"  {i}. {option}")

    while True:
        choice = input("Your answer (1-4): ").strip()
        if choice in ("1", "2", "3", "4"):
            break
        print("Please enter a number between 1 and 4.")

    selected = q["options"][int(choice) - 1]
    is_correct = selected == q["correct"]

    if is_correct:
        print("Correct!")
    else:
        print(f"Wrong. The correct answer was: {q['correct']}")

    return is_correct


def main():
    print("Welcome to the Trivia Quiz!")

    try:
        questions = fetch_questions()
    except (urllib.error.URLError, RuntimeError) as e:
        print(f"Error fetching questions: {e}")
        return

    score = 0
    for i, q in enumerate(questions, start=1):
        if ask_question(i, len(questions), q):
            score += 1

    print(f"\nQuiz complete! Your final score: {score} out of {len(questions)}")


if __name__ == "__main__":
    main()