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
        type = request.args.get("type",)
        score_over = request.args.get("score_over")
        if type:
            if type.lower() not in {'intelligence', 'obedience', 'aggression'}:
                return {"error": "Invalid value for 'type' parameter"}, 400

        if score_over:
            if score_over not in range(0, 101):
                return {"error": "Invalid value for 'score_over' parameter"}, 400

        experiments = get_experiment(conn)
        return experiments, 200

    # if request.method == "POST":


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
