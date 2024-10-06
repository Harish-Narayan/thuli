import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

# Load the processor and model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

# Load your local image
img_path = '/Users/harish/Downloads/Bipasha Basu Is The Bridesmaid Every Sister Wants At Her Wedding!.jpeg'  # Change this to your local image path
raw_image = Image.open(img_path).convert('RGB')

# Define the questions to ask the model
questions = [
    "Describe the color of the dress in detail.",
    "What is the style and silhouette of the dress? Please include details about the neckline and sleeves.",
    "What materials are used in the dress? Describe the fabric and its texture.",
    "What cultural or historical significance does this style of dress have in a wedding context?",
    "How does the dress complement the wearer? Focus on the fit and overall appearance.",
    "What are the unique design features of this dress?",
    "Explain the significance of the dress in a wedding setting."
]

# Store the answers
answers = []

# Iterate over each question and generate the response
for question in questions:
    # Prepare the input by combining the image and the question
    inputs = processor(raw_image, question, return_tensors="pt")

    # Generate the response with adjusted parameters
    out = model.generate(**inputs, max_length=256, temperature=0.9, top_p=0.95)

    # Decode the response and add it to the answers list
    answer = processor.decode(out[0], skip_special_tokens=True)
    
    # Check if the answer is similar to the question and re-generate if needed
    if answer.lower() == question.lower():
        print(f"Re-generating for question: {question}")
        continue  # Skip adding the repeated answer
    answers.append(answer)

# Combine all the answers into a single detailed description
detailed_description = "\n\n".join(answers)

# Print the combined description
print(detailed_description)
