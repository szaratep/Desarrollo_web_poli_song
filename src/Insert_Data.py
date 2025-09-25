import sqlite3, os

DB = "PoliSong.db"

with sqlite3.connect(DB) as conn:
    conn.execute("PRAGMA foreign_keys = ON;")  # 🔑 habilitar claves foráneas

    # =========================
    # 1. USUARIOS
    # =========================
    usuarios = [
        ("Carlos", "pass1"),
        ("Ana", "pass2"),
        ("Pedro", "pass3"),
        ("Lucia", "pass4"),
        ("Juan", "pass5"),
        ("Marta", "pass6"),
        ("Luis", "pass7"),
        ("Paula", "pass8"),
        ("Jorge", "pass9"),
        ("Sofia", "pass10"),
    ]
    conn.executemany("INSERT INTO usuario (nombre, contrasena) VALUES (?, ?)", usuarios)

    # TELEFONOS
    telefonos = [(i+1, f"30000000{i}") for i in range(10)]
    conn.executemany("INSERT INTO telefono (id_us, telefono) VALUES (?, ?)", telefonos)

    # CORREOS
    correos = [(i+1, f"user{i}@gmail.com") for i in range(10)]
    conn.executemany("INSERT INTO correo (id_us, correo) VALUES (?, ?)", correos)

    # =========================
    # 2. PROVEEDORES
    # =========================
    proveedores = [(f"Proveedor_{i}",) for i in range(1, 11)]
    conn.executemany("INSERT INTO proveedor (nombre) VALUES (?)", proveedores)

    correos_prov = [(f"prov{i}@mail.com", i) for i in range(1, 11)]
    conn.executemany("INSERT INTO correo_proveedor (correo, id_proveedor) VALUES (?, ?)", correos_prov)

    telefonos_prov = [(f"31000000{i}", i) for i in range(1, 11)]
    conn.executemany("INSERT INTO telefono_proveedor (telefono, id_proveedor) VALUES (?, ?)", telefonos_prov)

    # =========================
    # 3. CANCIONES
    # =========================
    canciones = [(f"Cancion{i}", "00:03:30", 5.0+i) for i in range(1, 11)]
    conn.executemany("INSERT INTO cancion (nombre, duracion, tamano) VALUES (?, ?, ?)", canciones)

    # =========================
    # 4. DISCOS MP3
    # =========================
    discos = [(f"DiscoMP3_{i}", "00:45:00", 50+i, 9.99+i) for i in range(1, 11)]
    conn.executemany("INSERT INTO discoMp3 (nombre, duration, tamano, precio) VALUES (?, ?, ?, ?)", discos)

    # Relación discoMp3Cancion
    disco_canciones = [(i, i) for i in range(1, 11)]
    conn.executemany("INSERT INTO discoMp3Cancion (id_discoMp3, id_cancion) VALUES (?, ?)", disco_canciones)

    # =========================
    # 5. VINILOS
    # =========================
    vinilos = [(f"Vinilo_{i}", f"Artista_{i}", 2000+i, 19.99+i, i, i) for i in range(1, 11)]
    conn.executemany("""
        INSERT INTO vinilo (nombre, artista, anio_salida, precio_unitario, id_cancion, id_proveedor)
        VALUES (?, ?, ?, ?, ?, ?)
    """, vinilos)

    # Relación viniloCancion
    vinilo_canciones = [(i, i) for i in range(1, 11)]
    conn.executemany("INSERT INTO viniloCancion (id_vinilo, id_cancion) VALUES (?, ?)", vinilo_canciones)

    # =========================
    # 6. PEDIDOS
    # =========================
    pedidos = [
        (1, "2025-01-10", "pendiente", "tarjeta"),
        (2, "2025-01-12", "enviado", "efectivo"),
        (3, "2025-01-15", "entregado", "nequi"),
        (4, "2025-01-18", "cancelado", "tarjeta"),
        (5, "2025-01-20", "entregado", "efectivo"),
        (6, "2025-01-22", "pendiente", "tarjeta"),
        (7, "2025-01-25", "entregado", "efectivo"),
        (8, "2025-01-27", "pendiente", "nequi"),
        (9, "2025-01-28", "enviado", "tarjeta"),
        (10, "2025-01-30", "entregado", "efectivo"),
    ]
    conn.executemany("INSERT INTO pedido (id_us, fecha_pedido, estado, medio_pago) VALUES (?, ?, ?, ?)", pedidos)

    # =========================
    # 7. VALORACIONES
    # =========================
    valoraciones = [
        (1, 1, "Muy bueno"),
        (2, 2, "Regular"),
        (3, 3, "Excelente"),
        (4, 4, "Malo"),
        (5, 5, "Buen servicio"),
        (6, 6, "Perfecto"),
        (7, 7, "Recomendado"),
        (8, 8, "Mediocre"),
        (9, 9, "Genial"),
        (10, 10, "Aceptable"),
    ]
    conn.executemany("INSERT INTO valoracion (id_pedido, id_us, descripcion) VALUES (?, ?, ?)", valoraciones)

    # =========================
    # 8. RECOPILACIONES
    # =========================
    recopilaciones = [(f"Recopilacion_{i}", i, True if i % 2 == 0 else False) for i in range(1, 11)]
    conn.executemany("INSERT INTO recopilacion (nombre, id_us, publica) VALUES (?, ?, ?)", recopilaciones)

    recop_canciones = [(i, i) for i in range(1, 11)]
    conn.executemany("INSERT INTO recopilacionCancion (id_recopilacion, id_cancion) VALUES (?, ?)", recop_canciones)

    # =========================
    conn.commit()

print("✅ 10 datos insertados en cada tabla en:", os.path.abspath(DB))
