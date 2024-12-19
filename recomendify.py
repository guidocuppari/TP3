#!/usr/bin/env python3
import argparse
import os
from funciones_auxiliares import leer_archivo, leer_entrada, efectuar_comandos
from estructuras import cargar_diccionario, cargar_grafo

param = argparse.ArgumentParser(None)
param.add_argument("ruta", type=str)
archivo = param.parse_args()

if not os.path.isfile(archivo.ruta):
    print("El archivo no existe")
    exit

imp = []
entradas = []
leer_archivo(archivo.ruta, imp)
leer_entrada(entradas)
cargar_diccionario(imp)
cargar_grafo()
efectuar_comandos(entradas)