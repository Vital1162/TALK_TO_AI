import google.generativeai as genai
import os
from dotenv import load_dotenv, dotenv_values
load_dotenv()

# Configure the Google Generative AI client
genai.configure(api_key=os.getenv('GEMENI_API'))


model = genai.GenerativeModel('gemini-1.5-flash')

# print(model.generate_content('Chào!').text)