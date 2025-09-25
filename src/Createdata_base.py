import sqlite3, os

DB = "PoliSong.db"  # se creará en la carpeta del script

with sqlite3.connect(DB) as conn:
    conn.execute("PRAGMA foreign_keys = ON;")  # activar claves foráneas

    # Tabla usuario
    conn.execute("""
        CREATE TABLE IF NOT EXISTS usuario (
            id_usuario  INTEGER PRIMARY KEY,
            nombre      VARCHAR(50),
            contrasena  VARCHAR(50)
        );
    """)

    # Tabla telefono
    conn.execute("""
        CREATE TABLE IF NOT EXISTS telefono (
            id_us     INTEGER,
            telefono  VARCHAR(15) PRIMARY KEY,
            FOREIGN KEY (id_us) REFERENCES usuario(id_usuario)
        );
    """)

    # Tabla correo
    conn.execute("""
        CREATE TABLE IF NOT EXISTS correo (
            id_us   INTEGER,
            correo  VARCHAR(50) PRIMARY KEY,
            FOREIGN KEY (id_us) REFERENCES usuario(id_usuario)
        );
    """)

    # Tabla pedido
    conn.execute("""
        CREATE TABLE IF NOT EXISTS pedido (
            id_pedido     INTEGER PRIMARY KEY,
            id_us         INTEGER,
            fecha_pedido  DATE,
            estado        VARCHAR(50),
            medio_pago    VARCHAR(50),
            FOREIGN KEY (id_us) REFERENCES usuario(id_usuario)
        );
    """)

    # Tabla valoracion
    conn.execute("""
        CREATE TABLE IF NOT EXISTS valoracion (
            id_valo     INTEGER PRIMARY KEY,
            id_pedido   INTEGER,
            id_us       INTEGER,
            descripcion VARCHAR(200),
            FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido),
            FOREIGN KEY (id_us) REFERENCES usuario(id_usuario)
        );
    """)

    # Tabla cancion
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cancion (
            id_cancion  INTEGER PRIMARY KEY,
            nombre      VARCHAR(100),
            duracion    TIME,
            tamano      DECIMAL
        );
    """)

    # Tabla discoMp3
    conn.execute("""
        CREATE TABLE IF NOT EXISTS discoMp3 (
            id_discoMp3  INTEGER PRIMARY KEY,
            nombre       VARCHAR(100),
            duration     TIME,
            tamano       DECIMAL,
            precio       FLOAT
        );
    """)

    # Tabla vinilo
    conn.execute("""
        CREATE TABLE IF NOT EXISTS vinilo (
            id_vinilo      INTEGER PRIMARY KEY,
            nombre         VARCHAR(100),
            artista        VARCHAR(100),
            anio_salida    INTEGER,
            precio_unitario FLOAT,
            id_cancion     INTEGER,
            id_proveedor   INTEGER,
            FOREIGN KEY (id_cancion) REFERENCES cancion(id_cancion),
            FOREIGN KEY (id_proveedor) REFERENCES proveedor(id_proveedor)
        );
    """)

    # Tabla viniloCancion (relación N:M)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS viniloCancion (
            id_vinilo   INTEGER,
            id_cancion  INTEGER,
            PRIMARY KEY (id_vinilo, id_cancion),
            FOREIGN KEY (id_vinilo) REFERENCES vinilo(id_vinilo),
            FOREIGN KEY (id_cancion) REFERENCES cancion(id_cancion)
        );
    """)

    # Tabla discoMp3Cancion (relación N:M)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS discoMp3Cancion (
            id_discoMp3  INTEGER,
            id_cancion   INTEGER,
            PRIMARY KEY (id_discoMp3, id_cancion),
            FOREIGN KEY (id_discoMp3) REFERENCES discoMp3(id_discoMp3),
            FOREIGN KEY (id_cancion) REFERENCES cancion(id_cancion)
        );
    """)

    # Tabla recopilacion
    conn.execute("""
        CREATE TABLE IF NOT EXISTS recopilacion (
            id_recopilacion INTEGER PRIMARY KEY,
            nombre          VARCHAR(100),
            id_us           INTEGER,
            publica         BOOLEAN,
            FOREIGN KEY (id_us) REFERENCES usuario(id_usuario)
        );
    """)

    # Tabla recopilacionCancion (relación N:M)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS recopilacionCancion (
            id_recopilacion INTEGER,
            id_cancion      INTEGER,
            PRIMARY KEY (id_recopilacion, id_cancion),
            FOREIGN KEY (id_recopilacion) REFERENCES recopilacion(id_recopilacion),
            FOREIGN KEY (id_cancion) REFERENCES cancion(id_cancion)
        );
    """)

    # Tabla proveedor
    conn.execute("""
        CREATE TABLE IF NOT EXISTS proveedor (
            id_proveedor INTEGER PRIMARY KEY,
            nombre       VARCHAR(100)
        );
    """)

    # Tabla correo_proveedor
    conn.execute("""
        CREATE TABLE IF NOT EXISTS correo_proveedor (
            correo       VARCHAR(50) PRIMARY KEY,
            id_proveedor INTEGER,
            FOREIGN KEY (id_proveedor) REFERENCES proveedor(id_proveedor)
        );
    """)

    # Tabla telefono_proveedor
    conn.execute("""
        CREATE TABLE IF NOT EXISTS telefono_proveedor (
            telefono     VARCHAR(15) PRIMARY KEY,
            id_proveedor INTEGER,
            FOREIGN KEY (id_proveedor) REFERENCES proveedor(id_proveedor)
        );
    """)

print("✅ Base de datos lista en:", os.path.abspath(DB))
