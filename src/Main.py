from typing import List
from classes.Question import Question
import os
from PIL import ImageGrab
import pytesseract

def get_files_in_dir(dir_path) -> List[str]:
    return [os.path.join(dir_path, f) for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]

def get_questions(dir_path) ->  List[Question]:
    file_paths = get_files_in_dir(dir_path)
    questions = []
    for i, file_path in enumerate(file_paths):
        # print(f'Processing file {i + 1}/{len(file_paths)}: {file_path}')
        with open(file_path, 'r', encoding='utf-8') as file:
            raw_text = file.read()
            questions.append(Question(i, raw_text))
    return questions
    
    
questions = get_questions('./nast-testownik/')
print(f'Total questions: {len(questions)}')


box = (100, 200, 400, 300)  # Example coordinates

screenshot = ImageGrab.grab(bbox=box)
text = pytesseract.image_to_string(screenshot, lang='pol') #eng

print(text)