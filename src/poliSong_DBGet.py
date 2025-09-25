from flask import Flask, jsonify
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB_PATH = Path(__file__).with_name("PoliSong.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/usuario", methods=["GET"])
def listar_usuarios():
    with get_conn() as conn:
        filas = conn.execute(
            "SELECT * FROM usuario ORDER BY id_usuario"
            ).fetchall()
    items = [dict(f) for f in filas]
    return jsonify(items), 200

if __name__ == "__main__":
    app.run(debug=True)