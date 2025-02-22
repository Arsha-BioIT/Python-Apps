from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/how-to-use")
def how_to_use():
    return render_template("how_to_use.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/history")
def history():
    return render_template("history.html")

@app.route("/why-probiotics")
def why_probiotics():
    return render_template("why_probiotics.html")

if __name__ == "__main__":
    app.run(debug=True)
