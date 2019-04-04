import logging

from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/about")
def about():
    return app.send_static_file("about.html")

@app.route("/home")
def home():
    return app.send_static_file("home.html")

if __name__ == '__main__':
    app.run( debug=True)
    #host='127.0.0.1', port=8080,