# Tarea CG 1: Modelo de Llanta
# Fernanda Cantu A01782232

# Librerias a utilizar
import math

# Función para definir los parametros de la llanta
def parametros(lados = 8, radio = 1, ancho = 0.5):
    lados = int(input("Ingresa el número de lados: ") or lados)
    radio = float(input("Ingresa el radio: ") or radio)
    ancho = float(input("Ingresa el ancho: ") or ancho)

    return lados, radio, ancho

# Función para calcular los vertices en base a los parametros
def calculoVertices(lados, radio, ancho):
    # Inicializar lista para almacenar los vertices
    vertices = []
    
    # Iterar por el número de lados para calcular los vertices usando el angulo
    for i in range(lados):
        #lista.append(x, y, z)
        vertices.append((0, radio * math.cos(math.radians(360/lados)*(i+1)), radio * math.sin(math.radians(360/lados)*(i+1))))
        vertices.append((ancho, radio * math.cos(math.radians(360/lados)*(i+1)), radio * math.sin(math.radians(360/lados)*(i+1))))
    
    return vertices

# Función para calcular las caras en base a los parametros
def calculoCaras(lados, vertices, ancho):
    # Inicializar lista para almacenar las caras
    caras = []

    # Cara "Frontal":
    # Centro y origen de cara A
    centroA = len(vertices)
    vertices.append((0, 0, 0))
    # Generar cara A
    for i in range(0, lados * 2, 2):
        caras.append((centroA, (i + 2) % (lados * 2), i))

    # "Borde" de la llanta:
    # Generar caras laterales
    for i in range(0, lados * 2, 2):
        caras.append((i, (i + 2) % (lados * 2), (i + 3) % (lados * 2), i + 1))

    # Cara "Trasera":
    # Centro y origen de cara B
    centroB = centroA + 1
    vertices.append((ancho, 0, 0))
    # Generar cara B
    for i in range(1, lados * 2, 2):
        caras.append((centroB, i, (i + 2) % (lados * 2)))

    return caras

def calculoNormales(vertices, caras):
    # Inicializar lista para almacenar las normales
    normales = []
    
    # Iterar por las caras
    for cara in caras:
        # Calcular los vertices de cada cara 
        if cara[0] < len(vertices):
            i = vertices[cara[0]]
            j = vertices[cara[1]]
            k = vertices[cara[2]]

            # Vectores a partir de los vertices
            vect1 = (j[0] - i[0], j[1] - i[1], j[2] - i[2])
            vect2 = (k[0] - i[0], k[1] - i[1], k[2] - i[2])

            # Producto cruz para obtener la normal de la cara
            productoCruz = (vect1[1] * vect2[2] - vect1[2] * vect2[1],
                            vect1[2] * vect2[0] - vect1[0] * vect2[2],
                            vect1[0] * vect2[1] - vect1[1] * vect2[0])
            
            # Normalizar la normal obtenida en el producto cruz
            length = math.sqrt(productoCruz[0]**2 + productoCruz[1]**2 + productoCruz[2]**2)
            normales.append((productoCruz[0]/length, productoCruz[1]/length, productoCruz[2]/length))
    
    return normales

def generarArchivo(vertices, caras, normales):
    with open("./Tarea Modelo Llanta/llanta_tarea1.obj", "w") as outputFile:
        outputFile.write("# OBJ para llanta - A01782232\n")
        outputFile.write("# Vertices: " + str(len(vertices)) + "\n")
        for vertice in vertices:
            outputFile.write("v {} {} {}\n".format(*vertice))
        outputFile.write("# Normales: " + str(len(normales)) + "\n")
        for normal in normales:
            outputFile.write("vn {} {} {}\n".format(*normal))
        outputFile.write("# Caras: " + str(len(caras)) + "\n")
        for cara in caras:
            outputFile.write("f")
            for vertice in cara:
                outputFile.write(" {}/{}".format(vertice + 1, vertice + 1))
            outputFile.write("\n")

def main():
    lados, radio, ancho = parametros()
    vertices = calculoVertices(lados, radio, ancho)
    caras = calculoCaras(lados, vertices, ancho)
    normales = calculoNormales(vertices, caras)
    generarArchivo(vertices, caras, normales)

main()