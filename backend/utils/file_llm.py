import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai.chat_models import ChatOpenAI

class FileLLM:
    def __init__(self):
        self.llm = ChatGroq(temperature=0.1, model_name="mixtral-8x7b-32768")
        self.prompt = """
            You are a jpg name editor. Respond with ONLY the jpg file name, nothing else. Here is the content inside the file: \
            {query} \
            Remember to output only ONE file name.
        """
        
    def chat(self, query):
        self.prompt = ChatPromptTemplate.from_messages([("system", self.prompt), ("human", query)])
        runnable = self.prompt | self.llm
        response = runnable.invoke({"query": query})
        return self.clean_response(response.content)
    
    def clean_response(self, output):
        cleaned_output = output.replace('"', '')
        cleaned_output = cleaned_output.replace(' ', '_')
        if not cleaned_output.endswith('.jpg'):
            cleaned_output += '.jpg'
        return cleaned_output
        