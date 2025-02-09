from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langgraph.graph import Graph, END
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

class SupportAgent:
    def __init__(self, name, role, llm):
        self.name = name
        self.role = role
        self.llm = llm

    def respond(self, message):
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=f"You are a {self.role}. Your name is {self.name}"),
            HumanMessage(content=message)
        ])
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({})

# Initialize LLM and agents
api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="deepseek-r1-distill-llama-70b", api_key=api_key)
Agent1 = SupportAgent(name="Alok", role="Billing Specialist", llm=llm)
Agent2 = SupportAgent(name="Ankit", role="Technical Support Agent", llm=llm)
Agent3 = SupportAgent(name="Aman", role="Support Manager", llm=llm)

# Define workflow
def billing_specialist(query):
    response = Agent1.respond(query)
    return response

def technical_support(query):
    response = Agent2.respond(query)
    return response

def manager_work(query):
    response = Agent3.respond(query)
    return response

workflow = Graph()
workflow.add_node("billing", billing_specialist)
workflow.add_node("technical", technical_support)
workflow.add_node("manager", manager_work)
workflow.add_edge("billing", "technical")
workflow.add_edge("technical", "manager")
workflow.add_edge("manager", END)
workflow.set_entry_point("billing")
app_workflow = workflow.compile()

@app.post("/process-query")
async def process_query(request: QueryRequest):
    try:
        result = app_workflow.invoke(request.query)
        return {"success": True, "response": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)