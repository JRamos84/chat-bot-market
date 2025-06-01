# calendar_display.py
import streamlit as st

# Define a variable for the Google Calendar URL
# IMPORTANT: Replace this URL with your actual Google Calendar embed URL.
# You can find this URL in your Google Calendar settings under "Integrate calendar".
GOOGLE_CALENDAR_EMBED_URL = "https://calendar.google.com/calendar/embed?src=joseph0001%40gmail.com&ctz=America%2FArgentina%2FBuenos_Aires"

def render_calendar_tab():
    """
    Renders the 'Calendario' tab with an embedded Google Calendar.
    """
    st.header("Calendario de Clientes")
    st.markdown(f"""
        <p>Aquí puedes ver tus turno con los clientes</p>
    
        <iframe 
            src="{GOOGLE_CALENDAR_EMBED_URL}" 
            class="calendar-iframe"
            frameborder="0" 
            scrolling="no">
        </iframe>
    """, unsafe_allow_html=True)
