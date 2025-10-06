from flask import Flask, jsonify, request, render_template
from simulation.model import BookstoreModel

app = Flask(__name__)
model = BookstoreModel()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/initialize", methods=["POST"])
def initialize():
    data = request.json
    num_customers = int(data.get("customers", 10))
    num_employees = int(data.get("employees", 3))
    num_books = int(data.get("books", 10))
    model.initialize(num_customers, num_employees, num_books)
    return jsonify({"status": "success", "message": "Simulation initialized"})

@app.route("/api/start", methods=["POST"])
def start():
    model.start()
    return jsonify({"status": "success", "message": "Simulation started"})

@app.route("/api/stop", methods=["POST"])
def stop():
    model.stop()
    return jsonify({"status": "success", "message": "Simulation stopped"})

@app.route("/api/step", methods=["POST"])
def step():
    model.step()
    return jsonify({"status": "success", "message": "Step executed"})

@app.route("/api/stats", methods=["GET"])
def stats():
    return jsonify(model.get_stats())

@app.route("/api/books", methods=["GET"])
def books():
    return jsonify(model.get_books())

@app.route("/api/customers", methods=["GET"])
def customers():
    return jsonify(model.get_customers())

@app.route("/api/employees", methods=["GET"])
def employees():
    return jsonify(model.get_employees())

@app.route("/api/history", methods=["GET"])
def history():
    return jsonify(model.get_history())

if __name__ == "__main__":
    app.run(debug=True)
