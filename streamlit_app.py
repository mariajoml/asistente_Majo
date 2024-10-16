import streamlit as st
from groq import Groq
from typing import Generator

# Configuración de la página de Streamlit
st.set_page_config(page_title="Nexy", page_icon="🤖", layout="wide")
st.title("Nexy 🤖")

# Inicialización del cliente Groq con la API Key
client = Groq(
    api_key="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"
)

# Modelos disponibles en Groq
modelos = ['llama3-8b-8192']

# Información básica que Groq puede usar
basic_info = """
Nexy es la primera aplicacion de social streaming media encargada de ofrecerle al usuario una experiencia innovadora al momento de ver peliculas series o documentales, las personas van a ser capaces de conectarse a medios de difucion como comunidades de las peliculas que les guste, a su vez podran conectar conn amigos o nuevas personas para ver peliculas grupales llamadas partys y tambien podran con un plan pago acceder a contenido premiu como ver la grabacion en tiempo real de sus peliculas favoritas
"""

# Función generadora para mostrar las respuestas del asistente
def generate_chat_responses(chat_completion) -> Generator[str, None, None]:   
    """Genera respuestas a partir de los chunks del chat_completion de Groq."""
    for chunk in chat_completion:
        if hasattr(chunk.choices[0], 'delta') and hasattr(chunk.choices[0].delta, 'content'):
            yield chunk.choices[0].delta.content

# Inicializar estado de la sesión para mensajes
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mensaje inicial del sistema proporcionando el contexto del asistente con la información básica
if not st.session_state.messages:
    system_message = {
        "role": "system",
        "content": (
            "Eres un asistente llamado nexy por la aplicacion nexy en este caso vas a dar a conocer la aplicacion, sus features y los beneficios de adquirirla  "
            " a su vez explica que tu seras en el momento de el lanzamiento de la pelicula el consejero principal de cada persona, ofreciendole soporte 24/7 no solo en el funcionamiento de la aplicacion si no tambien, contestandoles dudas o ofreciendo sugerencias sobre lo que vieran ver o etc "
            f"{basic_info}"
        )
    }
    st.session_state.messages.append(system_message)

# Mostrar los mensajes de chat previos del usuario y el asistente en la aplicación
with st.container():
    for message in st.session_state.messages:
        if message["role"] != "system":  # Evitar mostrar el mensaje del sistema
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

# Campo de entrada para el prompt del usuario
prompt = st.chat_input("¿Que te gustaria saber de majo el dia de hoy?")

if prompt:
    # Mostrar mensaje del usuario en el contenedor de mensajes de chat
    st.chat_message("user").markdown(prompt)
    # Agregar mensaje del usuario al historial de chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        # Generar respuesta con Groq usando el historial de mensajes, incluyendo el mensaje inicial con la información básica
        chat_completion = client.chat.completions.create(
            model=modelos[0],  # Asegúrate de seleccionar el modelo correcto                      
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],  # Entregamos el historial de los mensajes para que el modelo tenga contexto
            stream=True
        )

        # Generar respuestas con el contenido correcto desde los chunks de Groq
        response_chunks = [
            chunk.choices[0].delta.content
            for chunk in chat_completion 
            if hasattr(chunk.choices[0], 'delta') and hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content is not None
        ]

        response_content = "".join(response_chunks)

    except Exception as e:
        st.error(f"Error con Groq: {e}")
        response_content = "Lo siento, hubo un problema al procesar la solicitud."

    # Mostrar la respuesta final
    with st.chat_message("assistant"):
        st.markdown(response_content)

    # Agregar respuesta del asistente al historial de chat
    st.session_state.messages.append({"role": "assistant", "content": response_content})
