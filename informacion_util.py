import sys

CAMINO = "camino"
IMPORTANTES = "mas_importantes"
RECOMENDACION = "recomendacion"
CICLO = "ciclo"
NOMBRE_CANCION = 0
ARTISTA = 1

def leer_entrada(entradas):
    for linea in sys.stdin:
        linea = linea.strip()
        if linea == "":
            break
        entradas.append(linea)

def leer_archivo(ruta, datos):
    with open(ruta, 'r') as arc:
        next(arc)
        for linea in arc:
            info = linea.strip().split("\t")
            user = info[1]
            nombre_cancion = info[2]
            artista = info[3]
            nombre_playlist = info[5]
            datos.append((user, (nombre_cancion, artista), nombre_playlist))

def separar_datos(info):
    mas_datos = info.split(" ", 1)
    if len(mas_datos) < 2 or not mas_datos[0].isdigit():
        return None, None
    largo = int(mas_datos[0])

    cancion = mas_datos[1].split(" - ", 1)
    if len(cancion) < 2:
        return None, None
    inicio = (cancion[NOMBRE_CANCION].strip(), cancion[ARTISTA].strip())

    return largo, inicio

def guardar_canciones(divididas, canciones):
    for cancion in divididas:
        actual = cancion.split(" - ", 1)
        if len(actual) < 2:
            continue
        canciones.append((actual[NOMBRE_CANCION].strip(), actual[ARTISTA].strip()))

def error_formato_entrada(cantidad):
    if cantidad is None:
        return "Error: formato incorrecto."
    return None

def datos_comando_recomendacion(info, total_canciones):
    info = info.split(" ", 2)
    tipo = info[0]
    cantidad = int(info[1]) if len(info) > 1 else 0
    canciones = info[2] if len(info) > 2 else ""
    divididas = canciones.split(" >>>> ")
    guardar_canciones(divididas, total_canciones)
    return tipo, cantidad
    
def efectuar_comandos(recomendify, entradas):
    for entrada in entradas:
        datos = entrada.split(" ", 1)
        comando = datos[0]
        resto = datos[1] if len(datos) > 1 else ""
        if comando == CAMINO:
            canciones = resto.split(" >>>> ")
            if len(canciones) < 2:
                print("Error: formato incorrecto")
                continue
            primer_cancion = canciones[0].split(" - ", 1)
            segunda_cancion = canciones[1].split(" - ", 1)
            if len(primer_cancion) < 2 or len(segunda_cancion) < 2:
                print("Tanto el origen como el destino deben ser canciones")
                continue
            origen = (primer_cancion[NOMBRE_CANCION], primer_cancion[ARTISTA])
            destino = (segunda_cancion[NOMBRE_CANCION], segunda_cancion[ARTISTA])
            camino = recomendify.camino_minimo(origen, destino)
            print(camino)
        elif comando == IMPORTANTES:
            resto = int(resto)
            canciones = recomendify.mas_importantes(resto)
            print(canciones)
        elif comando == RECOMENDACION:
            canciones = []
            tipo, cantidad = datos_comando_recomendacion(resto, canciones)
            recomendaciones = recomendify.recomendar(recomendify.grafo_bipartito, tipo, cantidad, canciones, 50, 5000)
            print(recomendaciones)
        elif comando == CICLO:
            recomendify.cargar_grafo_de_canciones()
            largo, inicio = separar_datos(resto)
            mensaje = error_formato_entrada(largo)
            if mensaje is not None:
                print(mensaje)
                continue
            ciclo = recomendify.buscar_ciclo_n(inicio, largo)
            print(ciclo)
        else:
            recomendify.cargar_grafo_de_canciones()
            saltos, tupla = separar_datos(resto)
            mensaje = error_formato_entrada(saltos)
            if mensaje is not None:
                print(mensaje)
                continue
            rango = recomendify.rango(saltos, tupla)
            print(rango)