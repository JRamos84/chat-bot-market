# app.py
import streamlit as st
from styles import apply_styles
from data_loader import load_all_data
from chat_display import render_chat_tab
from calendar_display import render_calendar_tab

# --- Page configuration ---
st.set_page_config(layout="wide", page_title="bot-Ramos", page_icon=":speech_balloon:")

# --- Apply CSS styles ---
apply_styles()

# --- Load data with a spinner ---
with st.spinner("Cargando datos..."):
    usuarios_data, chat_data = load_all_data()

# Prepare the list of users for the selector
usuarios = [f"{usuario.get('nombre', 'Desconocido')}-{usuario.get('numero_telefono', 'N/A')}" for usuario in usuarios_data]
# Filter users who do not have a valid phone number to avoid split errors
usuarios = [u for u in usuarios if '-' in u and u.split('-')[1] != 'N/A']


# --- Main content ---
st.title("Distribuidora Ramos ChatsBots")


render_chat_tab(usuarios, chat_data)


