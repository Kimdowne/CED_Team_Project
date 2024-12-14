from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough

class ChatLLM:
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0.1,   
        )

        self.memory = ConversationSummaryBufferMemory(
            llm=self.llm,
            max_token_limit=100,
            return_messages=True,
        )
    
    def save_history(self, input, output):
        self.memory.save_context(
            {"input": input},
            {"output": output},
        )

    def language_generation(self, question):
        def load_memory(_):
            return self.memory.load_memory_variables({})["history"]

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI. and your name is GNU-CORE"),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ])

        chain = RunnablePassthrough.assign(history=load_memory) | prompt | self.llm
        result = chain.invoke({"question": question})

        return result.content


class ChatSummaryModel:
    def __init__(self):
        self.llm = ChatOpenAI(
            #model="",
            temperature=0.1,   
        )

    def language_generation(self, question):

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI. and your name is GNU-CORE"),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ])

        chain = prompt | self.llm
        result = chain.invoke({"question": question})

        return result.content
