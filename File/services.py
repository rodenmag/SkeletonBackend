#import google.generativeai as genai
from google import genai
from django.conf import settings

client = genai.Client(api_key='AIzaSyAfmAj6DwmZsg00p9nH3Jozh2Kat11OxEI')

#model = genai.GenerativeModel("gemini-2.5-flash")

def compare_documents(text_a: str, text_b: str):
    prompt = f"""
    You are a document comparison assistant.

    Compare Document A and Document B.

    Return:
    1. Summary of differences
    2. Added content
    3. Removed content
    4. Modified content

    Document A:
    {text_a}

    Document B:
    {text_b}
    """

    #response = model.generate_content(prompt)
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        #model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text