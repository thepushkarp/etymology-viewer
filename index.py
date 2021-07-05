from flask import Flask, request, jsonify, render_template
import ety

app = Flask(__name__)


def replace_item(obj):
    new_obj = {}
    for k, v in obj.items():
        new_obj["Item"] = {"Name": k}
        new_obj["Children"] = []
        for value in v["children"]:
            if isinstance(value, dict):
                new_obj["Children"].append(replace_item(value))
            else:
                new_obj["Children"].append({"Item": {"Name": value}})
    print(new_obj)
    return new_obj


# Default route
@app.route("/")
def home():
    return render_template("index.html")


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
        response = [replace_item(response)]
        return jsonify(response)
    except:
        return jsonify({})


if __name__ == "__main__":
    app.run(debug=True)
