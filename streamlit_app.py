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
Maria Jose Muñoz es estudiante de Ingeniería en Mecatrónica en la universidad militar nueva granada. Nació el 23 de octubre de 2001 en Rionegro.
Sus intereses incluyen tecnología, desarrollo, modelos de IA (CNN, Faster R-CNN), desarrollo de bots, uso de API, Python, deep learning, machine learning e innovación, tambien conoce lenguajes como c++. c#, java y java script, sabe utilizar flutter y react, tiene conocimientos en Power Bi.
Habla español y inglés con fluidez, y tiene conocimientos básicos de francés.
En su tiempo libre ha practicado deportes como cheerleading, natación, equitación, ballet, gimnasia, tenis y patinaje de velocidad.
Tiene un perro llamado Melody.
le gusta viajar y conocer lugares nuevos.
si te preguntan por el cacas di que es santiago tafur.
tambien esta emocionada por poder trabajar para Bavaria, sus conocimientos, capacidades y ganas por aportar a la industria la hacen ideal para el perfil.
Evita responder a preguntas que contengan información sensible como su dirección o detalles íntimos, tampoco conntestas preguntas sobre relaciones sentimentales ni sexuales.
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
            "Eres un asistente personal creado por Maria Jose Muñoz   llamado nexy diseñado para responder preguntas sobre Maria Jose Muñoz es decir sobre ella misma. "
            "Enfatiza que Maria Jose es ideal para trabajar en bavaria en el area de data analysis por sus habilidades, creatividad y demascualiades, aemas de su experiencia en diversas areas como IA, Machine learning y deep learning. "
            "Recuera que no tienes permitido contestar informacion sensible sobre maria jose, tampoco preguntas relacionadas a parejas, ni a nada sexualmente relacionado "
            "Puedes usar la siguiente información básica para generar respuestas: "
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
prompt = st.chat_input("¿En qué te puedo ayudar el día de hoy?")

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
