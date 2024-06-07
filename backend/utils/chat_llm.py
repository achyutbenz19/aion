import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai.chat_models import ChatOpenAI

class ChatLLM:
    def __init__(self):
        self.llm = ChatGroq(temperature=0.2, model_name="mixtral-8x7b-32768", groq_api_key=os.environ.get("GROQ_API_KEY"))
        self.store = {}
        self.system_prompt = """
            You are Aion, an assistant model with access to several summaries of the user's activity. Your job is to recall the user's past history and serve as a personalized assistant based on the provided information. You will also be given the image URL in the context.

            Here is the context:
            {context}

            Answer the following based on the context ONLY IF THE QUERY IS RELEVANT TO THE CONTEXT. Your answer must be natural. Do not start with "Based on the context, I think...".
            {query}
        """
        
    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]
    
    def chat(self, query, docs):
        self.prompt = ChatPromptTemplate.from_messages([("system", self.system_prompt), ("human", query)])
        runnable = self.prompt | self.llm
        context_runnable = RunnableWithMessageHistory(
            runnable,
            self.get_session_history,
            input_messages_key="query",
        )
        
        return (context_runnable.invoke({"query": query, "context": docs}, config={"configurable": {"session_id": "abc123"}}).content)
