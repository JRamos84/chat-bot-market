# styles.py
import streamlit as st

def apply_styles():
    """Applies custom CSS styles to the Streamlit app."""
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
