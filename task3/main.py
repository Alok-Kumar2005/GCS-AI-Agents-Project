from langgraph.graph import Graph ,END
from langchain_core.messages import HumanMessage , SystemMessage 
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")


class suportAgent:
    def __init__(self , name , role , llm):
        self.name = name
        self.role = role
        self.llm = llm

    def respond(self , message):
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content = f"You are a  { self.role} . Your name is {self.name}"),
            HumanMessage(content=message)
        ])
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({})
    

llm = ChatGroq(model = "deepseek-r1-distill-llama-70b",
               api_key = api_key)

Agent1 = suportAgent(name = "Alok" , role = "Billing Specialist" , llm=llm)
Agent2 = suportAgent(name = "Ankit" , role="Technical Suport Agent" , llm = llm)
Agent3 = suportAgent(name = "Aman" , role = "Suport manager" , llm = llm)

def billingSpecialist(query):
    print("Agent1 --> ")
    response1 = Agent1.respond(query)
    print(f"Agent1 response: {response1}")
    return response1

def technicalSuport(query):
    print("Agent2 -->")
    response2 = Agent2.respond(query)
    print(f"Agent2 response: {response2}")
    return response2

def managerWork(query):
    print("Agent3 -- >")
    response3 = Agent3.respond(query)
    print(f"Agent3 response: {response3}")
    return response3

workflow = Graph()

## giving name to the nodes
workflow.add_node("billing" , billingSpecialist)
workflow.add_node("technical" , technicalSuport)
workflow.add_node("manager" , managerWork)


## Adding edges between them
workflow.add_edge("billing" , "technical")
workflow.add_edge("technical" , "manager")
workflow.add_edge("manager" , END)

workflow.set_entry_point("billing")

## compile the workfloe
app = workflow.compile()

def start(query):
    print(f"Customer query: {query}")
    result = app.invoke(query)
    print(f"Final Answer : {result}")


start("i am getting error in latest update")