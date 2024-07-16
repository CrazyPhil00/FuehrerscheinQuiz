import json
import re
import fitz
from flask import Flask, render_template, request, redirect, url_for
import random
import time


def extract_quiz_data(pdf_path):
    document = fitz.open(pdf_path)
    quiz_data = []
    image_count_set = set()  # Use a set to track unique images

    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text = page.get_text("text")

        # Split the text into lines
        lines = text.split('\n')

        # Determine the number of lines to skip (adjust this value as needed)
        lines_to_skip = 2  # Example: skipping the first 2 lines

        # Remove the initial lines from consideration
        relevant_lines = lines[lines_to_skip:]

        # Join the relevant lines back into a single string
        filtered_text = '\n'.join(relevant_lines)

        # Split the text into segments based on chapter introductions
        segments = re.split(r'(Quesito n° \d+ - .*)', filtered_text, flags=re.IGNORECASE)

        # Iterate over each segment
        for segment in segments:
            # Apply the regular expression to the segment
            pattern = re.compile(r'(\d+)\s+(.*?)\s+(VERO|FALSO)\s*$', re.DOTALL | re.MULTILINE)
            matches = pattern.findall(segment)

            # Check if there are any images on the page
            images_on_page = page.get_images(full=True)
            has_image = False

            for img in images_on_page:
                # Generate a unique key for each image based on its index and width
                image_key = f"{img[0]}_{img[1]}"
                if image_key not in image_count_set:
                    image_count_set.add(image_key)
                    has_image = True
                    break

            for match in matches:
                numero_domanda, testo_domanda, risposta_corretta = match
                testo_domanda = ' '.join(testo_domanda.split()).strip()

                if has_image:
                    quiz_data.append({
                        'numero_domanda': numero_domanda,
                        'testo_domanda': testo_domanda,
                        'risposta_corretta': risposta_corretta,
                        'has_image': f"images/DomandeB.pdf-image-{list(image_count_set).index(image_key) + 1}.jpg"
                    })
                else:
                    quiz_data.append({
                        'numero_domanda': numero_domanda,
                        'testo_domanda': testo_domanda,
                        'risposta_corretta': risposta_corretta,
                        'has_image': None
                    })

    print(f"Found {len(image_count_set)} unique images")
    return quiz_data


app = Flask(__name__)

# Load the quiz data (already extracted in the previous step)
# quiz_data = extract_quiz_data('DomandeB.pdf')

with open("questions.json", "r") as file:
    quiz_data = json.load(file)


# Route for the home page
@app.route('/')
def home():
    return render_template('home.html')


# Route to start the quiz
@app.route('/start_quiz')
def start_quiz():
    selected_questions = random.sample(quiz_data, 30)  # Select 30 random questions
    start_time = time.time()
    return render_template('quiz.html', questions=selected_questions, start_time=start_time)


# Route to handle quiz submission
@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    answers = request.form
    score = 0
    result = []

    # Create a dictionary for easy access to user answers
    user_answers = {key: answers.get(key) for key in answers}

    for question in quiz_data:
        question_id = question['id']
        user_answer = user_answers.get(question_id)

        if user_answer:
            if user_answer == question['is_true']:
                score += 1
                result.append({
                    'question_id': question_id,
                    'text': question['text_translated'],
                    'user_answer': user_answer,
                    'correct': True
                })
            else:
                result.append({
                    'question_id': question_id,
                    'text': question['text_translated'],
                    'user_answer': user_answer,
                    'correct': False,
                    'correct_answer': question['is_true']
                })

    return render_template('result.html', score=score, result=result)


if __name__ == '__main__':
    app.run(debug=True)
