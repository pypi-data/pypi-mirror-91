from afitop100 import AFITop100
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config["DEBUG"] = True

afi = AFITop100()
afi.scrape_afi_list()


@app.route("/", methods=["GET"])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


@app.route("/api/v1/resources/afitop100/all", methods=["GET"])
def api_all():
    return jsonify(afi.afi_list)


if __name__ == "__main__":
    app.run(use_reloader=False)
