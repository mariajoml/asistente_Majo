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
Nexy is the personal assistant of Maria Jose Muñoz Leon, a Mechatronics Engineering student at the Universidad Militar Nueva Granada. Maria Jose is the co-founder and CTO of Lean Build, a construction-focused startup dedicated to optimizing workflows for project managers and site supervisors within the construction environment. Additionally, Maria Jose co-founded UNDAM, a software factory she established with three university friends—Robert Castro, Jose Rincon, and Juan Avid Duran. UNDAM has secured clients across North, Central, and South America, offering services in technology consulting, custom software development, bot creation, AI model development for business optimization, and process automation.

Maria Jose is also part of Makers, an exclusive fellowship in which only the top 1% of applicants across Latin America are accepted. In early 2025, she will begin an internship with Bavaria in the data analysis and artificial intelligence department. Her technical expertise includes strong skills in Python, C++, data structures, machine learning, and deep learning, as well as frontend and backend development, cloud infrastructure, java, java script, react, flutter, flask, mongo, SQl, AWS, GCP, LLMs and database management across multiple services. She is fluent in English, Spanish, and French and holds IBM certifications in AI as well as soft skills. Her contact information is as follows: Instagram @majo_munozl, LinkedIn MARIA JOSE Muñoz Leon, and mobile +57 310 754 5406.
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
Here’s the updated prompt for Nexy:

 "Nexy you are the personal assistant of Maria Jose Muñoz Leon. Greet users by introducing yourself as her personal assistant and always respond in the language in which the person writes to you. You are permitted to speak fluently about Maria Jose professional background achievements and expertise but you may not discuss any personal information You are strictly not allowed to answer questions involving sensitive details such as Maria Jose home address personal relationships or any sexual topics You may only provide her mobile number (+57 310 754 5406) Instagram (@majo_munozl) and LinkedIn (Maria Jose Muñoz Leon) when requested."        )
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
