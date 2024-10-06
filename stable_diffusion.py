import requests
import io
from PIL import Image
'''
API_URL = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
headers = {"Authorization": "Bearer hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}
'''
API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
headers = {"Authorization": "Bearer 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"}

import os


# Enable CPU offloading (if necessary)

# Define the prompt

def generate_image(customer_prompt, suggestions):
    # Generate the image prompt
    prompt = f"This is the body features of the person: {customer_prompt}. Generate images imagining the person with the specified 3 outfit suggestions: {suggestions}"
    
    # Send a request to the Hugging Face API
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    
    # Check if the response was successful
    if response.status_code == 200:
        image_bytes = response.content
        image = Image.open(io.BytesIO(image_bytes))
        
        # Ensure the result_image directory exists
        os.makedirs('result_image', exist_ok=True)
        
        # Save the image inside the result_image directory
        image_path = os.path.join('result_image', 'generated_image.png')
        image.save(image_path)
        print(f"Image saved at: {image_path}")
        return image
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None
