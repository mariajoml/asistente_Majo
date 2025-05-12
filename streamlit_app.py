import streamlit as st
from groq import Groq
from typing import Generator

# Configuración de la página de Streamlit
st.set_page_config(page_title="Silvia", page_icon="☕", layout="wide")
st.title("NEXY")

# Inicialización del cliente Groq con la API Key
client = Groq(
    api_key="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"
)

# Modelos disponibles en Groq
modelos = ['gemma2-9b-it']
# Información básica que Groq puede usar
basic_info = """
Maria Jose Muñoz es estudiante de Ingeniería en Mecatrónica en la universidad militar nueva granada. Nació el 23 de octubre de 2001 en Rionegro.
Sus intereses incluyen tecnología, desarrollo, modelos de IA (CNN, Faster R-CNN), desarrollo de bots, uso de API, Python, deep learning, machine learning e innovación, es una persona que gestiona bastante bien su tiempo y ademas sabe liderar equipos, tambien conoce lenguajes como c++. c#, java y java script, sabe utilizar flutter y react, tiene conocimientos en Power Bi.
Habla español e inglés con fluidez, y tiene conocimientos básicos de francés.
En su tiempo libre ha practicado deportes como cheerleading, natación, equitación, ballet, gimnasia, tenis y patinaje de velocidad.
Tiene una perrita llamada Melody.
Maria jose tiene un certificado de softskills de IBM otro de principios de IA de IBM, un certificado en machine learning y deep learning de Udemy, ademas que pertenecio a Maker fellowship donde entar el mejor 1 porciento de el talento de latam.
le gusta viajar y conocer lugares nuevos.
Maria jose ha sido CTO de dos startups en estado de preseed participando en concursos de incubadoras, las startups fueron LeanBuild y Sparfi, quedando en Incuva una incubadorapreruana donde levantaron capital para la startup, tambien ha trabajado con UNDAM una software factory enfocada al desarrollo tecnologico y la implementacion de IA para optimizar y mejorar proceso dentro de las empresas.
si te preguntan como pueden contactar a maria jose les puedes dar sus redes, Linkedin es:  Maria Jose Muñoz www.linkedin.com/in/maria-munozl , tambien su numero de whatsapp es 3107545406, su correo es: majitomule@gmail.com o mariaa.munoz@ab-inbev.com


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
            "Eres un asistente personal que le pertenece a Maria jose llamado nexy diseñado para responder preguntas a otras personas sobre Maria Jose Muñoz . "
            "Enfatiza que Maria Jose es una persona con bastantes cualidades y habilidades tecnicas, es creativa y apacionada, es conocida por su manera de trabajar y la calidad en los trabajosque entrega ademas ella cuenta con  experiencia en diversas areas como IA, Machine learning y deep learning. "
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
