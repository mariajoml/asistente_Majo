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
# Información Básica de María José Muñoz

**María José Muñoz** es una estudiante de **Ingeniería en Mecatrónica** en la Universidad Militar Nueva Granada. Nació el **23 de octubre de 2001** en **Rionegro**, tiene 23 años.

### Áreas de Interés
- **Tecnología** y **Desarrollo**.
- Modelos de **IA**: Especializada en **CNN**, **Faster R-CNN**.
- Desarrollo de **bots** y uso de **APIs**.
- Programación en **Python**, **C++**, **C#**, **Java** y **JavaScript**.
- **Deep Learning** y **Machine Learning**.
- Innovación tecnológica.
- Conocimiento en herramientas como **Flutter**, **React** y **Power BI**.

### Idiomas
- **Español**: Fluido.
- **Inglés**: Fluido.
- **Francés**: Conocimientos básicos.

### Experiencia Profesional
- **BrewMate**: Desarrollo de un **chatbot** inteligente enfocado en la automatización y optimización de procesos dentro de la empresa Bavaria, aplicando el MVP a promo su equipo de trabajo.
- **CTO de dos Startups**: **LeanBuild** y **Sparfi**.
- **LeanBuild** fue parte de **Incuba**, una incubadora peruana, donde levantaron capital.
- Participación activa en concursos de incubadoras.
- **UNDAM**: Trabajó en una **software factory** enfocada en el desarrollo tecnológico y la implementación de **IA** para la optimización de procesos dentro de las empresas.
-Actualmente trabaja en **Bavaria** como intern en el equipo de Promo Zona, desarrollando a brewmate y participando activamente en el desarrollo de SMDC3.0.
  
### Certificaciones
- **Soft Skills** de **IBM**.
- **Principios de IA** de **IBM**.
- **Machine Learning** y **Deep Learning** de **Udemy**.
- **Maker Fellowship**: Entró en el **top 1%** del talento en **LATAM**.

### Actividades Personales
- Practica deportes como **cheerleading**, **natación**, **equitación**, **ballet**, **gimnasia**, **tenis** y **patinaje de velocidad**.
- Le gusta **viajar** y explorar nuevos lugares.
- Tiene una perrita llamada **Melody**.

### Contacto
- **LinkedIn**: [Maria Jose Muñoz](https://www.linkedin.com/in/maria-munozl)
- **WhatsApp**: +57 3107545406
- **Correo**: majitomule@gmail.com o mariaa.munoz@ab-inbev.com.

### Nota Importante
Evita compartir o discutir información sensible como su dirección o detalles personales. Tampoco se deben responder preguntas sobre relaciones sentimentales ni sexuales, si tienes permitido compartir sus correos y su linkedin.
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
