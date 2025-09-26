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
            "SELECT u.id_usuario, u.nombre, u.contrasena, t.telefono, c.correo FROM usuario u LEFT JOIN telefono t ON u.id_usuario = t.id_us LEFT JOIN correo c ON u.id_usuario = c.id_us ORDER BY u.id_usuario",
            (usuario_id,)
        ).fetchone()
    if fila is None:
        return jsonify(error="Usuario no encontrado"), 404
    return jsonify(dict(fila)), 200

# -------- POST: crear --------
#TABLA USUARIO
@app.route("/crear/usuario", methods=["POST"])
def crear_usuario():
    if not request.is_json:
        return jsonify(error="Content-Type debe ser application/json"), 415

    data = request.get_json(silent=True)
    if data is None:
        return jsonify(error="JSON malformado o vacío"), 400

    nombre = data.get("nombre")
    contrasena = data.get("contrasena")
    telefono = data.get("telefono")
    correo = data.get("correo")

    faltan = [k for k in ("nombre", "contrasena","telefono", "correo") if k not in data]
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
    
    if not isinstance(telefono, str):
        return jsonify(error="telefono debe ser string"), 422
    telefono = telefono.strip()
    if not telefono or len(telefono) > 100:
        return jsonify(error="telefono no puede estar vacía (<= 100 chars)"), 422
    
    if not isinstance(correo, str):
        return jsonify(error="correo debe ser string"), 422
    correo = correo.strip()
    if not correo or len(correo) > 100:
        return jsonify(error="correo no puede estar vacía (<= 100 chars)"), 422

    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO usuario (nombre, contrasena) VALUES (?, ?)",
            (nombre, contrasena)
        )
        nuevo_id = cur.lastrowid

        cur = conn.execute(
            "INSERT INTO telefono (id_us, telefono) VALUES (?, ?)",
            (nuevo_id, telefono)
        )
        cur = conn.execute(
            "INSERT INTO correo (id_us, correo) VALUES (?, ?)",
            (nuevo_id, correo)
        )

    resp = jsonify({"id_usuario": nuevo_id, "nombre": nombre, "contrasena": contrasena, "correo":correo, "telefono": telefono})
    resp.status_code = 201
    resp.headers["Location"] = f"/usuarios/{nuevo_id}"
    return resp

#TABLA PROVEDOR
@app.route("/crear/proveedor", methods=["POST"])
def crear_proveedor():
    if not request.is_json:
        return jsonify(error="Content-Type debe ser application/json"), 415

    data = request.get_json(silent=True)
    if data is None:
        return jsonify(error="JSON malformado o vacío"), 400

    nombre = data.get("nombre")
    telefono = data.get("telefono")
    correo = data.get("correo")

    faltan = [k for k in ("nombre", "telefono", "correo") if k not in data]
    if faltan:
        return jsonify(error=f"Faltan campos: {', '.join(faltan)}"), 400

    if not isinstance(nombre, str):
        return jsonify(error="nombre debe ser string"), 422
    nombre = nombre.strip()
    if not nombre or len(nombre) > 100:
        return jsonify(error="nombre no puede estar vacío (<= 100 chars)"), 422
    
    if not isinstance(telefono, str):
        return jsonify(error="telefono debe ser string"), 422
    telefono = telefono.strip()
    if not telefono or len(telefono) > 100:
        return jsonify(error="telefono no puede estar vacía (<= 100 chars)"), 422
    
    if not isinstance(correo, str):
        return jsonify(error="correo debe ser string"), 422
    correo = correo.strip()
    if not correo or len(correo) > 100:
        return jsonify(error="correo no puede estar vacía (<= 100 chars)"), 422

    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO proveedor (nombre) VALUES (?)",
            (nombre,)
        )
        nuevo_id = cur.lastrowid

        cur = conn.execute(
            "INSERT INTO telefono_proveedor (id_proveedor, telefono) VALUES (?, ?)",
            (nuevo_id, telefono)
        )
        cur = conn.execute(
            "INSERT INTO correo_proveedor (id_proveedor, correo) VALUES (?, ?)",
            (nuevo_id, correo)
        )

    resp = jsonify({"id_usuario": nuevo_id, "nombre": nombre, "correo":correo, "telefono": telefono})
    resp.status_code = 201
    resp.headers["Location"] = f"/proveedores/{nuevo_id}"
    return resp

#TABLA CANCION
@app.route("/crear/cancion", methods=["POST"])
def crear_cancion():
    if not request.is_json:
        return jsonify(error="Content-Type debe ser application/json"), 415

    data = request.get_json(silent=True)
    if data is None:
        return jsonify(error="JSON malformado o vacío"), 400

    nombre = data.get("nombre")
    duracion = data.get("duracion")
    tamano = data.get("tamano")

    faltan = [k for k in ("nombre", "duracion", "tamano") if k not in data]
    if faltan:
        return jsonify(error=f"Faltan campos: {', '.join(faltan)}"), 400

    if not isinstance(nombre, str):
        return jsonify(error="nombre debe ser string"), 422
    nombre = nombre.strip()
    if not nombre or len(nombre) > 100:
        return jsonify(error="nombre no puede estar vacío (<= 100 chars)"), 422
    
    if not isinstance(duracion, str):
        return jsonify(error="duracion debe ser string"), 422
    duracion = duracion.strip()
    if not duracion or len(duracion) > 100:
        return jsonify(error="duracion no puede estar vacía (<= 100 chars)"), 422
    
    if not isinstance(tamano, str):
        return jsonify(error="tamano debe ser string"), 422
    tamano = tamano.strip()
    if not tamano or len(tamano) > 100:
        return jsonify(error="tamano no puede estar vacía (<= 100 chars)"), 422

    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO cancion (nombre, duracion, tamano) VALUES (?, ?, ?)",
            (nombre, duracion, tamano)
        )
        nuevo_id = cur.lastrowid

    resp = jsonify({"id_cancion": nuevo_id, "nombre": nombre, "duracion":duracion, "tamano": tamano})
    resp.status_code = 201
    resp.headers["Location"] = f"/canciones/{nuevo_id}"
    return resp

if __name__ == "__main__":
    app.run(debug=True)
