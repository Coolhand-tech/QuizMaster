import requests
import csv
import random
from time import time

class QuizMaster:
    def __init__(self):
        self.questions = []
        self.score = 0
        self.load_questions()

    def load_questions(self):
        response = requests.get("https://opentdb.com/api.php?amount=10&type=multiple")
        if response.status_code == 200:
            data = response.json()["results"]
            for q in data:
                self.questions.append({
                    "question": q["question"],
                    "correct": q["correct_answer"],
                    "options": q["incorrect_answers"] + [q["correct_answer"]]
                })
        else:
            print("Failed to fetch questions. Using fallback.")
            self.questions = [{"question": "What is 2+2?", "correct": "4", "options": ["3", "4", "5"]}]

    def run_quiz(self):
        random.shuffle(self.questions)
        for i, q in enumerate(self.questions[:5], 1):  # Limit to 5 questions
            print(f"\nQuestion {i}: {q['question']}")
            random.shuffle(q["options"])
            for j, opt in enumerate(q["options"], 1):
                print(f"{j}. {opt}")
            start = time()
            answer = input("Your answer (1-4): ")
            if time() - start > 10:  # 10-second limit
                print("Time's up!")
                continue
            if q["options"][int(answer) - 1] == q["correct"]:
                print("Correct!")
                self.score += 1
            else:
                print(f"Wrong! Correct answer: {q['correct']}")
        print(f"\nQuiz Over! Score: {self.score}/5")
        self.save_score()

    def save_score(self):
        with open("leaderboard.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([self.score, time.ctime()])

def main():
    qm = QuizMaster()
    qm.run_quiz()

if __name__ == "__main__":
    main()