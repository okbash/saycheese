from flask import Flask
from flask import render_template
from flask import request
from flask import Response
from base64 import b64decode
from glob import glob
import threading
from pyngrok import ngrok
import requests


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", server="http://localhost:3000")


@app.route("/image", methods=["POST"])
def image():
    data = request.form.get("image")
    data = data.replace("data:image/png;base64,", "").replace(" ", "+")
    with open("IMG_{}.png".format(len(glob("*.png")) + 1), "wb+") as f:
        f.write(b64decode(data))

    response = Response("OK")
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


def forward_port(port):
    while True:
        try:
            r = requests.get(f"http://localhost:{port}")
            if r.ok:
                break
        except requests.exceptions.ConnectionError:
            pass
    tunnel = ngrok.connect(port)
    print(f"\nForwarding localhost:{port} server, using Ngrok...")
    print(f"http://localhost:{port} -> {tunnel.public_url.replace('http://', 'https://')}")


if __name__ == "__main__":
    forward = threading.Thread(target=forward_port, args=(3000,))
    forward.start()
    app.run(port=3000, debug=False)
