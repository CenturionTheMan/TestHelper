# Overview

Test Helper is a Python application that assists with answering single/multiple-choice questions by:

1. Searching a local database of pre-defined questions
2. Using AI (DeepSeek API) to generate answers for new questions

The application features:

- Screen region capture using hotkeys
- OCR text extraction from screenshots
- Overlay display of answers
- Both database lookup and AI-generated responses
- Toggleable transparent overlay

# Features

- **Database Matching:** Finds similar questions in your local database
- **AI Assistance:** Uses DeepSeek API to generate answers for unfamiliar questions
- **Hotkey Controls:** Simple keyboard shortcuts for all operations
- **Transparent Overlay:** Non-intrusive answer display that stays on top of other windows

# Installation

1. **Install Python 3.10+**
   - Download from [python.org](https://www.python.org/)
2. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/test-helper.git
   cd test-helper
   ```
3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Install Tesseract OCR**

   - Windows: [Installation guide](https://github.com/UB-Mannheim/tesseract/wiki)
   - Mac: `brew install tesseract`
   - Linux: `sudo apt install tesseract-ocr` and `sudo apt-get install tesseract-ocr-{language code here}` (e.g., `tesseract-ocr-pol` for Polish)

   Ensure Tesseract is in your system PATH.

5. **Setup OpenRouter**
   - Create free account at [OpenRouter](https://openrouter.ai/)
   - Generate API key
6. **Set up environment variables**

   Create a .env file in the project root:

   ```env
   DEEPSEEK_KEY=your_openrouter_api_key_here
   ```

# Usage

1. **Prepare your question database:**

   - Place question files in `./data/` directory
   - File format:
     - Correct answer map: X{followed by ones and zeros where one indicate correl answer}
     - Question text
     - Answers in order separated by '\n'
   - File example:

   ```text
   X0100
   Question text here?
   Answer A
   Answer B (correct)
   Answer C
   Answer D
   ```

2. **Run the application:**

```bash
python TestHelper.py
```

3. **Hotkeys:**

- `l`: Set top-left corner of capture area
- `r`: Set bottom-right corner and search database
- `d`: Set bottom-right corner and query DeepSeek AI
- `h`: Toggle answer overlay visibility
- `c`: Exit application

4. **Workflow**

- Press `l` at the top-left of the question area
- Press `r` at the bottom-right to search your database
- For unfamiliar questions, press `d` instead to get AI-generated answers
- Answers appear in a semi-transparent overlay
- Toggle overlay visibility with `h`

# Project Structure

```text
test-helper/
├── data/                   # Question database
│   ├── 123.txt             # Example question file
│   └── 124.txt             # Example question file
|── src/                    # Source code
|   ├── classes/            # Classes directory
|   |   ├── DeepseekApi.py  # DeepSeek API interface
|   |   └── Question.py     # Question class definition
|   └── TestHelper.py       # Main application
├── .env                    # API key configuration
├── config.json             # Application configuration file
└── requirements.txt        # Dependencies
```

# Notes

- The application requires an internet connection for AI functionality

- Database matching works best with exact or near-exact question matches

- AI responses may take 5-15 seconds to generate

- Edit application via `config.json` file

- For best OCR results:

  - Use high-contrast text

  - Capture clean screenshots

  - Avoid distorted or stylized fonts

**_Important:_** Ensure compliance with academic integrity policies when using this tool. The application is intended for study assistance only.
