import numpy as np

class Question:
    def __init__(self, id, raw_text: str):
        self.id = id
        self.raw_text = raw_text
        lines = raw_text.split('\n')
        lines = [l.strip() for l in lines if l.strip() != '']
        self.question = lines[1].strip()
        self.all_answers = np.array(lines[2:])
        
        ans_arr = []
        self.correct_answers = []
        for x in lines[0]:
            if x == 'X' or x == 'x':
                continue
            elif x != '1':
                ans_arr.append(0)
            else:
                ans_arr.append(1)
        ans_arr = np.array(ans_arr)
        
        self.correct_answers = self.all_answers[ans_arr == 1]
        
        