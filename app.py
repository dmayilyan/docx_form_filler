from flask import Flask, request

from form_filler import process_docs

app = Flask(__name__)


@app.route("/")
@app.route("/generate_cert", methods=["GET", "POST"])
def start():
    payload = request.get_json()
    process_docs(payload)

    return "done\n"


if __name__ == "__main__":
    app.run(host="localhost", port=8085, threaded=True)
