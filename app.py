import streamlit as st
from openai import OpenAI

# Configuración de OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Mi ChatGPT", page_icon="🤖")
st.title("🤖 Mi Asistente IA")
st.write("¡Hola! Pregúntame lo que quieras")

# Chat input
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe tu mensaje..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
            )
            
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
