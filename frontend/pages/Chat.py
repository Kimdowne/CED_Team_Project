import streamlit as st
import json
import requests

st.title("Chat_temp ROOM")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# chat UI menegement Functions
def save_message(message, role):
    st.session_state["messages"].append({ "message": message, "role": role })

def send_message(message, role, save=True):
    with st.chat_message(role):
        st.markdown(message)
    if save:
        save_message(message, role)

def paint_history():
    for message in st.session_state["messages"]:
        send_message(message["message"], message["role"], save=False)
paint_history()


def request_message(message: str) -> str:
    url = "http://127.0.0.1:8000/chat"

    req = requests.post(
        url,
        json={
            "user_message": message,
        },
    )

    resp = req.json()
    with st.sidebar:
        st.write(resp)
    resp = resp["answer"]

    return resp

# Inputting message...
message = st.chat_input("Input text....")

if message:
    send_message(message, "human")
    answer = request_message(message)
    send_message(answer, "ai")
