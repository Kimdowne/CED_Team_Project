from fastapi import FastAPI
from pydantic import BaseModel

from llm import ChatLLM, ChatSummaryModel
from client import Server

app = FastAPI()

chat = ChatLLM()
summary = ChatSummaryModel()

server = Server()

class ConversationState(BaseModel):
    isProcessing: bool

class UserRequest(BaseModel):
    user_message: str

def end_conversation():
    summerized = summary.summary_history()
    print(summerized)
    server.start_server(summerized[0], summerized[1])
    chat.__init__()
    summary.__init__()

@app.get("/")
def get_root():
    return {"message": "root"}

@app.get("/conv_state")
def get_state(conv_state: ConversationState):
    process = conv_state.dict()
    value = process["isProcessing"]
    if not value:
        end_conversation()


    return {"isProcessing": value}

@app.post("/chat")
def post_message(request: UserRequest) -> dict[str, str]:
    context = request.dict()
    user_input = context["user_message"]

    # 사용자 입력을 받아서 대화를 실행합니다.
    answer = chat.language_generation(user_input)

    # save Chatting Log
    summary.save_chatlog(user_input, answer)

    return { "answer": answer }