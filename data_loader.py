# data_loader.py
import streamlit as st
import json
import os

@st.cache_data
def load_all_data():
    """
    Loads user and chat data from JSON files.
    Caches the data to improve performance.
    """
    usuarios_data = []
    chat_data = {}

    # Path to the user file
    file_path_usuario = "data/usuarios/usuarios.json"
    # Path to the conversations file
    file_path_conversaciones = "data/procesamiento/conversaciones_simplificadas.json"

    # Load user data
    if os.path.exists(file_path_usuario):
        try:
            with open(file_path_usuario, "r", encoding="utf-8") as f_users:
                usuarios_data = json.load(f_users)
        except json.JSONDecodeError:
            st.error(f"Error decoding JSON in {file_path_usuario}. Ensure the file has a valid JSON format.")
        except Exception as e:
            st.error(f"Error loading users from {file_path_usuario}: {e}")
    else:
        st.warning(f"User file not found: {file_path_usuario}. Please ensure the file exists.")

    # Load conversation data
    if os.path.exists(file_path_conversaciones):
        try:
            with open(file_path_conversaciones, "r", encoding="utf-8") as f_chat:
                chat_data = json.load(f_chat)
        except json.JSONDecodeError:
            st.error(f"Error decoding JSON in {file_path_conversaciones}. Ensure the file has a valid JSON format.")
        except Exception as e:
            st.error(f"Error loading conversations from {file_path_conversaciones}: {e}")
    else:
        st.warning(f"Conversation file not found: {file_path_conversaciones}. Please ensure the file exists.")
            
    return usuarios_data, chat_data
