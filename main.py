from flask import Flask, render_template

from app import create_app

app = create_app()


@app.route("/")
def home():
    return render_template("index.html", message="Hello, Flask!")


if __name__ == "__main__":
    app.run(debug=False)
