import streamlit as st
import requests

st.set_page_config(page_title="Hospital AI Agent", page_icon="🩺", layout="centered")

st.title("🩺 Hospital AI Assistant")
st.caption("Ask anything about patients, doctors, or hospital metrics using Natural Language.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_query := st.chat_input("Ex: How many patients have Diabetes?"):
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Querying database..."):
            try:
                response = requests.post(
                    "https://hospital-ai-agent-bfax.vercel.app/agent/chat",
                    json={"prompt": user_query},
                    timeout=30
                )
                if response.status_code == 200:
                    data = response.json()
                    bot_response = data.get("response", "No response received.")
                else:
                    bot_response = f"Error ({response.status_code}): Could not fetch response from backend."
            except Exception as e:
                bot_response = f"Connection Error: Make sure FastAPI backend is running. Details: {str(e)}"
            
            st.markdown(bot_response)
            st.session_state.messages.append({"role": "assistant", "content": bot_response})