from __future__ import annotations

import random
from typing import Iterable

from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

KNOWLEDGE_BASE = [
    {
        "keywords": ["html", "web page", "structure", "markup"],
        "response": (
            "HTML gives a web page its structure. It defines headings, paragraphs, "
            "buttons, images, and the other building blocks that a browser displays."
        ),
    },
    {
        "keywords": ["css", "style", "colors", "layout", "design"],
        "response": (
            "CSS controls how a web page looks. You use it to set colors, spacing, "
            "fonts, positioning, and responsive layouts."
        ),
    },
    {
        "keywords": ["javascript", "js", "interactive", "logic", "dynamic"],
        "response": (
            "JavaScript adds behavior to a website. It lets you respond to clicks, "
            "validate forms, update content, and build interactive features like this chatbot."
        ),
    },
    {
        "keywords": ["focus", "concentrate", "distraction", "study habit"],
        "response": (
            "A good focus routine is to study in short blocks, silence notifications, "
            "keep one task in front of you, and take a short break before your attention drops."
        ),
    },
    {
        "keywords": ["time", "schedule", "plan", "deadline", "manage"],
        "response": (
            "Try listing your top three tasks for the day, estimating how long each one "
            "will take, and starting with the hardest task while your energy is highest."
        ),
    },
    {
        "keywords": ["revise", "revision", "remember", "memorize", "exam"],
        "response": (
            "For revision, active recall works well. Close your notes, write what you "
            "remember, then compare and fill the gaps instead of only rereading."
        ),
    },
]

JOKES = [
    "Why did the student eat the homework? Because the teacher said it was a piece of cake.",
    "Why do programmers mix up Halloween and Christmas? Because OCT 31 equals DEC 25.",
    "Why was the math book stressed? It had too many problems.",
]

FALLBACK_REPLIES = [
    "I'm not fully sure about that one yet, but I can help with study tips, basic web concepts, or a quick joke.",
    "That's outside my tiny knowledge base right now. Try asking about HTML, CSS, JavaScript, focus, revision, or time management.",
    "I'm still a small local chatbot, so I do best with study support and beginner web-development questions.",
]

PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>StudyBuddy Chatbot</title>
  <style>
    :root {
      --bg: #f4efe7;
      --panel: rgba(255, 252, 246, 0.88);
      --panel-strong: #fffaf2;
      --line: rgba(105, 81, 53, 0.14);
      --text: #2f2419;
      --muted: #685748;
      --accent: #b5542f;
      --accent-dark: #8f3f20;
      --bot: #fff3dd;
      --user: #2f2419;
      --shadow: 0 24px 60px rgba(74, 50, 29, 0.12);
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      min-height: 100vh;
      font-family: "Segoe UI", Tahoma, sans-serif;
      color: var(--text);
      background:
        radial-gradient(circle at top left, rgba(255, 208, 141, 0.55), transparent 28%),
        radial-gradient(circle at bottom right, rgba(163, 214, 204, 0.55), transparent 26%),
        linear-gradient(135deg, #f8f3eb 0%, #efe7db 100%);
    }

    .page-shell {
      width: min(1180px, calc(100% - 32px));
      margin: 24px auto;
      display: grid;
      grid-template-columns: 340px 1fr;
      gap: 24px;
    }

    .info-panel,
    .chat-panel {
      border: 1px solid var(--line);
      border-radius: 28px;
      background: var(--panel);
      box-shadow: var(--shadow);
    }

    .info-panel {
      padding: 28px;
    }

    .chat-panel {
      padding: 22px;
      display: flex;
      flex-direction: column;
      min-height: 82vh;
    }

    .eyebrow {
      margin: 0 0 8px;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      font-size: 0.75rem;
      color: var(--accent);
      font-weight: 700;
    }

    h1,
    h2 {
      margin: 0;
      line-height: 1;
    }

    h1 {
      font-size: clamp(2.2rem, 5vw, 3.3rem);
    }

    h2 {
      font-size: 1.35rem;
    }

    .intro {
      margin: 18px 0 24px;
      font-size: 1.08rem;
      line-height: 1.55;
      color: var(--muted);
    }

    .panel-card {
      background: var(--panel-strong);
      border: 1px solid var(--line);
      border-radius: 22px;
      padding: 18px;
      margin-top: 16px;
    }

    .panel-card p {
      margin: 10px 0 0;
      color: var(--muted);
      line-height: 1.5;
    }

    .prompt-list {
      margin: 12px 0 0;
      padding-left: 18px;
      color: var(--muted);
    }

    .prompt-list li + li {
      margin-top: 10px;
    }

    .chat-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding-bottom: 18px;
      border-bottom: 1px solid var(--line);
    }

    .chat-window {
      flex: 1;
      overflow-y: auto;
      padding: 22px 4px;
    }

    .message {
      display: flex;
      gap: 12px;
      margin-bottom: 16px;
      align-items: flex-start;
    }

    .message.user {
      flex-direction: row-reverse;
    }

    .avatar {
      width: 42px;
      height: 42px;
      border-radius: 14px;
      display: grid;
      place-items: center;
      font-weight: 700;
      flex-shrink: 0;
    }

    .bot .avatar {
      background: #ffd8a5;
      color: #6a351d;
    }

    .user .avatar {
      background: #3b2e22;
      color: #fff6ec;
    }

    .bubble {
      max-width: min(720px, 84%);
      padding: 14px 16px;
      border-radius: 20px;
      line-height: 1.55;
      white-space: pre-wrap;
    }

    .bot .bubble {
      background: var(--bot);
      border-top-left-radius: 6px;
    }

    .user .bubble {
      background: var(--user);
      color: #fff8f0;
      border-top-right-radius: 6px;
    }

    .chat-form {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 12px;
      padding-top: 18px;
      border-top: 1px solid var(--line);
    }

    input {
      width: 100%;
      border: 1px solid rgba(105, 81, 53, 0.18);
      border-radius: 18px;
      padding: 15px 18px;
      font: inherit;
      color: var(--text);
      background: rgba(255, 255, 255, 0.88);
    }

    input:focus {
      outline: 2px solid rgba(181, 84, 47, 0.24);
      border-color: rgba(181, 84, 47, 0.45);
    }

    button {
      border: 0;
      border-radius: 18px;
      padding: 14px 18px;
      font: inherit;
      font-weight: 600;
      cursor: pointer;
      transition: transform 160ms ease, background 160ms ease;
    }

    button:hover {
      transform: translateY(-1px);
    }

    .primary-button {
      background: var(--accent);
      color: #fff7f1;
    }

    .primary-button:hover {
      background: var(--accent-dark);
    }

    .secondary-button {
      background: rgba(105, 81, 53, 0.08);
      color: var(--text);
    }

    .secondary-button:hover {
      background: rgba(105, 81, 53, 0.14);
    }

    .sr-only {
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border: 0;
    }

    @media (max-width: 900px) {
      .page-shell {
        grid-template-columns: 1fr;
      }

      .chat-panel {
        min-height: 70vh;
      }
    }

    @media (max-width: 640px) {
      .page-shell {
        width: min(100% - 20px, 100%);
        margin: 10px auto;
      }

      .info-panel,
      .chat-panel {
        border-radius: 24px;
      }

      .chat-header,
      .chat-form {
        grid-template-columns: 1fr;
      }

      .bubble {
        max-width: 100%;
      }

      .secondary-button,
      .primary-button {
        width: 100%;
      }
    }
  </style>
</head>
<body>
  <div class="page-shell">
    <aside class="info-panel">
      <p class="eyebrow">Flask Rule-Based Chatbot</p>
      <h1>StudyBuddy</h1>
      <p class="intro">
        A friendly study coach that can greet you, answer a few learning questions,
        share productivity tips, and tell the occasional joke.
      </p>

      <div class="panel-card">
        <h2>What makes it unique?</h2>
        <p>
          StudyBuddy runs through a single Python file, uses rule-based intent matching,
          and responds instantly without any API key or external model.
        </p>
      </div>

      <div class="panel-card">
        <h2>Try asking</h2>
        <ul class="prompt-list">
          <li>"How do I stay focused while studying?"</li>
          <li>"Explain what HTML does."</li>
          <li>"Tell me a joke."</li>
          <li>"What is CSS used for?"</li>
        </ul>
      </div>
    </aside>

    <main class="chat-panel">
      <section class="chat-header">
        <div>
          <p class="eyebrow">Live Demo</p>
          <h2>Chat with StudyBuddy</h2>
        </div>
        <button id="clear-chat" class="secondary-button" type="button">Clear chat</button>
      </section>

      <section id="chat-window" class="chat-window" aria-live="polite">
        <article class="message bot">
          <div class="avatar">S</div>
          <div class="bubble">
            Hi! I'm StudyBuddy. Ask me about study habits, basic web concepts, or just ask for a joke.
          </div>
        </article>
      </section>

      <form id="chat-form" class="chat-form">
        <label class="sr-only" for="user-input">Type your message</label>
        <input
          id="user-input"
          name="message"
          type="text"
          placeholder="Type your message here..."
          autocomplete="off"
          required
        >
        <button class="primary-button" type="submit">Send</button>
      </form>
    </main>
  </div>

  <script>
    const chatWindow = document.getElementById("chat-window");
    const chatForm = document.getElementById("chat-form");
    const userInput = document.getElementById("user-input");
    const clearButton = document.getElementById("clear-chat");

    function addMessage(role, text) {
      const message = document.createElement("article");
      message.className = "message " + role;

      const avatar = document.createElement("div");
      avatar.className = "avatar";
      avatar.textContent = role === "bot" ? "S" : "Y";

      const bubble = document.createElement("div");
      bubble.className = "bubble";
      bubble.textContent = text;

      message.appendChild(avatar);
      message.appendChild(bubble);
      chatWindow.appendChild(message);
      chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    chatForm.addEventListener("submit", async function (event) {
      event.preventDefault();
      const message = userInput.value.trim();

      if (!message) {
        return;
      }

      addMessage("user", message);
      userInput.value = "";
      userInput.focus();

      try {
        const response = await fetch("/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: message })
        });

        const data = await response.json();
        addMessage("bot", data.reply || "I couldn't generate a reply right now.");
      } catch (error) {
        addMessage("bot", "Something went wrong while contacting the chatbot.");
      }
    });

    clearButton.addEventListener("click", function () {
      chatWindow.innerHTML = "";
      addMessage(
        "bot",
        "Chat cleared. Ask me about study habits, HTML, CSS, JavaScript, or ask for a joke."
      );
      userInput.focus();
    });
  </script>
</body>
</html>
"""


def normalize_text(text: str) -> str:
    cleaned = "".join(character.lower() if character.isalnum() or character.isspace() else " " for character in text)
    return " ".join(cleaned.split())


def keyword_score(normalized_message: str, tokens: Iterable[str], keyword: str) -> int:
    if keyword in normalized_message:
        return 2

    keyword_tokens = keyword.split()
    return sum(1 for token in keyword_tokens if token in tokens)


def find_knowledge_match(message: str) -> str | None:
    normalized = normalize_text(message)
    tokens = normalized.split()

    best_response = None
    best_score = 0

    for entry in KNOWLEDGE_BASE:
        score = sum(keyword_score(normalized, tokens, keyword) for keyword in entry["keywords"])
        if score > best_score:
            best_score = score
            best_response = entry["response"]

    return best_response if best_score > 0 else None


def contains_phrase(normalized_text: str, phrases: Iterable[str]) -> bool:
    padded_text = f" {normalized_text} "
    return any(f" {phrase} " in padded_text for phrase in phrases)


def build_response(message: str) -> str:
    normalized = normalize_text(message)

    if not normalized:
        return "Type a message and I'll do my best to help."

    if contains_phrase(normalized, ["hello", "hi", "hey", "good morning", "good evening"]):
        return "Hi! I'm ready to help with study tips, beginner web concepts, or a joke if you need a quick break."

    if contains_phrase(normalized, ["who are you", "what are you", "your purpose"]):
        return "I'm StudyBuddy, a rule-based chatbot built for friendly conversation, beginner learning support, and simple productivity advice."

    if contains_phrase(normalized, ["joke", "funny", "make me laugh"]):
        return random.choice(JOKES)

    if contains_phrase(normalized, ["thank you", "thanks"]):
        return "You're welcome. Keep going, and feel free to ask another question."

    if contains_phrase(normalized, ["bye", "goodbye", "see you"]):
        return "See you later! I'll be here when you want another study session."

    knowledge_reply = find_knowledge_match(normalized)
    if knowledge_reply:
        return knowledge_reply

    return random.choice(FALLBACK_REPLIES)


@app.get("/")
def home() -> str:
    return render_template_string(PAGE_TEMPLATE)


@app.post("/chat")
def chat() -> tuple[object, int] | object:
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()

    if not message:
        return jsonify({"reply": "Please type a message first."}), 400

    return jsonify({"reply": build_response(message)})


if __name__ == "__main__":
    app.run(debug=True)
