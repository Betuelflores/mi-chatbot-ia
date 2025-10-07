import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("🤖 Mi Chatbot IA")
user_input = st.text_input("Pregúntame lo que quieras:")

if user_input:
    try:
        # PROBAR MODELOS ALTERNATIVOS
        modelos = ['gemini-1.0-pro', 'gemini-1.5-flash', 'gemini-1.5-pro']
        
        for modelo in modelos:
            try:
                model = genai.GenerativeModel(modelo)
                response = model.generate_content(user_input)
                st.success(f"✅ Modelo funcionando: {modelo}")
                st.write("**Respuesta:**", response.text)
                break
            except:
                continue
        else:
            st.error("❌ Ningún modelo de Gemini funciona en tu región")
            
    except Exception as e:
        st.error(f"Error: {e}")
