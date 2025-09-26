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
            "SELECT u.id_usuario, u.nombre, u.contrasena, t.telefono, c.correo FROM usuario u LEFT JOIN telefono t ON u.id_usuario = t.id_us LEFT JOIN correo c ON u.id_usuario = c.id_us ORDER BY u.id_usuario"
            ).fetchall()
    items = [dict(f) for f in filas]
    return jsonify(items), 200

if __name__ == "__main__":
    app.run(debug=True)
    print("Hola Mundo")