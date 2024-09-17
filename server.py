from flask import Flask, render_template, request
import os

def create_app(config=None):
    app = Flask(__name__, static_url_path='', static_folder="static")
    app.config.update(dict(DEBUG=True))
    app.config.update(config or {})

    @app.route("/game")
    def game():
        username = request.args.get("username_input")
        password = request.args.get("password_input")
        return render_template("game.html", username = username, password = password)

    @app.route("/login")
    def login():
        return render_template("login.html")
    
    return app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app = create_app()
    app.run(host="0.0.0.0", port=port)

