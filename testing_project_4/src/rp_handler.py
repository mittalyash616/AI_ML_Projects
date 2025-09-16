import runpod
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser


def handler(event):
    """
    RunPod handler function that processes incoming requests.
    
    Args:
        event (dict): Contains the input data and request metadata
                      Example:
                      {
                          "input": {
                              "message": "Hello AI!"
                          }
                      }

    Returns:
        dict: Response with the model's reply
    """
    print("Worker started...")

    # Extract input safely
    input_data = event.get("input", {})
    message = input_data.get("message", "")

    if not message:
        return {"error": "No message provided"}

    print(f"Received message: {message}")

    # Initialize the model
    llm = ChatOpenAI(model="gpt-4o-mini")

    # Create the chain
    chain = llm | StrOutputParser()

    # Invoke chain
    result = chain.invoke(message)

    print(f"Reply: {result}")

    return {"reply": result}


# Start the RunPod serverless worker
if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
