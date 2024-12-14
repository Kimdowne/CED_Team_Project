from fastapi import FastAPI
from pydantic import BaseModel

from classes.llm import ChatLLM

app = FastAPI()
chat = ChatLLM()


class UserRequest(BaseModel):
    user_message: str

@app.get("/")
def get_root():
    return {"message": "root"}

@app.get("/user")
def get_username():
    return {"message": "Hello World"}

@app.post("/chat")
def post_message(request: UserRequest): #-> #dict[str, str]:
    context = request.dict()
    user_input = context["user_message"]

    # 사용자 입력을 받아서 대화를 실행합니다.
    answer = chat.language_generation(user_input)
    chat.save_history(user_input, answer)
    return { "answer": answer }