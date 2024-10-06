import pathlib
import textwrap
import google.generativeai as genai
import PIL.Image
import os
import time  # Import time for sleep functionality

# Set up the API key and configuration
os.environ["GOOGLE_API_KEY"] = "AIzaSyBET2W7lgxi2_600MBj9UQJ5KgQ5mUrcgk"  # Replace with your actual API key
genai.configure(api_key='')

def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

model = genai.GenerativeModel('gemini-1.5-flash-latest')

# Directory containing the images
image_directory = '/Users/harish/Downloads/Celebrity/'
output_directory = pathlib.Path('doc_text')  # Directory for output text files

# Create the output directory if it doesn't exist
output_directory.mkdir(exist_ok=True)

# List to store images that failed processing
failed_images = []

# Loop through all JPEG files in the specified directory
for image_path in pathlib.Path(image_directory).glob('*.jpeg'):
    try:
        # Open the image
        img = PIL.Image.open(image_path)
        
        # Generate content using the model
        response = model.generate_content(
            [
                f"""
                Describe the color of the dress in detail.
                What is the style and silhouette of the dress? Please include details about the neckline and sleeves.
                What materials are used in the dress? Describe the fabric and its texture.
                What cultural or historical significance does this style of dress have in a wedding context?
                How does the dress complement the wearer? Focus on the fit and overall appearance.
                Explain the body type of the person and the other body features of the person and why is this dress suitable for the person.
                Explain the occasion and location it happens. Justify why this outfit will suit the place.
                Don't generate a very lengthy response. One line explanation for each question will do. Combine all the answers into a paragraph and describe as the response.
                """,
                img
            ],
            stream=False
        )
        
        # Resolve the response
        response.resolve()
        
        # Create a text file for each celebrity and write the response
        output_file = output_directory / f"{image_path.stem}.txt"  # Use the image name as the text file name
        with open(output_file, 'w') as file:
            file.write(response.text)
        
        print(f"Response for {image_path.name} saved to {output_file.name}")
        
    except Exception as e:
        print(f"Error processing {image_path.name}: {e}")
        if "429" in str(e):
            failed_images.append(image_path)  # Add to failed images list

# Retry processing for failed images
for image_path in failed_images:
    retries = 3  # Number of retries
    for attempt in range(retries):
        try:
            # Open the image again
            img = PIL.Image.open(image_path)

            # Generate content using the model
            response = model.generate_content(
                [
                    f"""
                    Describe the color of the dress in detail.
                    What is the style and silhouette of the dress? Please include details about the neckline and sleeves.
                    What materials are used in the dress? Describe the fabric and its texture.
                    What cultural or historical significance does this style of dress have in a wedding context?
                    How does the dress complement the wearer? Focus on the fit and overall appearance.
                    Explain the body type of the person and the other body features of the person and why is this dress suitable for the person.
                    Explain the occasion and location it happens. Justify why this outfit will suit the place.
                    Don't generate a very lengthy response. One line explanation for each question will do. Combine all the answers into a paragraph and describe as the response.
                    """,
                    img
                ],
                stream=False
            )
            
            # Resolve the response
            response.resolve()

            # Create a text file for each celebrity and write the response
            output_file = output_directory / f"{image_path.stem}.txt"
            with open(output_file, 'w') as file:
                file.write(response.text)

            print(f"Response for {image_path.name} saved to {output_file.name}")
            break  # Break out of retry loop on success

        except Exception as retry_e:
            print(f"Retry {attempt + 1} for {image_path.name} failed: {retry_e}")
            if "429" in str(retry_e):
                time.sleep(5)  # Wait for 5 seconds before retrying
            else:
                break  # Break retry loop on other exceptions

