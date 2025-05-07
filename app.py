from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

LIBRETRANSLATE_URL = "https://libretranslate.de/translate"  # Free instance

# Optional homepage with simple HTML form
@app.route("/", methods=["GET"])
def home():
    return render_template_string('''
        <h2>LibreTranslate API</h2>
        <form action="/translate" method="post">
            <label>Text:</label><br>
            <input name="q" value="Hello"><br>
            <label>Source language (e.g., en):</label><br>
            <input name="source" value="en"><br>
            <label>Target language (e.g., es):</label><br>
            <input name="target" value="es"><br><br>
            <input type="submit" value="Translate">
        </form>
    ''')

@app.route("/translate", methods=["GET", "POST"])
def translate():
    if request.method == "GET":
        return "Send a POST request with JSON body or use the HTML form at `/`."

    if request.content_type == 'application/json':
        data = request.get_json()
    else:
        # Fallback for form data (from browser form)
        data = {
            "q": request.form.get("q"),
            "source": request.form.get("source"),
            "target": request.form.get("target")
        }

    if not data or "q" not in data or "source" not in data or "target" not in data:
        return jsonify({"error": "Missing parameters"}), 400

    try:
        response = requests.post(LIBRETRANSLATE_URL, json={
            "q": data["q"],
            "source": data["source"],
            "target": data["target"],
            "format": "text"
        })

        return jsonify(response.json())

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

