from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import os
import langchain_core.chat_history as lc
from langchain_core.messages.base import message_to_dict
from langchain_core.messages.utils import messages_from_dict
from langchain_openai import AzureChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage, AnyMessage
from typing import List
import uvicorn
from datetime import datetime, timezone
from langchain_experimental.utilities import PythonREPL
from langchain_core.tools import Tool
from langgraph.graph import MessagesState
from langgraph.checkpoint.mongodb import MongoDBSaver
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition, ToolNode
from IPython.display import Image, display


app = FastAPI()
config_thread_id = [] #Keeps track of thread Ids to prevent duplicate Tool runs

# MongoDB setup for Persistence
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client["chatHistory"]
chat_collection = db["checkpoints"]

# Initialize the AI Model
llm = AzureChatOpenAI(
    azure_endpoint='',
    azure_deployment="",
    api_key='',
    api_version="",
    model_version="1",
    streaming=True,
)


python_repl = PythonREPL()
repl_tool = Tool(
    name="python_repl",
    description="A Python shell. Use this to execute python commands. Input should be a valid python command. Important point: If you want to see the output of a value, you should print it out with `print(...)`.",
    func=python_repl.run,
)

tools = [repl_tool]
llm_with_tools = llm.bind_tools(tools, tool_choice="auto")

SYSTEM_MESSAGE_CONTENT = (
    "You are a Data Science AI Agent with a Python shell. Use it to execute python commands. Input to the tool should be a valid python command. Important point: If you want to see the output of a value or result, you should print it out with `print(...)`. When given data, perform EDA and extract meaningful insights. Answer comprehensively and elaborately to questions."
)

# Define request and response models
class UserMessage(BaseModel):
    thread_id: str
    message: str

class AIResponse(BaseModel):
    response: str

def assistant(state: MessagesState):
   return {"messages": [llm_with_tools.invoke([SYSTEM_MESSAGE_CONTENT] + state["messages"])]}

checkpointer = MongoDBSaver(client=mongo_client, db_name="chatHistory", checkpoint_collection_name= "checkpoints", writes_collection_name= "checkpoint_writes")

builder = StateGraph(MessagesState)

# Define nodes
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

# Define edges
builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition,)
builder.add_edge("tools", "assistant")
react_graph_memory = builder.compile(checkpointer=checkpointer)


def get_chat_history(thread_id: str) -> List[AnyMessage]:
    config = {"configurable": {"thread_id": thread_id}}
    if react_graph_memory.get_state(config)[0]:
        messages = react_graph_memory.get_state(config)[0]['messages']
        for m in messages:
            if m.type == "ai" and m.tool_calls and (thread_id not in config_thread_id):
                #print("tool run")
                string_arg = m.tool_calls[0]["args"]["__arg1"]
                python_repl.run(string_arg)
                config_thread_id.append(thread_id)
        return messages
    else:
        return None 


def clear_chat_history(thread_id: str):
    """Clear the chat history for a user."""
    chat_collection.delete_many({"thread_id": thread_id})

#@app.post("/chat/", response_model=AIResponse)
@app.post("/chat/")
async def chat(user_message: UserMessage):
    thread_id = user_message.thread_id
    message = user_message.message

    config = {"configurable": {"thread_id": thread_id}}

    messages = [HumanMessage(content=message)]#.to_dict()
    
    messages = react_graph_memory.invoke({"messages": messages},config)
   
    return messages['messages']

@app.get("/chat_history/{thread_id}")
async def get_user_chat_history(thread_id: str):
    """
    Retrieve the chat history for a specific user.
    """
    messages = get_chat_history(thread_id)
    if not messages:
        raise HTTPException(status_code=404, detail="No chat history found for this user.")
    return {"chat_history": messages}

@app.post("/clear_history/{thread_id}")
async def clear_user_chat_history(thread_id: str):
    """
    Clear the chat history for a specific user.
    """
    clear_chat_history(thread_id)
    return {"message": f"Chat history for user {thread_id} cleared successfully"}

@app.get("/health/")
async def healthcheck():
    return {"Status":"healthy"}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080, log_level="info")