from dotenv import load_dotenv
load_dotenv()
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
#from utils import show_prompt
from Deep_research_from_scratch.prompts import clarify_with_user_instructions
llm=ChatOpenAI(model="gpt-4o-mini")

print(clarify_with_user_instructions)