# StudyBuddy AI Chatbot

A simple Flask-based chatbot with AI mode (DeepSeek via GitHub Models) and an offline rule-based fallback.

---

## Features

- ChatGPT-style UI
- AI and offline dual system
- Works without internet in offline mode
- Beginner-friendly Flask project

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/studybuddy-ai.git
cd studybuddy-ai
```

### 2. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
```

Activate it:

**Windows**
```bash
venv\Scripts\activate
```

**macOS / Linux**
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## API Setup (Optional)

Create a `.env` file:

```
GITHUB_TOKEN=your_token_here
```

If you skip this, the chatbot will still work in offline mode.

---

## Run the App

```bash
python app.py
```

Then open in your browser:

```
http://127.0.0.1:5000
```

---

## How It Works

| Mode         | Description                              |
|--------------|------------------------------------------|
| AI Mode      | Uses DeepSeek via GitHub Models          |
| Offline Mode | Uses built-in rule-based responses       |

---

## Example

```
You: What is HTML?
Bot: HTML is used to structure web pages.
```

---

## Troubleshooting

- **"Typing..." forever** — API not responding
- **Invalid token** — Check your `.env` file
- **Slow responses** — API limitation

---

## Requirements

- Flask
- python-dotenv
- azure-ai-inference
- azure-core
