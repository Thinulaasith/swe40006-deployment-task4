from flask import Flask

app = Flask(__name__)

@app.get("/")
def home():
    return """
    <h1>Study Task Tracker</h1>
    <p>My Python application is running inside Docker.</p>
    <p>Status: Ready</p>
    """

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
