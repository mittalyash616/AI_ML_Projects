
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import json
# Load environment variables (if using API keys or secrets)
load_dotenv()
# Load from env (Streamlit secrets or .env)
firebase_json = os.getenv("FIREBASE_CREDENTIALS") or st.secrets["FIREBASE_CREDENTIALS"]

# Convert to dictionary
firebase_dict = json.loads(firebase_json)

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_dict)
    firebase_admin.initialize_app(cred)
# Initialize Firebase Admin

# Connect to Firestore
db = firestore.client()

# Firestore state functions
def store_langgraph_state(thread_id, state):
    db.collection("langgraph_states").document(thread_id).set(state)
    st.success(f"✅ State stored successfully for thread_id: {thread_id}")

def get_langgraph_state(thread_id):
    doc = db.collection("langgraph_states").document(thread_id).get()
    if doc.exists:
        return doc.to_dict()
    else:
        return {"query": "", "content1": "", "content2": ""}

# Define the schema for LangGraph state
class state_content(TypedDict):
    query: str
    content1: str
    content2: str

# Define prompts and model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Prompt 1
prompt1 = ChatPromptTemplate.from_messages([
    ("system", "you are expert in giving answer"),
    ("human", """You are an assistant that answers user queries. 
Query: {topic}
Respond thoughtfully.""")
])
llm11 = prompt1 | llm | StrOutputParser()

# Prompt 2
prompt2 = ChatPromptTemplate.from_messages([
    ("system", "you are expert in giving answer"),
    ("human", """You are an assistant that answers user queries. 
Query: {topic}""")
])
llm22 = prompt2 | llm | StrOutputParser()

# Define execution logic for graph
def execute1(State: state_content):
    x = llm11.invoke({"topic": State["query"]})
    return {"content1": x}

def execute2(State: state_content):
    x = llm22.invoke({"topic": State["content1"]})
    return {"content2": x}

# Create and compile LangGraph
graph = StateGraph(state_content)
graph.add_node("llm1", execute1)
graph.add_node("llm2", execute2)
graph.add_edge(START, "llm1")
graph.add_edge("llm1", "llm2")
graph.add_edge("llm2", END)
app = graph.compile()

# -------------------- STREAMLIT UI --------------------
st.set_page_config(page_title="LangGraph + Firebase AI App", layout="centered")
st.title("🌐 LangGraph AI Pipeline")
st.markdown("This app runs a two-step Gemini-powered LangGraph pipeline and stores the state in Firebase Firestore.")

thread_id = st.text_input("Enter Thread ID", value="1234")

if "input_query" not in st.session_state:
    st.session_state["input_query"] = ""

st.session_state["input_query"] = st.text_input("Ask your query (e.g. 'What is AI?')", value=st.session_state["input_query"])

if st.button("🔁 Run Pipeline"):
    # Retrieve previous state (if exists)
    current_state = get_langgraph_state(thread_id)
    current_state["query"] = st.session_state["input_query"]

    # Run the LangGraph pipeline
    result = app.invoke(current_state)

    # Store final result in Firestore
    store_langgraph_state(thread_id, result)

    # Display output
    st.subheader("🧠 AI Output (Step 1)")
    st.write(result["content1"])

    st.subheader("🔄 AI Output (Step 2)")
    st.write(result["content2"])

if st.button("📂 Retrieve Stored State"):
    stored = get_langgraph_state(thread_id)
    st.json(stored)
