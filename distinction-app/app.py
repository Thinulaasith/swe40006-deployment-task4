import os
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ title }}</title>
  <style>
    body { font-family: Arial, sans-serif; background: #eef2f7; margin: 0; color: #17243a; }
    main { max-width: 560px; margin: 70px auto; padding: 32px; background: white;
           border-radius: 16px; box-shadow: 0 8px 30px #17243a18; }
    h1 { margin-top: 0; color: #174ea6; }
    input, button { padding: 12px; font-size: 16px; }
    input { width: 140px; }
    button { background: #174ea6; color: white; border: 0; border-radius: 6px; cursor: pointer; }
    .result { margin-top: 24px; padding: 16px; background: #e9f4ea; border-radius: 8px; }
    .error { color: #b42318; }
  </style>
</head>
<body>
  <main>
    <h1>{{ title }}</h1>
    <p>Enter your focus time to plan 25-minute study blocks.</p>
    <form method="post">
      <label for="minutes">Focus minutes:</label>
      <input id="minutes" name="minutes" type="number" min="25" max="600" required>
      <button type="submit">Create plan</button>
    </form>
    {% if error %}<p class="error">{{ error }}</p>{% endif %}
    {% if result %}
    <div class="result">
      <strong>Your study plan</strong>
      <p>Focus time: {{ result.minutes }} minutes</p>
      <p>Study blocks: {{ result.blocks }}</p>
      <p>Break time: {{ result.break_time }} minutes</p>
      <p>Total planned time: {{ result.total }} minutes</p>
    </div>
    {% endif %}
  </main>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None
    if request.method == "POST":
        minutes = request.form.get("minutes", type=int)
        if minutes is None or not 25 <= minutes <= 600:
            error = "Enter a number between 25 and 600."
        else:
            blocks = (minutes + 24) // 25
            break_minutes = int(os.getenv("BREAK_MINUTES", "5"))
            break_time = max(0, blocks - 1) * break_minutes
            result = {
                "minutes": minutes,
                "blocks": blocks,
                "break_time": break_time,
                "total": minutes + break_time,
            }
    return render_template_string(
        PAGE,
        title=os.getenv("APP_TITLE", "Focus Planner"),
        result=result,
        error=error,
    )

@app.get("/health")
def health():
    return jsonify(status="healthy")
