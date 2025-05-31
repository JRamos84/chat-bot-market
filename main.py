import streamlit as st
import json
import os

# --- Configuración de la página ---
# Page configuration
st.set_page_config(layout="wide", page_title="bot-Ramos", page_icon=":speech_balloon:")

# --- Estilos CSS para simular WhatsApp ---
# CSS styles to simulate WhatsApp
st.markdown("""
    <style>
    @import url('https://fonts.com/css2?family=Inter:wght@400;600&display=swap');

    html, body, [class*="st-"] {
        color: #1a1a1a; /* Color de texto predeterminado */
        font-family: 'Inter', sans-serif;
    }

    /* Fondo general para el área de contenido principal, similar al fondo de chat de WhatsApp */
    .stApp {
        background-color: #FFFFFF; /* Beige/gris claro, fondo común de WhatsApp */
    }

    /* Estilo del contenedor de chat */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 10px; /* Espacio entre mensajes */
        padding: 15px;
        
        border-radius: 8px;
        box_shadow: 0 2px 5px rgba(0,0,0,0.1);
        max_height: 70vh; /* Limitar altura para permitir desplazamiento */
        overflow_y: auto; /* Habilitar desplazamiento */
    }

    /* Burbuja de mensaje para el cliente (alineado a la izquierda, verdoso) */
    .client-message {
        background-color: #144d37; /* Verde WhatsApp para mensajes salientes */
        color: #1a1a1a;
        padding: 10px 12px;
        border-radius: 10px;
        align-self: flex-start; /* Alinear a la izquierda */
        max_width: 70%; /* Limitar el ancho de la burbuja */
        word-wrap: break-word; /* Romper palabras largas */
        box_shadow: 0 1px 0.5px rgba(0, 0, 0, 0.13);
    }

    /* Burbuja de mensaje para el agente (alineado a la derecha, gris claro) */
    .agent-message {
        background-color: #FFFFFF; /* Blanco para mensajes entrantes */
        color: #1a1a1a;
        padding: 10px 12px;
        border-radius: 10px;
        align-self: flex-end; /* Alinear a la derecha */
        max_width: 70%; /* Limitar el ancho de la burbuja */
        word-wrap: break-word; /* Romper palabras largas */
        box_shadow: 0 1px 0.5px rgba(0, 0, 0, 0.13);
    }

    /* Ajustar elementos predeterminados de Streamlit para una mejor integración */
    .stRadio > label {
        padding: 8px 0;
        font-weight: 600;
        color: #075E54; /* Verde oscuro para nombres de clientes */
    }
    .stRadio > label > div {
        border-radius: 8px;
    }
    .stButton > button {
        border-radius: 8px;
    }
    .stHeader {
        color: #075E54; /* Color de encabezado de WhatsApp */
    }
    h1 {
        color: #075E54;
    }
    </style>
""", unsafe_allow_html=True)

# --- Cargar datos ---
# Load data
@st.cache_data
def load_data():
    usuarios_data = []
    chat_data = {}

    # Ruta del archivo de usuarios
    file_path_usuario = "data/usuarios/usuarios.json"
    # Ruta del archivo de conversaciones
    file_path_conversaciones = "data/procesamiento/conversaciones_simplificadas.json"

    # Cargar datos de usuarios
    if os.path.exists(file_path_usuario):
        try:
            with open(file_path_usuario, "r", encoding="utf-8") as f_users: # Usar f_users para evitar conflicto
                usuarios_data = json.load(f_users)
        except json.JSONDecodeError:
            st.error(f"Error al decodificar JSON en {file_path_usuario}. Asegúrate de que el archivo tenga un formato JSON válido.")
        except Exception as e:
            st.error(f"Error al cargar usuarios de {file_path_usuario}: {e}")
    else:
        st.warning(f"Archivo de usuarios no encontrado: {file_path_usuario}. Por favor, asegúrate de que el archivo exista.")

    # Cargar datos de conversaciones
    if os.path.exists(file_path_conversaciones):
        with open(file_path_conversaciones, "r", encoding="utf-8") as f_chat:
            raw_chat_data = json.load(f_chat)
            
    
    return usuarios_data, raw_chat_data

# Cargar los datos con un spinner
with st.spinner("Cargando datos..."):
    usuarios_data, chat_data = load_data()


# Preparar la lista de usuarios para el selector
usuarios = [f"{usuario.get('nombre', 'Desconocido')}-{usuario.get('numero_telefono', 'N/A')}" for usuario in usuarios_data]
# Filtrar usuarios que no tienen un número de teléfono válido para evitar errores de split
usuarios = [u for u in usuarios if '-' in u and u.split('-')[1] != 'N/A']


# --- Barra lateral (Sidebar) ---
# Sidebar
st.sidebar.title("Opciones")
st.sidebar.header("Visualizar Chats de Clientes")

# --- Contenido principal ---
# Main content
st.title("Distribuidora Ramos ChatsBots")

# Crear dos columnas para la selección del cliente y la visualización del chat
# Create two columns for client selection and chat visualization
col1, col2 = st.columns([1, 3]) # col1 toma 1 parte, col2 toma 3 partes del ancho

with col1:
    st.header("Clientes")
    
    # Selector de cliente usando st.radio para mostrar todos los clientes como una lista
    # Client selector using st.radio to display all clients as a list
    if usuarios:
        selected_client_display = st.radio(
            "Elige un cliente para ver sus conversaciones:",
            usuarios
        )
        # Extraer solo el número de teléfono
        selected_telefono = selected_client_display.split("-")[1]
        selected_nombre = selected_client_display.split("-")[0]
    else:
        st.info("No hay clientes disponibles para mostrar.")
        selected_telefono = None
        selected_nombre = None

with col2:
    if selected_telefono:
        st.header(f"Conversaciones de {selected_nombre} ({selected_telefono})")
        # Add a div to contain chat messages for scrolling
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Mostrar las conversaciones del cliente seleccionado
        # Display the conversations of the selected client
        conversations = chat_data.get(selected_telefono, [])
        if conversations:
            for chat_entry in conversations:
                sender = chat_entry.get("sender", "Desconocido")
                message = chat_entry.get("message", "Mensaje vacío")
                
                # Usar st.markdown para formatear los mensajes con clases CSS
                # Use st.markdown to format messages with CSS classes
                if sender == selected_telefono: # Asumimos que el "sender" del cliente es su número de teléfono
                    st.markdown(f"<div class='client-message'><b>{sender}:</b> {message}</div>", unsafe_allow_html=True)
                else: # Cualquier otro sender se considera el agente
                    st.markdown(f"<div class='agent-message'><b>{sender}:</b> {message}</div>", unsafe_allow_html=True)
        else:
            st.info("No hay conversaciones para este cliente.")
        st.markdown('</div>', unsafe_allow_html=True) # Cerrar el div del contenedor de chat
    else:
        st.info("Por favor, selecciona un cliente para ver sus conversaciones.")
