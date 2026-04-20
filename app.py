from flask import Flask, request, jsonify, render_template_string
import os
from dotenv import load_dotenv

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# ── Load env ─────────────────────────────
load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")

endpoint = "https://models.github.ai/inference"
model = "deepseek/DeepSeek-V3-0324"

# ── Create client ────────────────────────
client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(TOKEN),
)

app = Flask(__name__)

# ── AI response function ─────────────────
def ai_response(message):
    try:
        response = client.complete(
            messages=[
                SystemMessage("You are a helpful study assistant."),
                UserMessage(message),
            ],
            temperature=0.8,
            top_p=0.1,
            max_tokens=500,
            model=model
        )

        return response.choices[0].message.content

    except Exception as e:
        return "Error: " + str(e)

# ── HTML UI ─────────────────────────────
PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>StudyBuddy (GitHub DeepSeek)</title>
<style>
body {
    font-family: Arial;
    background: linear-gradient(135deg,#667eea,#764ba2);
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
}

.chat {
    width:600px;
    height:90vh;
    background:white;
    border-radius:15px;
    display:flex;
    flex-direction:column;
}

.header {
    background:#4f46e5;
    color:white;
    padding:15px;
    text-align:center;
}

.messages {
    flex:1;
    padding:10px;
    overflow-y:auto;
}

.msg {
    padding:10px;
    margin:5px;
    border-radius:10px;
    max-width:70%;
}

.user {
    background:#4f46e5;
    color:white;
    margin-left:auto;
}

.bot {
    background:#eee;
}

form {
    display:flex;
}

input {
    flex:1;
    padding:10px;
    border:none;
}

button {
    padding:10px;
    background:#4f46e5;
    color:white;
    border:none;
}
</style>
</head>

<body>

<div class="chat">
    <div class="header">🤖 StudyBuddy (DeepSeek via GitHub)</div>
    <div id="messages" class="messages"></div>

    <form id="form">
        <input id="input" placeholder="Ask something..." required>
        <button>Send</button>
    </form>
</div>

<script>
const form = document.getElementById("form");
const input = document.getElementById("input");
const messages = document.getElementById("messages");

function add(text, cls){
    const div = document.createElement("div");
    div.className = "msg " + cls;
    div.innerText = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
}

form.onsubmit = async (e)=>{
    e.preventDefault();

    const msg = input.value;
    add(msg, "user");
    input.value = "";

    add("Typing...", "bot");

    const res = await fetch("/chat", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({message: msg})
    });

    const data = await res.json();

    messages.lastChild.remove();
    add(data.reply, "bot");
};
</script>

</body>
</html>
"""

# ── Routes ───────────────────────────────
@app.route("/")
def home():
    return render_template_string(PAGE)

@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json.get("message")
    reply = ai_response(msg)
    return jsonify({"reply": reply})

# ── Run ─────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)