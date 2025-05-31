import os
import json
from typing import List, Dict, Any


def cargar_conversaciones(carpeta: str) -> List[Dict[str, Any]]:
    conversaciones = []

    if not os.path.exists(carpeta):
        raise FileNotFoundError(f"La carpeta {carpeta} no existe.")

    for filename in os.listdir(carpeta):
        if filename.endswith(".json"):
            ruta = os.path.join(carpeta, filename)
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    datos = json.load(f)
                    if isinstance(datos, list):
                        conversaciones.extend(datos)
                    else:
                        print(f"⚠️ El archivo {filename} no contiene una lista válida.")
            except json.JSONDecodeError as e:
                print(f"❌ Error en {filename}: {e}")
    
    return conversaciones



def procesar_conversaciones(conversaciones: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, str]]]:
    salida = {}
    numero, nombre, texto = None, None, None

    for mensaje in conversaciones:
        tipo = mensaje.get("message", {}).get("type")
        contenido = mensaje.get("message", {}).get("content", "")

        if tipo == "human":
            numero, nombre, texto = None, None, None
            for linea in contenido.splitlines():
                if "user number" in linea.lower():
                    numero = linea.split(":", 1)[-1].strip()
                elif "user name" in linea.lower():
                    nombre = linea.split(":", 1)[-1].strip()
                elif "message text or description" in linea.lower():
                    texto = linea.split(":", 1)[-1].strip()

            if numero and nombre and texto:
                if numero not in salida:
                    salida[numero] = []
                salida[numero].append({
                    "sender": nombre,
                    "message": texto
                })

        elif tipo == "ai" and numero:
            if numero not in salida:
                salida[numero] = []
            salida[numero].append({
                "sender": "AI",
                "message": contenido.strip()
            })

    return salida