from flask import Flask, jsonify, request
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB_PATH = Path(__file__).with_name("PoliSong.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ------------------- USUARIO -------------------
@app.route("/usuario", methods=["GET"])
def listar_usuarios():
    with get_conn() as conn:
        filas = conn.execute(
            """
            SELECT u.id_usuario AS id_usuario, u.nombre, u.contrasena,
                   t.telefono, c.correo
            FROM usuario u
            LEFT JOIN telefono t ON u.id_usuario = t.id_us
            LEFT JOIN correo c ON u.id_usuario = c.id_us
            ORDER BY u.id_usuario
            """
        ).fetchall()
    return jsonify([dict(f) for f in filas]), 200


@app.route("/usuario/<int:id_usuario>", methods=["GET"])
def detalle_usuario(id_usuario):
    with get_conn() as conn:
        fila = conn.execute(
            """
            SELECT u.id_usuario AS id_usuario, u.nombre, u.contrasena,
                   t.telefono, c.correo
            FROM usuario u
            LEFT JOIN telefono t ON u.id_usuario = t.id_us
            LEFT JOIN correo c ON u.id_usuario = c.id_us
            WHERE u.id_usuario = ?
            """,
            (id_usuario,)
        ).fetchone()
    if fila is None:
        return jsonify(error="Usuario no encontrado"), 404
    return jsonify(dict(fila)), 200


# ------------------- PROVEEDOR -------------------
@app.route("/proveedor", methods=["GET"])
def listar_proveedores():
    with get_conn() as conn:
        filas = conn.execute(
            """
            SELECT p.id_proveedor AS id_proveedor, p.nombre,
                   t.telefono, c.correo
            FROM proveedor p
            LEFT JOIN telefono_proveedor t ON p.id_proveedor = t.id_proveedor
            LEFT JOIN correo_proveedor c ON p.id_proveedor = c.id_proveedor
            ORDER BY p.id_proveedor
            """
        ).fetchall()
    return jsonify([dict(f) for f in filas]), 200


@app.route("/proveedor/<int:id_proveedor>", methods=["GET"])
def detalle_proveedor(id_proveedor):
    with get_conn() as conn:
        fila = conn.execute(
            """
            SELECT p.id_proveedor AS id_proveedor, p.nombre,
                   t.telefono, c.correo
            FROM proveedor p
            LEFT JOIN telefono_proveedor t ON p.id_proveedor = t.id_proveedor
            LEFT JOIN correo_proveedor c ON p.id_proveedor = c.id_proveedor
            WHERE p.id_proveedor = ?
            """,
            (id_proveedor,)
        ).fetchone()
    if fila is None:
        return jsonify(error="Proveedor no encontrado"), 404
    return jsonify(dict(fila)), 200


# ------------------- CANCION -------------------
@app.route("/cancion", methods=["GET"])
def listar_canciones():
    with get_conn() as conn:
        filas = conn.execute(
            "SELECT id_cancion AS id_cancion, nombre, duracion, tamano FROM cancion ORDER BY id_cancion"
        ).fetchall()
    return jsonify([dict(f) for f in filas]), 200


@app.route("/cancion/<int:id_cancion>", methods=["GET"])
def detalle_cancion(id_cancion):
    with get_conn() as conn:
        fila = conn.execute(
            "SELECT id_cancion AS id_cancion, nombre, duracion, tamano FROM cancion WHERE id_cancion = ?",
            (id_cancion,)
        ).fetchone()
    if fila is None:
        return jsonify(error="Canción no encontrada"), 404
    return jsonify(dict(fila)), 200


# ------------------- DISCOMp3 -------------------
@app.route("/discoMp3", methods=["GET"])
def listar_discos():
    with get_conn() as conn:
        filas = conn.execute(
            "SELECT id_discoMp3 AS id_discoMp3, nombre, duration, tamano, precio FROM discoMp3 ORDER BY id_discoMp3"
        ).fetchall()
    return jsonify([dict(f) for f in filas]), 200


@app.route("/discoMp3/<int:id_discoMp3>", methods=["GET"])
def detalle_disco(id_discoMp3):
    with get_conn() as conn:
        fila = conn.execute(
            "SELECT id_discoMp3 AS id_discoMp3, nombre, duracion, tamaño, precio FROM discoMp3 WHERE id_discoMp3 = ?",
            (id_discoMp3,)
        ).fetchone()
    if fila is None:
        return jsonify(error="Disco no encontrado"), 404
    return jsonify(dict(fila)), 200


# ------------------- VINILO -------------------
@app.route("/vinilo", methods=["GET"])
def listar_vinilos():
    with get_conn() as conn:
        filas = conn.execute(
            "SELECT id_vinilo AS id_vinilo, nombre, artista, anio_salida, precio_unitario FROM vinilo ORDER BY id_vinilo"
        ).fetchall()
    return jsonify([dict(f) for f in filas]), 200


@app.route("/vinilo/<int:id_vinilo>", methods=["GET"])
def detalle_vinilo(id_vinilo):
    with get_conn() as conn:
        fila = conn.execute(
            "SELECT id_vinilo AS id_vinilo, nombre, artista, anio_salida, precio_unitario FROM vinilo WHERE id_vinilo = ?",
            (id_vinilo,)
        ).fetchone()
    if fila is None:
        return jsonify(error="Vinilo no encontrado"), 404
    return jsonify(dict(fila)), 200


# ------------------- PEDIDO -------------------
@app.route("/pedido", methods=["GET"])
def listar_pedidos():
    with get_conn() as conn:
        filas = conn.execute(
            "SELECT id_pedido AS id_pedido, id_us, fecha_pedido, estado, medio_pago FROM pedido ORDER BY id_pedido"
        ).fetchall()
    return jsonify([dict(f) for f in filas]), 200


@app.route("/pedido/<int:id_pedido>", methods=["GET"])
def detalle_pedido(id_pedido):
    with get_conn() as conn:
        fila = conn.execute(
            "SELECT id_pedido AS id_pedido, id_us, fecha_pedido, estado, medio_pago FROM pedido WHERE id_pedido = ?",
            (id_pedido,)
        ).fetchone()
    if fila is None:
        return jsonify(error="Pedido no encontrado"), 404
    return jsonify(dict(fila)), 200


# ------------------- VALORACION -------------------
@app.route("/valoracion", methods=["GET"])
def listar_valoraciones():
    with get_conn() as conn:
        filas = conn.execute(
            "SELECT id_valo AS id_valo, id_pedido, id_us, descripcion FROM valoracion ORDER BY id_valo"
        ).fetchall()
    return jsonify([dict(f) for f in filas]), 200


@app.route("/valoracion/<int:id_valo>", methods=["GET"])
def detalle_valoracion(id_valo):
    with get_conn() as conn:
        fila = conn.execute(
            "SELECT id_valo AS id_valo, id_pedido, id_us, descripcion FROM valoracion WHERE id_valo = ?",
            (id_valo,)
        ).fetchone()
    if fila is None:
        return jsonify(error="Valoración no encontrada"), 404
    return jsonify(dict(fila)), 200


# ------------------- CORREO -------------------
@app.route("/correo", methods=["GET"])
def listar_correos():
    with get_conn() as conn:
        filas = conn.execute(
            "SELECT id_us AS id_usuario, correo FROM correo ORDER BY id_us"
        ).fetchall()
    return jsonify([dict(f) for f in filas]), 200


@app.route("/correo/<int:id_us>", methods=["GET"])
def detalle_correo(id_us):
    with get_conn() as conn:
        fila = conn.execute(
            "SELECT id_us AS id_usuario, correo FROM correo WHERE id_us = ?",
            (id_us,)
        ).fetchone()
    if fila is None:
        return jsonify(error="Correo no encontrado"), 404
    return jsonify(dict(fila)), 200


# ------------------- TELEFONO -------------------
@app.route("/telefono", methods=["GET"])
def listar_telefonos():
    with get_conn() as conn:
        filas = conn.execute(
            "SELECT id_us AS id_usuario, telefono FROM telefono ORDER BY id_us"
        ).fetchall()
    return jsonify([dict(f) for f in filas]), 200


@app.route("/telefono/<int:id_us>", methods=["GET"])
def detalle_telefono(id_us):
    with get_conn() as conn:
        fila = conn.execute(
            "SELECT id_us AS id_usuario, telefono FROM telefono WHERE id_us = ?",
            (id_us,)
        ).fetchone()
    if fila is None:
        return jsonify(error="Teléfono no encontrado"), 404
    return jsonify(dict(fila)), 200


# ------------------- CORREO_PROVEEDOR -------------------
@app.route("/correo_proveedor", methods=["GET"])
def listar_correos_proveedor():
    with get_conn() as conn:
        filas = conn.execute(
            "SELECT id_proveedor AS id_proveedor, correo FROM correo_proveedor ORDER BY id_proveedor"
        ).fetchall()
    return jsonify([dict(f) for f in filas]), 200


@app.route("/correo_proveedor/<int:id_proveedor>", methods=["GET"])
def detalle_correo_proveedor(id_proveedor):
    with get_conn() as conn:
        fila = conn.execute(
            "SELECT id_proveedor AS id_proveedor, correo FROM correo_proveedor WHERE id_proveedor = ?",
            (id_proveedor,)
        ).fetchone()
    if fila is None:
        return jsonify(error="Correo de proveedor no encontrado"), 404
    return jsonify(dict(fila)), 200


# ------------------- TELEFONO_PROVEEDOR -------------------
@app.route("/telefono_proveedor", methods=["GET"])
def listar_telefonos_proveedor():
    with get_conn() as conn:
        filas = conn.execute(
            "SELECT id_proveedor AS id_proveedor, telefono FROM telefono_proveedor ORDER BY id_proveedor"
        ).fetchall()
    return jsonify([dict(f) for f in filas]), 200


@app.route("/telefono_proveedor/<int:id_proveedor>", methods=["GET"])
def detalle_telefono_proveedor(id_proveedor):
    with get_conn() as conn:
        fila = conn.execute(
            "SELECT id_proveedor AS id_proveedor, telefono FROM telefono_proveedor WHERE id_proveedor = ?",
            (id_proveedor,)
        ).fetchone()
    if fila is None:
        return jsonify(error="Teléfono de proveedor no encontrado"), 404
    return jsonify(dict(fila)), 200


# ------------------- RECOPILACION -------------------
@app.route("/recopilacion", methods=["GET"])
def listar_recopilaciones():
    with get_conn() as conn:
        filas = conn.execute(
            "SELECT id_recopilacion AS id_recopilacion, nombre, id_us, publica FROM recopilacion ORDER BY id_recopilacion"
        ).fetchall()
    return jsonify([dict(f) for f in filas]), 200


@app.route("/recopilacion/<int:id_recopilacion>", methods=["GET"])
def detalle_recopilacion(id_recopilacion):
    with get_conn() as conn:
        fila = conn.execute(
            "SELECT id_recopilacion AS id_recopilacion, nombre, id_us, publica FROM recopilacion WHERE id_recopilacion = ?",
            (id_recopilacion,)
        ).fetchone()
    if fila is None:
        return jsonify(error="Recopilación no encontrada"), 404
    return jsonify(dict(fila)), 200

if __name__ == "__main__":
    
    app.run(debug=True)