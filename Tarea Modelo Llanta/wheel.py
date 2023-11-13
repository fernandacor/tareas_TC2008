import math
import sys

def valoresModelo(lados=8, radio=1.0, ancho=0.5):
    lados = int(input("Ingresa número de lados: ") or lados)
    radio = float(input("Ingresa radio: ") or radio)
    ancho = float(input("Ingresa ancho: ") or ancho)

    # Esto no va a ser necesario
    print("num_lados = ", lados)
    print("radio = ", radio)
    print("ancho = ", ancho)

    # Listas para almacenar vértices y vectores normales
    vertices = []
    normales = []
    
    # Calcular ángulo
    angulo = 360 / lados

    # Generar vértices y normales
    for i in range(lados):
        angle_rad = math.radians(i * angulo)
        x = radio * math.cos(angle_rad)
        y = radio * math.sin(angle_rad)

        # Vértices de la parte superior de la rueda
        vertices.append((x, y, ancho / 2.0))

        # Vértices de la parte inferior de la rueda
        vertices.append((x, y, -ancho / 2.0))

        # Normales
        normales.append((x, y, 0))

    # Crear el archivo OBJ
    with open("wheel_model.obj", "w") as obj_file:
        obj_file.write("# OBJ file\n")
        obj_file.write("# Vertices: {}\n".format(len(vertices)))

        for vertex in vertices:
            obj_file.write("v {} {} {}\n".format(vertex[0], vertex[1], vertex[2]))

        obj_file.write("# Normals: {}\n".format(len(normales)))

        for normal in normales:
            obj_file.write("vn {} {} {}\n".format(normal[0], normal[1], normal[2]))

        obj_file.write("# Faces: {}\n".format(lados * 4))

        for i in range(0, len(vertices), 2):
            obj_file.write("f {0}//{0} {1}//{1} {3}//{3}\n".format(i + 1, i + 2, i + 3, i + 4))
        
valoresModelo()


