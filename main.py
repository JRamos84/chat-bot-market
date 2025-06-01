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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    html, body, [class*="st-"] {
        color: #1a1a1a; /* Default text color */
        font-family: 'Inter', sans-serif;
    }

    /* General background for the main content area, similar to WhatsApp chat background */
    .stApp {
        background-color: #FFFFFF; /* Beige/light gray, common WhatsApp background */
    }

    /* Chat container style */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 10px; /* Space between messages */
        padding: 15px;
        background-color: #E5DDD5; /* Same as app background for a seamless look */
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        max-height: 70vh; /* Limit height to allow scrolling */
        overflow-y: auto; /* Enable scrolling */
    }

    /* Message bubble for the client (left-aligned, greenish) */
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

    /* Message bubble for the agent (right-aligned, light gray) */
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

    /* Adjust default Streamlit elements for better integration */
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

    /* Style for the embedded calendar iframe */
    .calendar-iframe {
        width: 100%;
        height: 800px; /* Adjust height as needed */
        border: none;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# --- Cargar datos ---
# Load data
@st.cache_data
def load_data():
    usuarios_data = []
    chat_data = {}

    # Path to the user file
    file_path_usuario = "data/usuarios/usuarios.json"
    # Path to the conversations file
    file_path_conversaciones = "data/procesamiento/conversaciones_simplificadas.json"

    # Load user data
    if os.path.exists(file_path_usuario):
        try:
            with open(file_path_usuario, "r", encoding="utf-8") as f_users: # Use f_users to avoid conflict
                usuarios_data = json.load(f_users)
        except json.JSONDecodeError:
            st.error(f"Error decoding JSON in {file_path_usuario}. Ensure the file has a valid JSON format.")
        except Exception as e:
            st.error(f"Error loading users from {file_path_usuario}: {e}")
    else:
        st.warning(f"User file not found: {file_path_usuario}. Please ensure the file exists.")

    # Load conversation data
    if os.path.exists(file_path_conversaciones):
        with open(file_path_conversaciones, "r", encoding="utf-8") as f_chat:
            raw_chat_data = json.load(f_chat)
            
    
    return usuarios_data, raw_chat_data

# Load data with a spinner
with st.spinner("Cargando datos..."):
    usuarios_data, chat_data = load_data()


# Prepare the list of users for the selector
usuarios = [f"{usuario.get('nombre', 'Desconocido')}-{usuario.get('numero_telefono', 'N/A')}" for usuario in usuarios_data]
# Filter users who do not have a valid phone number to avoid split errors
usuarios = [u for u in usuarios if '-' in u and u.split('-')[1] != 'N/A']


# --- Barra lateral (Sidebar) ---
# Sidebar
st.sidebar.title("Opciones")
st.sidebar.header("Chats de Clientes")

# --- Contenido principal ---
# Main content
st.title("Distribuidora Ramos ChatsBots")

# Create tabs
tab1, tab2 = st.tabs(["Chats de Clientes", "Calendario"])

with tab1:
    # Create two columns for client selection and chat visualization
    col1, col2 = st.columns([1, 3]) # col1 takes 1 part, col2 takes 3 parts of the width

    with col1:
        st.header("Clientes")
        
        # Client selector using st.radio to display all clients as a list
        if usuarios:
            selected_client_display = st.radio(
                "Elige un cliente para ver sus conversaciones:",
                usuarios
            )
            # Extract only the phone number
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
            
            # Display the conversations of the selected client
            conversations = chat_data.get(selected_telefono, [])
            if conversations:
                for chat_entry in conversations:
                    sender = chat_entry.get("sender", "Desconocido")
                    message = chat_entry.get("message", "Mensaje vacío")
                    
                    # Use st.markdown to format messages with CSS classes
                    if sender == selected_telefono: # Assume the client's "sender" is their phone number
                        st.markdown(f"<div class='client-message'><b>{sender}:</b> {message}</div>", unsafe_allow_html=True)
                    else: # Any other sender is considered the agent
                        st.markdown(f"<div class='agent-message'><b>{sender}:</b> {message}</div>", unsafe_allow_html=True)
            else:
                st.info("No hay conversaciones para este cliente.")
            st.markdown('</div>', unsafe_allow_html=True) # Close the chat container div
        else:
            st.info("Por favor, selecciona un cliente para ver sus conversaciones.")

with tab2:
    st.header("Calendario de Google")
    st.markdown("""
        <p>Aquí puedes ver tu calendario de Google. Por favor, asegúrate de que el calendario esté configurado como público o compartible para que pueda ser incrustado correctamente.</p>
        <p>Para incrustar tu propio calendario, ve a la configuración de tu Google Calendar, busca la sección "Integrar calendario" y copia el código HTML. Luego, reemplaza el valor de <code>src</code> en el <code>iframe</code> de este código con tu propio URL.</p>
        <iframe 
            src="https://calendar.google.com/calendar/embed?src=es.argentinian%23holiday%40group.v.calendar.google.com&ctz=America%2FArgentina%2FBuenos_Aires" 
            class="calendar-iframe"
            frameborder="0" 
            scrolling="no">
        </iframe>
    """, unsafe_allow_html=True)
