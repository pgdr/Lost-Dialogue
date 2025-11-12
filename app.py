# app.py
from flask import Flask, request, jsonify, render_template_string
import lost_dialogue

app = Flask(__name__)

HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Plato's Lost Dialogue</title>
  <style>
    :root { --gray:#c8c8c8; --lgray:#e6e6e6; --blue:#0078d7; --black:#000; --white:#fff; }
    body { font-family: system-ui, sans-serif; background: var(--white); margin: 0; padding: 24px; }
    .container { max-width: 1100px; margin: 0 auto; }
    label { display:block; font-size:14px; margin-bottom:6px; color: var(--black); }
    .row { display:flex; gap: 20px; }
    .box, .field { background: var(--lgray); border: 1px solid var(--gray); border-radius: 6px; padding: 10px; }
    .box { width: 100%; min-height: 160px; }
    textarea { width:100%; height:140px; border:none; background:transparent; resize:vertical; outline:none; font: 16px/1.4 system-ui, sans-serif; color:var(--black); }
    .grid { display:grid; grid-template-columns: 1fr 1fr; gap: 20px; }
    .inputs { margin-top: 20px; display:grid; grid-template-columns: 1fr 1fr; gap: 20px; }
    .field input { width:100%; border:none; background:transparent; outline:none; font: 16px system-ui, sans-serif; color: var(--black); padding: 4px 0; }
    .actions { margin-top: 20px; display:flex; justify-content:flex-end; }
    button { background: var(--blue); color: var(--white); border:none; border-radius: 8px; padding: 10px 18px; font: 16px system-ui, sans-serif; cursor:pointer; }
    button[disabled] { opacity: 0.6; cursor: default; }
    .hint { font-size: 12px; color: #555; margin-top: 6px; }
  </style>
</head>
<body>
  <div class="container">
    <div class="grid">
      <div>
        <label for="input">Input</label>
        <div class="box">
          <textarea id="input" placeholder="Enter prompt.">Enter prompt.</textarea>
        </div>
        <div class="hint">Press Ctrl+Enter to submit.</div>
      </div>
      <div>
        <label for="output">Output</label>
        <div class="box">
          <textarea id="output" readonly></textarea>
        </div>
      </div>
    </div>

    <div class="inputs">
      <div class="field">
        <label for="sender">Sender</label>
        <input id="sender" value="Ninja" />
      </div>
      <div class="field">
        <label for="receiver">Receiver</label>
        <input id="receiver" value="Princess" />
      </div>
      <div class="field">
        <label for="mood">Mood</label>
        <input id="mood" value="Happy" />
      </div>
    </div>

    <div class="actions">
      <button id="submit">Submit</button>
    </div>
  </div>

  <script>
    const $ = (id) => document.getElementById(id);
    const input = $("input");
    const output = $("output");
    const sender = $("sender");
    const receiver = $("receiver");
    const mood = $("mood");
    const submitBtn = $("submit");

    async function generate() {
      submitBtn.disabled = true;
      output.value = "";
      try {
        const res = await fetch("/generate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            input: input.value,
            sender: sender.value,
            receiver: receiver.value,
            mood: mood.value
          })
        });
        const data = await res.json();
        output.value = data.output || "";
      } catch (e) {
        output.value = "Error: " + (e?.message || "unknown");
      } finally {
        submitBtn.disabled = false;
      }
    }

    submitBtn.addEventListener("click", generate);
    input.addEventListener("keydown", (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === "Enter") generate();
    });
  </script>
</body>
</html>
"""


@app.get("/")
def index():
    return render_template_string(HTML)


@app.post("/generate")
def generate():
    data = request.get_json(force=True) or {}
    prompt = data.get("input", "") or ""
    sender = data.get("sender", "") or ""
    receiver = data.get("receiver", "") or ""
    mood = data.get("mood", "") or ""

    text = lost_dialogue.main(mood, sender, receiver, prompt)
    return jsonify({"output": text})


if __name__ == "__main__":
    app.run(debug=True)
