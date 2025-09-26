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
# ------------------- USUARIO -------------------
@app.route("/usuario", methods=["GET"])
def listar_usuarios():
    with get_conn() as conn:
        filas = conn.execute(
            "SELECT u.id_usuario, u.nombre, u.contrasena, t.telefono, c.correo FROM usuario u LEFT JOIN telefono t ON u.id_usuario = t.id_us LEFT JOIN correo c ON u.id_usuario = c.id_us ORDER BY u.id_usuario"
            ).fetchall()
    items = [dict(f) for f in filas]
    return jsonify(items), 200


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

# ------------------- PROVEDOR -------------------
@app.route("/proveedor", methods=["GET"])
def listar_proveedores():
    with get_conn() as conn:
        filas = conn.execute(
            "SELECT p.id_proveedor, p.nombre, t.telefono, c.correo FROM proveedor p LEFT JOIN telefono_proveedor t ON p.id_proveedor = t.id_proveedor LEFT JOIN correo_proveedor c ON p.id_proveedor = c.id_proveedor ORDER BY p.id_proveedor"
            ).fetchall()
    items = [dict(f) for f in filas]
    return jsonify(items), 200

@app.route("/proveedor/<int:proveedor_id>", methods=["GET"])
def detalle_proveedor(proveedor_id):
    with get_conn() as conn:
        fila = conn.execute(
            "SELECT p.id_proveedor, p.nombre, t.telefono, c.correo FROM proveedor p LEFT JOIN telefono_proveedor t ON p.id_proveedor = t.id_proveedor LEFT JOIN correo_proveedor c ON p.id_proveedor = c.id_proveedor ORDER BY p.id_proveedor",
            (proveedor_id,)
        ).fetchone()
    if fila is None:
        return jsonify(error="proveedor no encontrado"), 404
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
            "SELECT id_discoMp3 AS id_discoMp3, nombre, duracion, tamaño, precio FROM discoMp3 ORDER BY id_discoMp3"
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
            "SELECT id_vinilo AS id_vinilo, nombre, artista, año_salida, precio_unitario FROM vinilo ORDER BY id_vinilo"
        ).fetchall()
    return jsonify([dict(f) for f in filas]), 200


@app.route("/vinilo/<int:id_vinilo>", methods=["GET"])
def detalle_vinilo(id_vinilo):
    with get_conn() as conn:
        fila = conn.execute(
            "SELECT id_vinilo AS id_vinilo, nombre, artista, año_salida, precio_unitario FROM vinilo WHERE id_vinilo = ?",
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
            "SELECT id_pedido AS id_pedido, id_us, fecha_pedido, estado, medio_pago, id_item, id_proveedor FROM pedido ORDER BY id_pedido"
        ).fetchall()
    return jsonify([dict(f) for f in filas]), 200


@app.route("/pedido/<int:id_pedido>", methods=["GET"])
def detalle_pedido(id_pedido):
    with get_conn() as conn:
        fila = conn.execute(
            "SELECT id_pedido AS id_pedido, id_us, fecha_pedido, estado, medio_pago, id_item, id_proveedor FROM pedido WHERE id_pedido = ?",
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

#TABLA DISCOMP3
@app.route("/crear/discoMp3", methods=["POST"])
def crear_discoMp3():
    if not request.is_json:
        return jsonify(error="Content-Type debe ser application/json"), 415

    data = request.get_json(silent=True)
    if data is None:
        return jsonify(error="JSON malformado o vacío"), 400

    nombre = data.get("nombre")
    duracion = data.get("duracion")
    tamano = data.get("tamano")
    precio = data.get("precio")

    faltan = [k for k in ("nombre", "duracion", "tamano", "precio") if k not in data]
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
    
    if not isinstance(precio, str):
        return jsonify(error="precio debe ser string"), 422
    precio = precio.strip()
    if not precio or len(precio) > 100:
        return jsonify(error="precio no puede estar vacía (<= 100 chars)"), 422

    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO discoMp3 (nombre, duracion, tamano, precio) VALUES (?, ?, ?, ?)",
            (nombre, duracion, tamano, precio)
        )
        nuevo_id = cur.lastrowid

    resp = jsonify({"id_discoMp3": nuevo_id, "nombre": nombre, "duracion":duracion, "tamano": tamano, "precio": precio})
    resp.status_code = 201
    resp.headers["Location"] = f"/discoMp3/{nuevo_id}"
    return resp

#TABLA VINILO
@app.route("/crear/vinilo", methods=["POST"])
def crear_vinilo():
    if not request.is_json:
        return jsonify(error="Content-Type debe ser application/json"), 415

    data = request.get_json(silent=True)
    if data is None:
        return jsonify(error="JSON malformado o vacío"), 400

    nombre = data.get("nombre")
    artista = data.get("artista")
    anio_salida = data.get("anio_salida")
    precio_unitario = data.get("precio_unitario")

    faltan = [k for k in ("nombre", "artista", "anio_salida", "precio_unitario") if k not in data]
    if faltan:
        return jsonify(error=f"Faltan campos: {', '.join(faltan)}"), 400

    if not isinstance(nombre, str):
        return jsonify(error="nombre debe ser string"), 422
    nombre = nombre.strip()
    if not nombre or len(nombre) > 100:
        return jsonify(error="nombre no puede estar vacío (<= 100 chars)"), 422
    
    if not isinstance(artista, str):
        return jsonify(error="artista debe ser string"), 422
    artista = artista.strip()
    if not artista or len(artista) > 100:
        return jsonify(error="artista no puede estar vacía (<= 100 chars)"), 422
    
    if not isinstance(anio_salida, str):
        return jsonify(error="anio_salida debe ser string"), 422
    anio_salida = anio_salida.strip()
    if not anio_salida or len(anio_salida) > 100:
        return jsonify(error="anio_salida no puede estar vacía (<= 100 chars)"), 422
    
    if not isinstance(precio_unitario, str):
        return jsonify(error="precio_unitario debe ser string"), 422
    precio_unitario = precio_unitario.strip()
    if not precio_unitario or len(precio_unitario) > 100:
        return jsonify(error="precio_unitario no puede estar vacía (<= 100 chars)"), 422

    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO vinilo (nombre, artista, anio_salida, precio_unitario) VALUES (?, ?, ?, ?)",
            (nombre, artista, anio_salida, precio_unitario)
        )
        nuevo_id = cur.lastrowid

    resp = jsonify({"id_vinilo": nuevo_id, "nombre": nombre, "artista":artista, "anio_salida": anio_salida, "precio_unitario": precio_unitario})
    resp.status_code = 201
    resp.headers["Location"] = f"/vinilo/{nuevo_id}"
    return resp

#TABLA VALORACION
@app.route("/crear/valoracion", methods=["POST"])
def crear_valoracion():
    if not request.is_json:
        return jsonify(error="Content-Type debe ser application/json"), 415
    
    data = request.get_json(silent=True)
    if data is None:
        return jsonify(error="JSON malformado o vacío"), 400
    
    id_pedido = data.get("id_pedido")
    id_us = data.get("id_us")
    descripcion = data.get("descripcion")

    faltan = [k for k in ("id_pedido","id_us","descripcion") if k not in data]
    if faltan:
        return jsonify(error=f"Faltan campos: {', '.join(faltan)}"), 400
    
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO valoracion (id_pedido, id_us, descripcion) VALUES (?, ?, ?)",
            (id_pedido, id_us, descripcion)
        )
        nuevo_id = cur.lastrowid
    
    resp = jsonify({
        "id_valo": nuevo_id, "id_pedido": id_pedido,
        "id_us": id_us, "descripcion": descripcion
    })
    resp.status_code = 201
    resp.headers["Location"] = f"/valoracion/{nuevo_id}"
    return resp

#TABLA PEDIDO
@app.route("/crear/pedido", methods=["POST"])
def crear_pedido():
    if not request.is_json:
        return jsonify(error="Content-Type debe ser application/json"), 415
    
    data = request.get_json(silent=True)
    if data is None:
        return jsonify(error="JSON malformado o vacío"), 400
    
    id_us = data.get("id_us")
    id_item = data.get("id_item")
    tipo_item = data.get("tipo_item")   # puede ser 'vinilo' o 'discoMp3'
    cantidad = data.get("cantidad")
    fecha_pedido = data.get("fecha_pedido")
    estado = data.get("estado")
    medio_pago = data.get("medio_pago")
    id_proveedor = data.get("id_proveedor")

    faltan = [k for k in ("id_us","id_item","tipo_item","cantidad","fecha_pedido","estado","medio_pago","id_proveedor") if k not in data]
    if faltan:
        return jsonify(error=f"Faltan campos: {', '.join(faltan)}"), 400
    
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO pedido (id_us, id_item, tipo_item, cantidad, fecha_pedido, estado, medio_pago, id_proveedor) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (id_us, id_item, tipo_item, cantidad, fecha_pedido, estado, medio_pago, id_proveedor)
        )
        nuevo_id = cur.lastrowid
    
    resp = jsonify({
        "id_pedido": nuevo_id, "id_us": id_us, "id_item": id_item,
        "tipo_item": tipo_item, "cantidad": cantidad, "fecha_pedido": fecha_pedido,
        "estado": estado, "medio_pago": medio_pago, "id_proveedor": id_proveedor
    })
    resp.status_code = 201
    resp.headers["Location"] = f"/pedido/{nuevo_id}"
    return resp

if __name__ == "__main__":
    app.run(debug=True)
