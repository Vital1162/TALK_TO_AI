import google.generativeai as genai
import os
from dotenv import load_dotenv, dotenv_values
load_dotenv()

# Configure the Google Generative AI client
genai.configure(api_key=os.getenv('GEMENI_API'))

# temperature, top_p, top_k, max_output_tokens = ...
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 512,
}


model = genai.GenerativeModel('gemini-1.5-flash')

# def stream_response(prompt):
#     # Generate content with streaming enabled
#     response = model.generate_content(prompt, stream=True)
    
#     # Iterate through the streaming response
#     for chunk in response:
#         if chunk.text:
#             print(chunk.text, end='', flush=True)
#     print()  # New line after the response is complete

# user_input = input("Enter your prompt: ")
# response = model.generate_content(user_input,
#                                   generation_config=generation_config)
# print(response.text)