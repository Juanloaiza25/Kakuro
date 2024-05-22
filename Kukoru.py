import itertools

Cols = "ABCDEFGHI"
Rows = set(range(1, 10))

def clearBoard(Vars):
    for row in Rows:
        for col in Cols:
            Vars[f"{col}{row}"] = Rows.copy()   # Inicializar como un conjunto vacío


Vars = {}
clearBoard(Vars)

def loadBoard(Vars, fileName):
    sums = []
    with open(fileName, 'r') as file:
        for line in file:
            line = line.strip().upper()
            print("Línea leída del archivo:", line)  # Agregar esta línea para verificar la lectura del archivo
            if line:
                if ':' in line:
                    if ',' in line:
                        value, cells = line.split(':')
                        value = int(value)
                        cells = cells.split(',')
                        sums.append((value, cells))
                    else:
                        value, cell = line.split(':')
                        value = int(value)
                        Vars[cell] = {value}
                        print("Asignado valor", value, "a la celda", cell)  # Agregar esta línea para verificar la asignación de valores
                else:
                    print("Error: línea no válida:", line)
    return sums


def defineConstraints(sums):
    constraints = []
    for sum_value, cells in sums:
        constraints.append((sum_value, cells))
    return constraints


def domsEqual(Vars, constraint):
    anyChange = False
    sum_value, cells = constraint
    varsEquals = {}
    for cell1 in cells:
        if len(Vars[cell1]) > 1:
            for cell2 in cells:
                if cell1 != cell2:
                    if Vars[cell1] == Vars[cell2]:
                        if tuple(Vars[cell1]) in varsEquals:
                            aux_set = set(varsEquals[tuple(Vars[cell1])])
                            aux_set.add(cell1)
                            aux_set.add(cell2)
                            varsEquals[tuple(Vars[cell1])] = list(aux_set)
                        else:
                            varsEquals[tuple(Vars[cell1])] = [cell1, cell2]

    for domVar in varsEquals:
        if len(domVar) == len(varsEquals[domVar]):
            for cell in cells:
                if cell not in varsEquals[domVar]:
                    for value in domVar:
                        oldValue = Vars[cell].copy()
                        Vars[cell].discard(value)
                        if oldValue != Vars[cell]:
                            anyChange = True
    return anyChange

def is_valid_assignment(Vars, var, value):
    for constraint in constraints:
        if var in constraint:
            for other_var in constraint:
                if other_var != var and len(Vars[other_var]) == 1 and list(Vars[other_var])[0] == value:
                    return False
    return True


def solve_kakuro(Vars, constraints):
    if is_solved(Vars):
        return True

    var = select_unassigned_variable(Vars)
    if var is not None:
        print ("Variable seleccionada:", var)
        domain = Vars[var].copy()
        for value in domain:
            if is_valid_assignment(Vars, var, value):
                print("Asignando valor", value, "a la variable", var)
                Vars[var] = {value}
                 
                apply_constraints(Vars, constraints)

            if solve_kakuro(Vars, constraints):
                return True

            Vars[var] = domain
        
        else:
            print("No se encontró ninguna asignación válida para la variable", var)
    else:
        print("No se encontró ninguna variable no asignada")
    return False

def is_solved(Vars):
    return all(len(Vars[var]) == 1 for var in Vars)

def select_unassigned_variable(Vars):
    for var in Vars:
        if len(Vars[var]) > 1:
            return var

def apply_constraints(Vars, constraints):
    for constraint in constraints:
        sum_value, cells = constraint
        if domsEqual(Vars, constraint):
            print("Se aplicó la restricción domsEqual")
        if allDif(Vars, constraint):
            print("Se aplicó la restricción allDif")

def posibles_combinaciones_suma(sum_value, cells):
    posibles_combinaciones=[]
    for i in range(1,10):
        for j in range(1,10):
            if i+j==sum_value:
                posibles_combinaciones.append((i,j))
    return posibles_combinaciones


def allDif(Vars, constraint):
    anyChange = False
    sum_value, cells = constraint
    for cell1 in cells:
        if len(Vars[cell1]) == 1:
            for cell2 in cells:
                if cell1 != cell2:
                    oldDomain = Vars[cell2].copy()
                    Vars[cell2].discard(list(Vars[cell1])[0])
                    if oldDomain != Vars[cell2]:
                        anyChange = True
    return anyChange


def select_unassigned_variable(Vars):
    unassigned_vars = [var for var in Vars if len(Vars[var]) > 1]
    if not unassigned_vars:
        print("No se encontró ninguna variable no asignada")
        return None
    return unassigned_vars[0]


# Cargar el tablero y las restricciones desde un archivo
sums = loadBoard(Vars, 'board.txt')
print("Tablero cargado desde el archivo:")
print(Vars)  # Aquí agregamos la impresión de Vars
constraints = defineConstraints(sums)

solve_kakuro(Vars, constraints)

# Imprimir el tablero resultante
print("Tablero después de resolver:")
for row in range(1, 10):
    for col in "ABCDEFGHI":
        cell_values = list(Vars[f"{col}{row}"])
        if cell_values:
            print(cell_values[0], end=" ")
        else:
            print("X", end=" ")  # Si la lista está vacía, imprime "X"
    print()