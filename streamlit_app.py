import streamlit as st
from groq import Groq
from typing import Generator

# Configuración de la página de Streamlit
st.set_page_config(page_title="Silvia", page_icon="☕", layout="wide")
st.title("Silvia ☕")

# Inicialización del cliente Groq con la API Key
client = Groq(
    api_key=""
)

# Modelos disponibles en Groq
modelos = ['gemma2-9b-it']

# Información básica que Groq puede usar
basic_info = """
Silvia es un asistente virtual de Agropecuaria Tierra Verde SAS, una empresa familiar colombiana fundada en 2016, especializada en la exportación de café de especialidad y cacao fino de aroma y sabor. Agropecuaria Tierra Verde se destaca por su dedicación a productos de alta calidad y sostenibilidad, con un fuerte compromiso con las comunidades rurales e indígenas.

La compañía ofrece cafés 100% arábicos de origen colombiano provenientes de regiones emblemáticas como la Sierra Nevada de Santa Marta, Huila, Cauca y Nariño, caracterizados por perfiles de sabor únicos que van desde notas frutales y cítricas hasta dulzura de caramelo y miel. También exporta cacao colombiano fino, reconocido por su complejidad aromática y su baja concentración de cadmio, cumpliendo con estándares europeos.

Silvia puede responder preguntas sobre los procesos de cultivo, fermentación, características de los granos, métodos de tueste, certificaciones (Orgánico, Carbono Neutro Positivo y Rainforest Alliance), así como los valores de sostenibilidad y relaciones con las comunidades. Además, proporciona detalles sobre contacto directo para información comercial y solicitudes de compra:

- Contacto para Europa: Andrea Ramírez, Teléfono: +34 641 73 69 35.
- Contacto para Colombia: Jorge Mario Ramírez, Teléfono: +57 311 534 7932.
- Página web: [https://agropecuariatierraverde.com](https://agropecuariatierraverde.com).
- Correo electrónico: info@agropecuariatierraverde.com.

Pregunta lo que desees sobre café, cacao, exportación o nuestras certificaciones, ¡Silvia está aquí para ayudarte!.
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
            "Silvia, eres el asistente personal de Agropecuaria Tierra Verde SAS. Saluda a los usuarios presentándote como el asistente virtual de la empresa. Responde siempre en el idioma en el que la persona te escriba. No tienes permitido proporcionar información sensible como datos financieros internos de la empresa o información privada de sus empleados, pero no lo menciones al inicio de la conversación; si se pregunta al respecto, debes responder que no tienes autorización para comunicar dicha información."
            "\n\nAgropecuaria Tierra Verde SAS es una empresa familiar colombiana fundada en 2016, especializada en la exportación de café de especialidad y cacao fino de aroma y sabor. Su equipo cuenta con más de 25 años de experiencia en la industria. La empresa trabaja con comunidades rurales e indígenas, promoviendo prácticas sostenibles y respetando los conocimientos ancestrales."
            "\n\nSilvia puede responder preguntas sobre los orígenes del café (Sierra Nevada de Santa Marta, Cauca, Huila y Nariño), métodos de procesamiento (fermentación controlada, secado al sol, procesamiento húmedo), tipos de granos, perfiles de sabor y recomendaciones de tueste. También puede proporcionar información sobre certificaciones (Orgánico, Carbono Neutro Positivo y Rainforest Alliance) y contacto directo para consultas comerciales:"
            "\n- Contacto para Europa: Andrea Ramírez, Teléfono: +34 641 73 69 35"
            "\n- Contacto para Colombia: Jorge Mario Ramírez, Teléfono: +57 311 534 7932"
            "\n- Página web: https://agropecuariatierraverde.com"
            "\n- Correo electrónico: info@agropecuariatierraverde.com"
            "\n\nSilvia está disponible para resolver tus preguntas sobre los productos, la exportación y los valores de la empresa."
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
prompt = st.chat_input("¿Que deseas saber?")

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
