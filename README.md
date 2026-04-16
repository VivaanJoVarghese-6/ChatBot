# StudyBuddy Chatbot

StudyBuddy is a Flask-based chatbot designed for friendly conversation, beginner web-development questions, and study support. The entire web app now runs from `app.py`, which serves the interface and handles chatbot replies.

## Requirements

Before running the project, make sure you have:

- Python 3.10 or newer installed
- `pip` available in your terminal
- Internet access once, so `pip` can download Flask

If `python` does not work in your terminal, install Python from the official Python installer and make sure the **Add Python to PATH** option is enabled during installation.

## Setup and Run Locally

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Create a virtual environment:

```bash
python -m venv venv
```

4. Activate the virtual environment.

On Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

On Windows Command Prompt:

```cmd
venv\Scripts\activate.bat
```

5. Install the dependency:

```bash
pip install -r requirements.txt
```

6. Start the Flask app:

```bash
python app.py
```

7. Open the local URL shown in the terminal, usually `http://127.0.0.1:5000`.

## Quick Troubleshooting

- If `python` is not recognized, Python is not installed or not added to PATH yet.
- If `pip` is not recognized, try `python -m pip install -r requirements.txt` instead.
- If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the virtual environment again.
- If Flask does not install, check your internet connection and try the install command one more time.

## Approach

This chatbot uses a **rule-based approach** with a small built-in knowledge base.

- The backend checks for simple intents such as greetings, thanks, farewells, and joke requests.
- It also searches a small set of keyword-based knowledge entries to answer questions about HTML, CSS, JavaScript, focus, revision, and time management.
- If the message does not match a known intent or topic, the chatbot returns a fallback response.

## What Makes It Unique

StudyBuddy is designed to be encouraging and beginner-friendly. It focuses on a small set of useful topics instead of pretending to know everything, and it runs from a single Python file so it is easy to understand and submit.

## Files

- `app.py` contains the Flask app, chatbot logic, web interface, and chat API.
- `requirements.txt` contains the Python dependency needed to run the project.

## Challenges and How They Were Solved

One challenge was making the chatbot feel helpful without using an external AI API. That was solved by combining intent detection with a keyword-based knowledge base so the bot can still respond in a structured and friendly way.

Another challenge was keeping the project simple for local setup and submission. Putting the interface and backend together inside `app.py` made the project easier to run and easier to review.
