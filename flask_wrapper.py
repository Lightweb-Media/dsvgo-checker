import json
from flask import Flask

app = Flask(__name__)

@app.route("/", methods = ["GET"])
def hello():
    response = {"message":"Hello Flask.!!"}
    return json.dumps(response)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9090, debug=True)