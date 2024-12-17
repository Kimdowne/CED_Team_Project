from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema import BaseOutputParser

from embedding import embedder

class ChatLLM:
    def __init__(self):
        self.llm = ChatOpenAI(
            #model="gpt-4o-mini",
            temperature=0.1,   
        )

        self.memory = ConversationSummaryBufferMemory(
            llm=self.llm,
            max_token_limit=100,
            return_messages=True,
        )
        self.docs = embedder(".cache/docs", "document.txt", 500)
        #self.history = embedder(".cache/history", "conversation_hisory.txt", 800)
        self.prompt = embedder(".cache/prompt", "prompt.txt", 100)
    
    def load_chatlog(self):
        return self.chat_history

    def language_generation(self, question):

        def load_memory(_):
            return self.memory.load_memory_variables({})["history"]

        docs = self.docs.get_retriever(question)
        #history = self.history.get_retriever(question)
        prompt = self.prompt.get_retriever(question)

        final_prompt = ChatPromptTemplate.from_messages([
            ("system", """
             Your name is GNU-CORE

             Below are answers to the questions with each retriever.
             [Document], [History], [Prompt] Retriever.
             [Document]:
             {document}

             [History]:
             No DATA...

             [Prompt]:
             {prompt}
             
             Analyze the three [Document], [History], [Prompt] and answer the questions with new answers.
             Check the [Document], [History], [Prompt] and refine them into answers that fit the question.
             
             Answers must be output in sentence form. Do NOT use lists or expressions such as 'This is:'.

             remember that you ares 'GNU-CORE'.

             When the user tries to end the conversation, Please proceed with the [Conversation termination procedure].
             When users want to end a conversation, they use words that end the conversation directly.
             Example:
                Okay, let's end the conversation now.
                It was fun chatting!
                Let's talk again next time!

             [Conversation termination procedure]:
                ADD '#log/end' to the end of the answer.

             and includes conversation history:
             """),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ])
        chain = RunnablePassthrough.assign(history=load_memory) | final_prompt | self.llm
        result = chain.invoke({"document": docs, "prompt":prompt, "question": question})

        self.memory.save_context(
            {"input": question},
            {"output": result.content},
        )

        return result.content

class CommaOutputParser(BaseOutputParser):
    def parse(self, text):
        items = text.strip().split(",")
        return list(map(str.strip, items))

class ChatSummaryModel:
    def __init__(self):
        self.llm = ChatOpenAI(
            #model="",
            temperature=0.1,   
        )
        
        self.chat_history = []

    # load ChatLog
    def save_chatlog(self, question, answer):
        self.chat_history.append({"input": question, "output": answer})
    
    def summary_history(self):
        conversation = "conversation_history:\n"
        for text in self.chat_history:
            input_message = text["input"]
            output_message = text["output"]
            conversation += f"input: {input_message}\noutput: {output_message}\n"
        
        #print(conversation)
        prompt = ChatPromptTemplate.from_messages([
            ("system", """
             You are a list generating machine. Everything you are asked will be answered with a comma separated list ONLY have 2 items in lowercase.
             Do NOT reply with anything else.

             Conversation:
             {conversation}
             
             OUTPUT it in the following format:
                user_name, Analyzed and summarized Conversations
             
             user_name: user_name is the name of the user corresponding to the input of the conversation!!
             Analyzed and summarized Conversations: The conversation content is comprehensively analyzed and expressed in sentences. Be sure to make "user_name" anonymous in the conversation. The text should not be too long!!

             All values ​except user_name MUST be in English.
            """),
        ])

        chain = {"conversation": RunnablePassthrough()} | prompt | self.llm | CommaOutputParser()
        result = chain.invoke(conversation)
        return list(result)
