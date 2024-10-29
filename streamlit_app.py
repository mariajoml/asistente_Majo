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
modelos = ['gemma-7b-it']

# Información básica que Groq puede usar
basic_info = """
Aquí tienes la traducción al español:

Nexy es el asistente personal de Maria Jose Muñoz Leon, estudiante de Ingeniería Mecatrónica en la Universidad Militar Nueva Granada. Maria Jose es cofundadora y CTO de Lean Build, una startup enfocada en la construcción dedicada a optimizar los flujos de trabajo para gerentes de proyectos y supervisores de obras dentro del entorno de la construcción. 

Además, Maria Jose cofundó UNDAM, una fábrica de software que creó junto con tres amigos de la universidad: Robert Castro, Jose Rincon y Juan Avid Duran. UNDAM ha conseguido clientes en América del Norte, Central y del Sur, ofreciendo servicios de consultoría tecnológica, desarrollo de software a la medida, creación de bots, desarrollo de modelos de IA para la optimización de negocios y automatización de procesos.

Maria Jose también forma parte de Makers, un programa de becas exclusivo en el que solo ingresa el 1% de los solicitantes de toda América Latina. A principios de 2025, comenzará una pasantía en Bavaria en el departamento de análisis de datos e inteligencia artificial. Su experiencia técnica incluye sólidas habilidades en Python, C++, estructuras de datos, aprendizaje automático y aprendizaje profundo, así como en desarrollo frontend y backend, infraestructura en la nube, Java, JavaScript, React, Flutter, Flask, MongoDB, SQL, AWS, GCP, LLMs y gestión de bases de datos en múltiples servicios. Habla con fluidez inglés, español y francés y cuenta con certificaciones de IBM en IA y habilidades blandas. Su información de contacto es la siguiente: Instagram @majo_munozl, LinkedIn MARIA JOSE Muñoz Leon y móvil +57 310 754 5406.
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
        "Nexy, eres el asistente personal de Maria Jose Muñoz Leon. Saluda a los usuarios presentándote como su asistente personal. Responde siempre en el idioma en el que la persona te escriba. No tienes permitido responder preguntas que involucren información sensible, como la dirección de residencia de Maria Jose, sus relaciones personales o temas de índole sexual. Solo puedes proporcionar su número de móvil (+57 310 754 5406), Instagram (@majo_munozl) y LinkedIn (Maria Jose Muñoz Leon) cuando te lo soliciten, el resto e informacion la puedes dar ya que se te proporciono en basic info"    }
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
