# Tarea CG 1- Modelo para Llantas
# Fernanda Cantú A01782232

import math

def definirParametros():
    # Parámetros
    lados = int(input("Ingresa número de lados: ") or lados == 8)
    radio = float(input("Ingresa radio: ") or radio == 1.0)
    ancho = float(input("Ingresa ancho: ") or ancho == 0.5)
    
    return lados, radio, ancho

def calcularVertices(lados, radio, ancho):
    # Listas para almacenar vértices y vectores normales
    vertices = []
    caras = []
    normales = []

    # Calcular vértices
    for i in range(lados):
        angulo = 2 * math.pi * i / lados
        vertices.append((radio * math.cos(angulo), radio * math.sin(angulo), 0))
        vertices.append((radio * math.cos(angulo), radio * math.sin(angulo), ancho))

    # Calcular caras
    carafrente = len(vertices) - 2
    caraatras = len(vertices) - 1

    for i in range(0, lados * 2, 2):
        caras.append((carafrente, i, (i + 2) % (lados * 2)))

    for i in range(0, lados * 2, 2):
        caras.append((i, (i + 2) % (lados * 2), (i + 3) % (lados * 2), i + 1))

    for i in range(1, lados * 2, 2):
        caras.append((caraatras, i, (i + 2) % (lados * 2)))

    # Calcular normales
    for cara in caras:
        v1 = vertices[cara[0]]
        v2 = vertices[cara[1]]
        v3 = vertices[cara[2]]

        vector1 = (v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2])
        vector2 = (v3[0] - v1[0], v3[1] - v1[1], v3[2] - v1[2])

        normal = (vector1[1]*vector2[2] - vector1[2]*vector2[1],
                  vector1[2]*vector2[0] - vector1[0]*vector2[2],
                  vector1[0]*vector2[1] - vector1[1]*vector2[0])

        length = math.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
        #normales.append((normal[0]/length, normal[1]/length, normal[2]/length))

        if length != 0:
            normales.append((normal[0]/length, normal[1]/length, normal[2]/length))
        else:
            normales.append((0,0,0))
           
            
    with open("Tarea Modelo Llanta/rueda_tarea1.obj", 'w') as archivo:
        # Escribir vértices
        for vertice in vertices:
            archivo.write(f'v {vertice[0]} {vertice[1]} {vertice[2]}\n')

        # Escribir normales
        for normal in normales:
            archivo.write(f'vn {normal[0]} {normal[1]} {normal[2]}\n')

        # Escribir caras
        for cara in caras:
            archivo.write('f ')
            for vertice in cara:
                archivo.write(f'{vertice + 1}/{vertice + 1} ')
            archivo.write('\n')

# Llamada a la función
lados, radio, ancho = definirParametros()
calcularVertices(lados, radio, ancho)