from flask import Flask, request, jsonify
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB_PATH = Path(__file__).with_name("PoliSong.db")

# -------- utilidades de BD --------
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def ensure_schema():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS usuario (
                id_usuario  INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre      TEXT NOT NULL,
                contrasena  TEXT NOT NULL
            );
        """)

ensure_schema()

# -------- GET: detalle --------
@app.route("/usuarios/<int:usuario_id>", methods=["GET"])
def detalle_usuario(usuario_id):
    with get_conn() as conn:
        fila = conn.execute(
            "SELECT id_usuario, nombre, contrasena FROM usuario WHERE id_usuario = ?",
            (usuario_id,)
        ).fetchone()
    if fila is None:
        return jsonify(error="Usuario no encontrado"), 404
    return jsonify(dict(fila)), 200

# -------- POST: crear --------
@app.route("/crear", methods=["POST"])
def crear_usuario():
    if not request.is_json:
        return jsonify(error="Content-Type debe ser application/json"), 415

    data = request.get_json(silent=True)
    if data is None:
        return jsonify(error="JSON malformado o vacío"), 400

    nombre = data.get("nombre")
    contrasena = data.get("contrasena")

    faltan = [k for k in ("nombre", "contrasena") if k not in data]
    if faltan:
        return jsonify(error=f"Faltan campos: {', '.join(faltan)}"), 400

    if not isinstance(nombre, str):
        return jsonify(error="nombre debe ser string"), 422
    nombre = nombre.strip()
    if not nombre or len(nombre) > 100:
        return jsonify(error="nombre no puede estar vacío (<= 100 chars)"), 422

    if not isinstance(contrasena, str):
        return jsonify(error="contrasena debe ser string"), 422
    contrasena = contrasena.strip()
    if not contrasena or len(contrasena) > 100:
        return jsonify(error="contrasena no puede estar vacía (<= 100 chars)"), 422

    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO usuario (nombre, contrasena) VALUES (?, ?)",
            (nombre, contrasena)
        )
        nuevo_id = cur.lastrowid

    resp = jsonify({"id_usuario": nuevo_id, "nombre": nombre, "contrasena": contrasena})
    resp.status_code = 201
    resp.headers["Location"] = f"/usuarios/{nuevo_id}"
    return resp
