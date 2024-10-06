import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI

def generate_context(context, given_context):
    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = "AIzaSyBET2W7lgxi2_600MBj9UQJ5KgQ5mUrcgk"  # Replace with your actual API key

    llm = ChatGoogleGenerativeAI(model="gemini-pro")

    # Create a dictionary to structure the request
    request_data = {
        "context": context,
        "task": "Analyze the body types, color palettes of these celebrities. Provide a summary that describes how a person embodying characteristics from all five profiles might look, including an overview of their body type and suitable colors for clothing. Don't generate a very long response, not very too short too."
    }
    
    suggestion_request = {
        "context": context+ " The customer wants this : " + given_context,
        "task": "You are a stylist. You are given certain body profiles who might look similar to the customer. You are also given the requirements of the customer. Analyze the body types, color palettes of these celebrities. Analyze what the customer wants, considering her body types and similiar celebs suited dresses. Give top 3 outfit suggestions for the customer. It should be indian outfits, dont mention any celebrity names. Give the color and type of dress, justify why the dress will suit the customer."
    }
    # Convert the dictionary to a JSON string
    request_json = json.dumps(request_data)
    suggestion_json= json.dumps(suggestion_request)
    # Generating detailed physical profiles for actors
    result = llm.invoke(request_json)
    suggestion_result = llm.invoke(suggestion_json)
    # Save the result content to a file
    with open("gemini_actor_data.txt", "w") as f:
        f.write(result.content)

    return result.content, suggestion_result.content
