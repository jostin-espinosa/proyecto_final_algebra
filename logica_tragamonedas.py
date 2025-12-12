import random

SIMBOLOS = ["🍋", "🍒", "🍇", "🔔", "⭐", "💎", "💰"]
FILAS = 3
COLUMNAS = 5

def obtener_simbolo():
    prob = random.randrange(1, 1000)
    if prob <= 210:
        return SIMBOLOS[0]  # 🍋
    elif prob <= 420:
        return SIMBOLOS[1]  # 🍒
    elif prob <= 570:
        return SIMBOLOS[2]  # 🍇
    elif prob <= 720:
        return SIMBOLOS[3]  # 🔔
    elif prob <= 825:
        return SIMBOLOS[4]  # ⭐
    elif prob <= 930:
        return SIMBOLOS[5]  # 💎
    else:
        return SIMBOLOS[6]  # 💰
   

def generar_tablero():
    return [[obtener_simbolo() for _ in range(COLUMNAS)] for _ in range(FILAS)]

PATRONES_ESPECIFICOS = {
    "P24_OJO_DIABLO": [(0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 3), (1, 4), (2, 1), (2, 2), (2, 3)],
    "P25_JACKPOT": [(r, c) for r in range(FILAS) for c in range(COLUMNAS)],
}

def es_jackpot(tablero):
    primer_simbolo = tablero[0][0]
    for i in range(FILAS):
        for j in range(COLUMNAS):
            if tablero[i][j] != primer_simbolo:
                return False, None
    return True, primer_simbolo

def calcular_premios_jackpot(simbolo_ganador):
    premios = []
    # Filas
    nombres_filas = ["P1_HOR_SUP_LARG", "P2_HOR_CENT_LARG", "P3_HOR_INF_LARG"]
    for f, nombre in enumerate(nombres_filas):
        coords = [(f, c) for c in range(COLUMNAS)]
        premios.append({
            "patron": nombre,
            "simbolo": simbolo_ganador,
            "conteo": 5,
            "pago_base": 50,
            "coordenadas": coords
        })

    # Columnas
    nombres_cols = ["P19_VERT_1", "P20_VERT_2", "P21_VERT_3", "P22_VERT_4", "P23_VERT_5"]
    for c, nombre in enumerate(nombres_cols):
        coords = [(r, c) for r in range(FILAS)]
        premios.append({
            "patron": nombre,
            "simbolo": simbolo_ganador,
            "conteo": 3,
            "pago_base": 5,
            "coordenadas": coords
        })

    # Diagonales
    diag_coords = [
        [(0,0), (1,1), (2,2)],           # P13
        [(0,1), (1,2), (2,3)],           # P14
        [(0,2), (1,3), (2,4)],           # P15
        [(2,0), (1,1), (0,2)],           # P16
        [(2,1), (1,2), (0,3)],           # P17
        [(2,2), (1,3), (0,4)],           # P18
    ]
    nombres_diag = ["P13_DIAG_1", "P14_DIAG_2", "P15_DIAG_3",
                    "P16_DIAG_INV_1", "P17_DIAG_INV_2", "P18_DIAG_INV_3"]
    for nombre, coords in zip(nombres_diag, diag_coords):
        premios.append({
            "patron": nombre,
            "simbolo": simbolo_ganador,
            "conteo": 3,
            "pago_base": 5,
            "coordenadas": coords
        })

    # Patrones especiales
    for nombre_patron, coords in PATRONES_ESPECIFICOS.items():
        pago = {"P24_OJO_DIABLO": 100, "P25_JACKPOT": 500}.get(nombre_patron, 0)
        premios.append({
            "patron": nombre_patron,
            "simbolo": simbolo_ganador,
            "conteo": len(coords),
            "pago_base": pago,
            "coordenadas": coords
        })

    return premios

def validar_lineas_comunes_normal(tablero):
    premios = []
    posiciones_premiadas = [[False for _ in range(COLUMNAS)] for _ in range(FILAS)]

    def procesar_secuencia(secuencia, coords):
        premios_encontrados = []
        i = 0
        while i < len(secuencia):
            r, c = coords[i]
            if posiciones_premiadas[r][c]:
                i += 1
                continue

            simbolo = secuencia[i]
            j = i + 1
            while j < len(secuencia) and secuencia[j] == simbolo:
                j += 1
            longitud = j - i

            if longitud >= 3:
                conteo = min(longitud, 5)
                pago = {5: 50, 4: 20, 3: 5}[conteo]
                premio_coords = coords[i:j]
                premios_encontrados.append({
                    "patron": f"LINEA_{i}_{j}",
                    "simbolo": simbolo,
                    "conteo": conteo,
                    "pago_base": pago,
                    "coordenadas": premio_coords
                })
                for k in range(i, j):
                    r, c = coords[k]
                    posiciones_premiadas[r][c] = True
                i = j
            else:
                i += 1
        return premios_encontrados

    # Filas
    for f in range(FILAS):
        fila = tablero[f]
        coords = [(f, c) for c in range(COLUMNAS)]
        premios.extend(procesar_secuencia(fila, coords))

    # Columnas
    for c in range(COLUMNAS):
        columna = [tablero[r][c] for r in range(FILAS)]
        coords = [(r, c) for r in range(FILAS)]
        premios.extend(procesar_secuencia(columna, coords))

    # Diagonales descendentes
    for start_col in range(COLUMNAS):
        diag = []
        coords = []
        r, c = 0, start_col
        while r < FILAS and c < COLUMNAS:
            diag.append(tablero[r][c])
            coords.append((r, c))
            r += 1
            c += 1
        if len(diag) >= 3:
            premios.extend(procesar_secuencia(diag, coords))

    for start_row in range(1, FILAS):
        diag = []
        coords = []
        r, c = start_row, 0
        while r < FILAS and c < COLUMNAS:
            diag.append(tablero[r][c])
            coords.append((r, c))
            r += 1
            c += 1
        if len(diag) >= 3:
            premios.extend(procesar_secuencia(diag, coords))

    # Diagonales ascendentes
    for start_col in range(COLUMNAS):
        diag = []
        coords = []
        r, c = FILAS - 1, start_col
        while r >= 0 and c < COLUMNAS:
            diag.append(tablero[r][c])
            coords.append((r, c))
            r -= 1
            c += 1
        if len(diag) >= 3:
            premios.extend(procesar_secuencia(diag, coords))

    for start_row in range(FILAS - 2, -1, -1):
        diag = []
        coords = []
        r, c = start_row, 0
        while r >= 0 and c < COLUMNAS:
            diag.append(tablero[r][c])
            coords.append((r, c))
            r -= 1
            c += 1
        if len(diag) >= 3:
            premios.extend(procesar_secuencia(diag, coords))

    return premios

def validar_patrones_especificos_normal(tablero):
    premios = []
    for nombre_patron, coordenadas in PATRONES_ESPECIFICOS.items():
        if nombre_patron == "P25_JACKPOT":
            continue
        try:
            secuencia = [tablero[r][c] for r, c in coordenadas]
        except IndexError:
            continue
        if all(s == secuencia[0] for s in secuencia):
            simbolo_ganador = secuencia[0]
            pago = {"P24_OJO_DIABLO": 100}.get(nombre_patron, 0)
            premios.append({
                "patron": nombre_patron,
                "simbolo": simbolo_ganador,
                "conteo": len(secuencia),
                "pago_base": pago,
                "coordenadas": coordenadas
            })
    return premios

def validar_premios(tablero):
    es_jack, simbolo_jack = es_jackpot(tablero)
    if es_jack:
        return calcular_premios_jackpot(simbolo_jack)
    else:
        premios_normales = validar_lineas_comunes_normal(tablero)
        premios_especificos = validar_patrones_especificos_normal(tablero)
        return premios_normales + premios_especificos