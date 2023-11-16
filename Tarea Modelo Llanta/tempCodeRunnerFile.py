faces = []
# Obtener las faces. Esto es siguiendo un patrón
for i in range(numLados):
    if (i < numLados - 1):
        # Faces de las caras circulares
        faces.append([1, 3 + i, 2 + i])
        faces.append([numLados + 2, numLados + 3 + i, numLados + 4 + i])
        # Faces de los lados de la rueda
        faces.append([2 + i, 3 + i, numLados + 3 + i])
        faces.append([3 + i, numLados + 4 + i, numLados + 3 + i])
    # Cuando es el último elemento se tiene que dar la vuelta a los índices
    else:
        faces.append([1, 2, 2 + i])
        faces.append([numLados + 2, numLados + 3 + i, numLados + 3])
        faces.append([2 + i, 2, numLados + 3 + i])
        faces.append([2, numLados + 3, numLados + 3 + i])