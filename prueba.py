import itertools

# Definición de restricciones
restricciones = {
    3: ['B8', 'B9'],
    7: ['E7', 'E8'],
    7: ['H5', 'I5'],
    10: ['B8', 'C8', 'D8', 'E8'],
    17: ['B5', 'C5', 'D5', 'E5'],
}

# Restricciones fijas para comenzar
valores_fijos = {
    'B8': 1,
    'B9': 2,
    'E7': 1,
    'E8': 6,
    'H5': 2,
    'I5': 5,
}

# Función para validar sumas
def validar_sumas(tablero, restricciones):
    for suma, celdas in restricciones.items():
        if sum(tablero[celda] for celda in celdas) != suma:
            return False
    return True

# Tablero inicial con valores fijos
tablero = {f"{chr(x)}{y}": 0 for x in range(66, 75) for y in range(1, 10)}
tablero.update(valores_fijos)

# Comprobación
validar_sumas(tablero, restricciones)
print(tablero)
