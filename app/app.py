from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "CI/CD Pipeline Running Successfully on 04/03/2026 by sahilmahat hey how are you"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
