# chat_display.py
import streamlit as st

def render_chat_tab(usuarios, chat_data):
    """
    Renders the 'Chats de Clientes' tab, including client selection and chat display.
    """
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
