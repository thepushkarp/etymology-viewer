from flask import Flask, request, jsonify
import ety

app = Flask(__name__)


# Default route
@app.route("/")
def home():
    return "Etymology Viewer Backend"


# Gets the origin of a word
@app.get("/origin/")
@app.get("/origin/<string:word>")
def origin(word: str = ""):
    try:
        recursive = request.args.get("recursive") == "True"
        results = ety.origins(word, recursive=recursive)
        response = [result.pretty for result in results]
        return jsonify(response)
    except:
        return jsonify([])


# Gets the etymological tree of a word
@app.get("/tree/")
@app.get("/tree/<string:word>")
def tree(word: str = ""):
    try:
        response = ety.tree(word).to_dict()
        return jsonify(response)
    except:
        return jsonify({})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
