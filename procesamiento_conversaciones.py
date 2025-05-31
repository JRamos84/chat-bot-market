from utils.procesamiento_data import cargar_conversaciones, procesar_conversaciones
from utils.supabase import get_conversations_by_session, get_all_usuarios, guardar_json
import json
import os


def main():
    print("🔄 Descargando usuarios y conversaciones...")
    file_path_usuario = "data/usuarios/usuarios.json"
    with open(file_path_usuario, "r", encoding="utf-8") as f_users: # Usar f_users para evitar conflicto
                usuarios_data = json.load(f_users)
    
    usuarios = [usuario.get('numero_telefono') for usuario in usuarios_data]
    # Ejemplo: cargar conversaciones por session_id (puedes automatizar si lo deseas)
    for usuario in usuarios:
        get_conversations_by_session(usuario)

        print("🧪 Procesando conversaciones...")
        conversaciones = cargar_conversaciones("data/conversaciones/")
        output = procesar_conversaciones(conversaciones)
        guardar_json(output, "data/procesamiento/conversaciones_simplificadas.json")

    print("✅ Proceso completado.")

if __name__ == "__main__":
    get_all_usuarios()
    main()
