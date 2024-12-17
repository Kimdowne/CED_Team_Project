import streamlit as st
import json
import requests

st.title("Chat_temp ROOM")

def request_message(message: str) -> str:
    url = "http://127.0.0.1:8000/chat"

    req = requests.post(
        url,
        json={
            "user_message": message,
        },
    )

    resp = req.json()
    resp = resp["answer"]

    return resp

def get_state(isProcessing: bool):
    url = "http://127.0.0.1:8000/conv_state"

    req = requests.get(
        url,
        json={
            "isProcessing": isProcessing,
        }
    )
    resp = req.json()

    return resp["isProcessing"]

# sesstion Initialize
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "isProcessing" not in st.session_state:
    st.session_state["isProcessing"] = True
        


def chattting():
    # Inputting message...
    message = st.chat_input("Input text....")

    if message:
        send_message(message, "human")
        answer = request_message(message)
        send_message(answer, "ai")
        if not answer.count("#log/end") == 0:
            st.session_state["isProcessing"] = False
            get_state(False)
            st.rerun()

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
if st.session_state["isProcessing"]:
    chattting()
