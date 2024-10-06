from get_image_text import get_text_for_image
from RAG_fusion_2 import rrf_retriever
import google.generativeai as genai

import os
from get_image_text import get_text_for_image
from RAG_fusion_2 import rrf_retriever
import google.generativeai as genai
from gemini import generate_context
from RAG_fusion import dress_retriever
from stable_diffusion import generate_image

def process_results(image_path,customer_context):
    similiar_names=set()
    # Step 1: Extract text from the image
    extracted_text = get_text_for_image(image_path)
    print("Extracted Text from Image:")
    print(extracted_text)

    # Step 2: Call RAG fusion using the extracted text
    retrieved_documents = rrf_retriever(extracted_text)

    # Step 3: Output retrieved documents
    print("\nRetrieved Documents:")
    profiles = []
    for doc in retrieved_documents:
        filename = doc.metadata.get('filename', 'N/A')
        print("hi",type(doc.page_content[:100]),"hi")
        print(f"Filename: {filename}, Content: {doc.page_content[:100]}...\n")
        content = doc.page_content[:100]
        start = content.find('"') + 1
        end = content.find('":')
        name = content[start:end].strip()
        similiar_names.add(name)

        # Load the actress profile from the corresponding text file
        profile_path = os.path.join("actress_profile", f"{name}.txt")  # Assuming the filename corresponds to the profile
        if os.path.exists(profile_path):
            with open(profile_path, 'r', encoding='utf-8') as file:
                profile_content = file.read()
                profiles.append(profile_content)
        else:
            print(f"Profile file for {doc.page_content[:100]} not found.")

    # Step 4: Combine all profiles into a single string
    all_profiles_content = "\n\n".join(profiles)
    print("\nCombined Profiles Content:")
    celebrity_context, suggested_outfits = generate_context(all_profiles_content, customer_context)
    total_context= f"{customer_context},      {celebrity_context}"
    retrieved_dress = dress_retriever(total_context)
    for doc in retrieved_dress:
        filename = doc.metadata.get('filename', 'N/A')
        print("hi",type(doc.page_content[:100]),"hi")
        print(f"Filename: {filename}, Content: {doc.page_content[:100]}...\n")
        content = doc.page_content[:100]
        start = content.find('"') + 1
        end = content.find('":')
        name = content[start:end].strip()
        similiar_names.add(name)
    print(similiar_names,suggested_outfits)
    generate_image(extracted_text, suggested_outfits)
    return

if __name__ == "__main__":
    # Example usage
    image_path = "/Users/harish/Downloads/Celebrity/Katrina Kaif.jpeg"  # Replace with the actual image path
    customer_context=""
    process_results(image_path,customer_context)
