import streamlit as st
import requests
import json

API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
headers = {"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_KEY']}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

st.title("🤖 Mi Chatbot IA Gratuito")
user_input = st.text_input("Pregúntame lo que quieras:")

if user_input:
    output = query({"inputs": user_input})
    st.write("**Respuesta:**", output[0]['generated_text'])
