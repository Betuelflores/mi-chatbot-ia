import streamlit as st
import requests
import random

def try_multiple_free_apis(mensaje):
    apis = [
        {
            "name": "Hugging Face",
            "url": "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
            "func": lambda msg: requests.post(apis[0]["url"], json={"inputs": msg}).json()
        }
    ]
    
    for api in apis:
        try:
            response = api["func"](mensaje)
            if response and len(response) > 0:
                return f"{api['name']}: {response[0].get('generated_text', 'Respuesta no válida')}"
        except:
            continue
    
    return "Todos los servicios gratuitos están ocupados. Intenta más tarde."

st.title("🤖 Chatbot Multi-Fuente Gratis")
user_input = st.text_input("Pregunta:")
if user_input:
    respuesta = try_multiple_free_apis(user_input)
    st.write(respuesta)
