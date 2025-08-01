"""An API for handling marine experiments."""

from datetime import datetime

from flask import Flask, jsonify, request
from psycopg2 import sql

from database_functions import get_db_connection, get_subject, get_experiment, delete


app = Flask(__name__)

"""
For testing reasons; please ALWAYS use this connection. 

- Do not make another connection in your code
- Do not close this connection

If you do not understand this instructions; as a coach to explain
"""
conn = get_db_connection("marine_experiments")


@app.get("/")
def home():
    """Returns an informational message."""
    return jsonify({
        "designation": "Project Armada",
        "resource": "JSON-based API",
        "status": "Classified"
    })


@app.route("/subject", methods=["GET"])
def subject():
    if request.method == "GET":
        subjects = get_subject(conn)
        return subjects, 200


@app.route("/experiment", methods=["GET", "POST"])
def experiment():
    if request.method == "GET":
        numbers = [
            "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
            "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
            "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
            "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
            "41", "42", "43", "44", "45", "46", "47", "48", "49", "50",
            "51", "52", "53", "54", "55", "56", "57", "58", "59", "60",
            "61", "62", "63", "64", "65", "66", "67", "68", "69", "70",
            "71", "72", "73", "74", "75", "76", "77", "78", "79", "80",
            "81", "82", "83", "84", "85", "86", "87", "88", "89", "90",
            "91", "92", "93", "94", "95", "96", "97", "98", "99", "100"
        ]

        type_experiment = request.args.get("type", None)
        score_over = request.args.get("score_over")
        if type_experiment:
            if type_experiment.lower() not in {'intelligence', 'obedience', 'aggression'}:
                return {"error": "Invalid value for 'type' parameter"}, 400

        if score_over:
            if score_over not in numbers:
                return {"error": "Invalid value for 'score_over' parameter"}, 400

        experiments = get_experiment(conn, type_experiment, score_over)
        return experiments, 200

    if request.method == "POST":
        data = request.json
        if not data['subject_id']:
            return {"error": "Invalid value for 'subject_id' parameter"}, 400


@app.route("/experiment/<id>", methods=["DELETE"])
def delete_movie(id):
    result = delete(conn, id)
    id = int(id)
    if result == False:
        return {"error": f"Unable to locate experiment with {id} x."}, 404
    return {
        "experiment_id": id,
        "experiment_date": f"{result}"
    }, 200


if __name__ == "__main__":
    app.config["DEBUG"] = True
    app.config["TESTING"] = True

    app.run(port=8000, debug=True)

    conn.close()
