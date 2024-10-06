import pathlib
import textwrap
import google.generativeai as genai
# from google.colab import userdata
import PIL.Image
import google.ai.generativelanguage as glm
genai.configure(api_key= '')

def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
def get_text_for_image(image_dir):
    model = genai.GenerativeModel('gemini-1.5-pro')
    img = PIL.Image.open(image_dir)
    '''
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
    '''
    response = model.generate_content(
        [
            f"""Describe the features of the person present in the image under these categories:    
            1. Body type, Skin tone, facial features, Posture, overall Silhouette. 
            2. Other important features as a string, no need to describe the costume or accessories of the person. Just want to know about the body features of the person. Give response as a JSON with features and other details as keys. Features need to be json in itself.

            """,
            img
        ],
        stream=False
    )


    response.resolve()
    # to_markdown(response.text)
    print(response.text)
    return response.text
