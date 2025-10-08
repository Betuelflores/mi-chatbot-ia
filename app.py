import streamlit as st
import requests
import re
import tempfile
import subprocess
import shutil
import os

st.set_page_config(page_title="Bot Código sin Token", page_icon="🤖", layout="wide")
st.title("🤖 Bot Asistente de Código sin Token")
st.markdown("Envía tu pregunta o petición de código y recibe respuestas usando un modelo gratuito de Hugging Face Inference API sin token.")

def llamar_space(mensaje: str) -> str:
    # Usa la Inference API gratuita de Hugging Face (sin token para uso básico)
    url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
    payload = {"inputs": mensaje}
    try:
        resp = requests.post(url, json=payload, timeout=20)
        if resp.status_code == 200:
            return resp.json()
        else:
            return f"Error: {resp.status_code} - {resp.text}"
    except Exception as e:
        return f"Excepción al llamar al API: {e}"

def extraer_codigo(texto: str) -> str:
    # Busca bloques de código Python entre triple backticks
    bloques = re.findall(r"```(?:python)?\n(.*?)```", texto, re.DOTALL)
    return "\n\n".join(bloques).strip() if bloques else ""

def ejecutar_python_simple(codigo: str, timeout: int = 5):
    tmp = tempfile.mkdtemp()
    path = os.path.join(tmp, "script.py")
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(codigo)
        proc = subprocess.run(
            ["python3", path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout
        )
        return proc.stdout.decode("utf-8"), proc.stderr.decode("utf-8")
    except subprocess.TimeoutExpired:
        return "", "Tiempo excedido al ejecutar el código."
    except Exception as e:
        return "", f"Error ejecutando código: {e}"
    finally:
        shutil.rmtree(tmp)

mensaje = st.text_input("Escribe tu pregunta o petición de código:")
if mensaje:
    respuesta = llamar_space(mensaje)
    st.write("Respuesta completa:")
    st.write(respuesta)

    # Extraer texto relevante del JSON
    texto = ""
    if isinstance(respuesta, dict) and "generated_text" in respuesta[0]:  # Ajustado para DialoGPT
        texto = respuesta[0]["generated_text"]
    else:
        texto = str(respuesta)

    st.markdown(texto)

    codigo = extraer_codigo(texto)
    if codigo:
        st.subheader("Código extraído:")
        st.code(codigo, language="python")

        if st.button("Ejecutar código extraído"):
            salida, error = ejecutar_python_simple(codigo)
            if salida:
                st.subheader("Salida del código:")
                st.code(salida)
            if error:
                st.subheader("Errores de ejecución:")
                st.error(error)
    else:
        st.info("No se detectó código Python en la respuesta.")
