import streamlit as st
import json

# --- Datos de ejemplo (reemplazar con datos reales de una base de datos) ---
# Example data (replace with real data from a database)

## Conseguir datos de usuarios 


# Ruta del archivo generado
file_path_usuario = "data/usuarios/usuarios.json"

# Leer el archivo y guardar en una variable
with open(file_path_usuario, "r", encoding="utf-8") as f:
    usuarios_data = json.load(f)
print(usuarios_data)

usuarios = [usuario["nombre"] + "-" + usuario["numero_telefono"]  for usuario in usuarios_data]


#conseguir los datos de las conversaciones
file_path_conversaciones = "data/procesamiento/conversaciones_simplificadas.json"
# Leer el archivo y guardar en una variable
with open(file_path_conversaciones, "r", encoding="utf-8") as f:
    chat_data = json.load(f)
# Convertir los datos de chat a un formato más manejable
# Convert chat data to a more manageable format

chat_data = {
    "Juan perez": [
        {"sender": "Juan perez", "message": "¡Hola! Necesito ayuda con mi pedido."},
        {"sender": "Agente", "message": "Claro, ¿me podría dar su número de pedido, por favor?"},
        {"sender": "Juan perez", "message": "Es el #12345."},
        {"sender": "Agente", "message": "Gracias. Veo que su pedido está en camino y debería llegar mañana."},
        {"sender": "Juan perez", "message": "¿Hay alguna forma de rastrearlo en tiempo real?"},
        {"sender": "Agente", "message": "Sí, le he enviado un enlace de seguimiento a su correo electrónico."},
    ],
    "saragoza": [
        {"sender": "saragoza", "message": "Tengo un problema con la factura de este mes."},
        {"sender": "Agente", "message": "¿Podría especificar qué problema tiene con la factura?"},
        {"sender": "saragoza", "message": "El monto es incorrecto. Me cobraron de más."},
        {"sender": "Agente", "message": "Entendido. Permítame revisar su cuenta. ¿Es la factura del 15 de mayo?"},
        {"sender": "saragoza", "message": "Sí, esa misma."},
        {"sender": "Agente", "message": "Gracias. Estoy investigando el error. Le contactaré en breve con una solución."},
    ],
    "casimiro": [
        {"sender": "casimiro", "message": "Quiero cambiar mi plan de servicio."},
        {"sender": "Agente", "message": "Con gusto le ayudo. ¿Qué tipo de plan le gustaría?"},
        {"sender": "casimiro", "message": "Uno con más datos y llamadas ilimitadas."},
        {"sender": "Agente", "message": "Tenemos varias opciones que se ajustan a eso. ¿Le gustaría que le explique cada una?"},
        {"sender": "casimiro", "message": "Sí, por favor."},
    ]
}

# --- Configuración de la página ---
# Page configuration
st.set_page_config(layout="wide", page_title="bot-Ramos", page_icon=":speech_balloon:")

# --- Estilos CSS para simular WhatsApp ---
# CSS styles to simulate WhatsApp
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    html, body, [class*="st-"] {
        color: #1a1a1a; /* Default text color */
        font-family: 'Inter', sans-serif;
    }

    /* General background for the main content area, similar to WhatsApp's chat background */
    .stApp {
        background-color: #FFFFFF; /* Light beige/grey, common WhatsApp background */
    }

    /* Chat container styling */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 10px; /* Space between messages */
        padding: 15px;
        background-color: #E5DDD5; /* Same as app background for seamless look */
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        max-height: 70vh; /* Limit height for scrollability */
        overflow-y: auto; /* Enable scrolling */
    }

    /* Message bubble for the client (left aligned, green-ish) */
    .client-message {
        background-color: #DCF8C6; /* WhatsApp green for outgoing messages */
        color: #1a1a1a;
        padding: 10px 12px;
        border-radius: 10px;
        align-self: flex-start; /* Align to the left */
        max-width: 70%; /* Limit bubble width */
        word-wrap: break-word; /* Break long words */
        box-shadow: 0 1px 0.5px rgba(0, 0, 0, 0.13);
    }

    /* Message bubble for the agent (right aligned, light grey) */
    .agent-message {
        background-color: #FFFFFF; /* White for incoming messages */
        color: #1a1a1a;
        padding: 10px 12px;
        border-radius: 10px;
        align-self: flex-end; /* Align to the right */
        max-width: 70%; /* Limit bubble width */
        word-wrap: break-word; /* Break long words */
        box-shadow: 0 1px 0.5px rgba(0, 0, 0, 0.13);
    }

    /* Adjust Streamlit default elements for better integration */
    .stRadio > label {
        padding: 8px 0;
        font-weight: 600;
        color: #075E54; /* Dark green for client names */
    }
    .stRadio > label > div {
        border-radius: 8px;
    }
    .stButton > button {
        border-radius: 8px;
    }
    .stHeader {
        color: #075E54; /* WhatsApp header color */
    }
    h1 {
        color: #075E54;
    }
    </style>
""", unsafe_allow_html=True)


# --- Barra lateral (Sidebar) ---
# Sidebar
st.sidebar.title("Opciones")
st.sidebar.header("Visualizar Chats de Clientes")

# --- Contenido principal ---
# Main content
st.title("Distribuidora Ramos ChatsBots")

# Crear dos columnas para la selección del cliente y la visualización del chat
# Create two columns for client selection and chat visualization
col1, col2 = st.columns([1, 3]) # col1 takes 1 part, col2 takes 3 parts of the width

with col1:
    st.header("Clientes")
    # Obtener la lista de clientes disponibles
    # Get the list of available clients
    client_names = usuarios 
    
    # Selector de cliente usando st.radio para mostrar todos los clientes como una lista
    # Client selector using st.radio to display all clients as a list
    selected_client = st.radio(
        "Elige un cliente para ver sus conversaciones:",
        client_names
    )

with col2:
    st.header(f"Conversaciones de {selected_client}")
    # Add a div to contain chat messages for scrolling
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    if selected_client:
        # Mostrar las conversaciones del cliente seleccionado
        # Display the conversations of the selected client
        conversations = chat_data.get(selected_client, [])
        if conversations:
            for chat_entry in conversations:
                sender = chat_entry["sender"]
                message = chat_entry["message"]
                
                # Usar st.markdown para formatear los mensajes con clases CSS
                # Use st.markdown to format messages with CSS classes
                if sender == selected_client:
                    st.markdown(f"<div class='client-message'><b>{sender}:</b> {message}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='agent-message'><b>{sender}:</b> {message}</div>", unsafe_allow_html=True)
        else:
            st.info("No hay conversaciones para este cliente.")
    else:
        st.info("Por favor, selecciona un cliente para ver sus conversaciones.")
    st.markdown('</div>', unsafe_allow_html=True) # Close the chat container div
