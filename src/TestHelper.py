import os
import numpy as np
import pytesseract
from PIL import ImageGrab
import pyautogui
import tkinter as tk
import threading
import difflib
from pynput import keyboard
from typing import List
from classes.DeepseekApi import DeepseekApi
from classes.Question import Question
from dotenv import load_dotenv, dotenv_values 
import json

# === Load Config ===
load_dotenv() 
with open('./config.json', 'r') as f:
    config = json.load(f)

# === Load Questions ===
def get_files_in_dir(dir_path) -> List[str]:
    return [os.path.join(dir_path, f) for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]

def get_questions(dir_path) -> List[Question]:
    file_paths = get_files_in_dir(dir_path)
    questions = []
    for i, file_path in enumerate(file_paths):
        with open(file_path, 'r', encoding='utf-8') as file:
            raw_text = file.read()
            _id = file_path.split('/')[-1].split('.')[0]
            questions.append(Question(_id, raw_text))
    return questions

questions = get_questions('./data/')
print(f'Total questions loaded: {len(questions)}')

# === Answer Overlay ===
class AnswerOverlay:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', config["alpha_level"])
        self.root.overrideredirect(True)
        self.label = tk.Label(self.root, text="", justify='left', font=("Arial", 12), bg="white")
        self.label.pack()
        self.visible = False
        self.hide()

    def show(self, text):
        self.label.config(text=text)
        self.root.geometry(f"+{int(config["position_top_left"]["x"])}+{int(config["position_top_left"]["y"])}")
        # self.root.deiconify()
        # self.visible = True

    def hide(self):
        self.root.withdraw()
        self.visible = False

    def toggle(self):
        if self.visible:
            self.hide()
        else:
            self.root.deiconify()
            self.visible = True

# === Similarity Function ===
def find_best_matches(text: str, questions: List[Question], threshold: float) -> List[tuple[Question, float]]:
    results = []

    for q in questions:
        score = difflib.SequenceMatcher(None, text, q.raw_text).ratio()
        # Boost score if OCR text is a substring
        if text.strip() in q.raw_text:
            score += 0.3  # optional boost, tune as needed

        if score >= threshold:
            results.append((q, score))

    # Sort results by score descending
    results.sort(key=lambda x: x[1], reverse=True)
    return results

# === Take screenshot and OCR ===
def handle_screenshot_to_text(start_pos, end_pos):
    left = min(start_pos.x, end_pos.x)
    top = min(start_pos.y, end_pos.y)
    right = max(start_pos.x, end_pos.x)
    bottom = max(start_pos.y, end_pos.y)
    box = (left, top, right, bottom)
    screenshot = ImageGrab.grab(bbox=box)
    text = pytesseract.image_to_string(screenshot, lang=f'{config["ocr_language"]}')
    print("OCR Text:\n", text)
    return text

def run_deepseek_in_thread(overlay, deepseek, start_pos, end_pos):
    overlay.show(f"CHAT:\nWAITING....")
    text = handle_screenshot_to_text(start_pos, end_pos)
    
    prompt = config["deepseek_prompt"].replace("[TEXT]", text)
    res = deepseek.get_response(message=prompt)
    overlay.show(f"CHAT:\n{(res)}")

# === Main function ===
def start_listener(overlay: AnswerOverlay, deepseek: DeepseekApi):
    start_pos = None
    end_pos = None
    
    def on_press(key):
        nonlocal start_pos, end_pos

        try:
            if key.char == 'l':
                start_pos = pyautogui.position()
                print(f"Top-left corner saved: {start_pos}")

            elif key.char == 'r':
                end_pos = pyautogui.position()
                print(f"Bottom-right corner saved: {end_pos}")

                if start_pos and end_pos:
                    text = handle_screenshot_to_text(start_pos, end_pos)

                    matches = find_best_matches(text, questions, threshold=config["min_answer_confidence"])
                    matches = matches[:config["n_best_answers"]]

                    if not matches:
                        print("No suitable question found.")
                        overlay.show('???')
                    else:
                        output_lines = []
                        for match, score in matches:
                            print(f"Match: Question ID {match.id} | Score: {score:.2f}")
                            correct_ans = "\n".join(match.correct_answers.tolist())
                            full_text = f"[{score:.2f}] {match.question}\n{correct_ans}"
                            output_lines.append(full_text)

                        overlay.show("\n\n".join(output_lines))
            elif key.char == 'd':
                end_pos = pyautogui.position()
                print(f"Bottom-right corner saved: {end_pos}")
                if start_pos and end_pos:
                    threading.Thread(
                        target=run_deepseek_in_thread,
                        args=(overlay, deepseek, start_pos, end_pos),
                        daemon=True
                    ).start()

            elif key.char == 'h':
                overlay.toggle()
                
            elif key.char == 'c':
                overlay.show("Quitting...")
                overlay.root.quit()
                return False

        except AttributeError:
            pass

    print("Press 'l' to mark top-left, 'r' to mark bottom-right and OCR/DATABASE, 'd' for bottom-right and deepseek, 'h' to toggle overlay, 'c' to quit.")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# === Run Everything in Main Thread ===
if __name__ == "__main__":    
    root = tk.Tk()
    overlay = AnswerOverlay(root)
    deepseek_key = os.getenv("DEEPSEEK_KEY")
    deepseek = DeepseekApi(key=deepseek_key)
    
    overlay.show("App is running!")
    overlay.toggle()
    
    # Run the key listener in a background thread
    listener_thread = threading.Thread(target=start_listener, args=(overlay,deepseek), daemon=True)
    listener_thread.start()

    # Run the Tkinter GUI in the main thread
    root.mainloop()
