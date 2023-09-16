from flask import Flask, render_template

app = Flask(__name__)


@app.get("/", endpoint="index")
def get_index():
    return render_template("index.html")


@app.get("/about/", endpoint="about")
def get_about():
    return render_template("base.html")
