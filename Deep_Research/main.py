from dotenv import load_dotenv
load_dotenv()
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from Deep_research_from_scratch.utils import show_prompt,format_messages
from Deep_research_from_scratch.prompts import clarify_with_user_instructions , transform_messages_into_research_topic_prompt
from langgraph.graph import StateGraph, START, END
from datetime import datetime
from typing_extensions import Literal

from langgraph.checkpoint.memory import InMemorySaver

from langchain_core.messages import HumanMessage, AIMessage, get_buffer_string
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from Deep_research_from_scratch.state_scope import AgentState, ClarifyWithUser, ResearchQuestion, AgentInputState
model=ChatOpenAI(model="gpt-4o-mini")
def get_today_str() -> str:
    """Get current date in a human-readable format."""
    return datetime.now().strftime("%a %b %-d, %Y")


def clarify_with_user(state: AgentState):
    """
    Determine if the user's request contains sufficient information to proceed with research.
    
    Uses structured output to make deterministic decisions and avoid hallucination.
    Routes to either research brief generation or ends with a clarification question.
    """
    # Set up structured output model
    structured_output_model = model.with_structured_output(ClarifyWithUser)

    # Invoke the model with clarification instructions
    response = structured_output_model.invoke([
        HumanMessage(content=clarify_with_user_instructions.format(
            messages=get_buffer_string(messages=state["messages"]), 
            date=get_today_str()
        ))
    ])
    
    # Route based on clarification need
    if response.need_clarification:
        return Command(
            goto=END, 
            update={"messages": [AIMessage(content=response.question)]}
        )
    else:
        return Command(
            goto="write_research_brief", 
            update={"messages": [AIMessage(content=response.verification)]}
        )

def write_research_brief(state: AgentState):
    """
    Transform the conversation history into a comprehensive research brief.
    
    Uses structured output to ensure the brief follows the required format
    and contains all necessary details for effective research.
    """
    # Set up structured output model
    #structured_output_model = model.with_structured_output(ResearchQuestion)
    
    # Generate research brief from conversation history
    # response = structured_output_model.invoke([
    #     HumanMessage(content=transform_messages_into_research_topic_prompt.format(
    #         messages=get_buffer_string(state.get("messages", [])),
    #         date=get_today_str()
    #     ))
    # ])
    response = model.invoke([
        HumanMessage(content=transform_messages_into_research_topic_prompt.format(
            messages=get_buffer_string(state.get("messages", [])),
            date=get_today_str()
        ))
    ])
    print(response)
    # Update state with generated research brief and pass it to the supervisor
    return {
        "research_brief": response.research_brief,
        "supervisor_messages": [HumanMessage(content=f"{response.research_brief}.")]
    }





deep_researcher_builder = StateGraph(AgentState, input_schema=AgentInputState)
deep_researcher_builder.add_node("clarify_with_user", clarify_with_user)
deep_researcher_builder.add_node("write_research_brief", write_research_brief)

deep_researcher_builder.add_edge(START, "clarify_with_user")
deep_researcher_builder.add_edge("write_research_brief", END)


checkpointer = InMemorySaver()
scope = deep_researcher_builder.compile(checkpointer=checkpointer)
from rich.console import Console
from rich.markdown import Markdown
console = Console()
thread = {"configurable": {"thread_id": "1"}}
result = scope.invoke({"messages": [HumanMessage(content="Also, could you include details about the ambiance and seating options in each place?")]}, config=thread)
format_messages(result['messages'])

print(result)