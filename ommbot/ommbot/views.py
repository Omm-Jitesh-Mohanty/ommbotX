# Import the necessary libraries
import os
from dotenv import load_dotenv
from django.shortcuts import render
from django.http import JsonResponse
import google.generativeai as genai # Import the Google AI library

# Load environment variables from your .env file
# Make sure your .env file is in a secure location and not exposed publicly
load_dotenv(dotenv_path="C:/Users/ommji_mttma5p/OneDrive/Desktop/Django Project/ommbot/key.env")

# --- MODIFICATION 1: Configure the Gemini API ---
# Configure the Gemini API with the key from your .env file
# Note: We are using "GEMINI_API_KEY" which you should set in your key.env file
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # Handle the case where the API key is not found
    # You might want to raise an error or log a warning
    print("Error: GEMINI_API_KEY not found in environment variables.")
else:
    genai.configure(api_key=api_key)

# --- MODIFICATION 2: Update the completion function for Gemini ---
def get_completion(prompt):
    """
    This function takes a prompt and returns the Gemini model's response.
    """
    print(f"Received prompt: {prompt}")
    try:
        # Initialize the Generative Model. 
        # 'gemini-1.5-flash' is a fast and versatile model.
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Send the prompt to the model and get the response
        response = model.generate_content(prompt)
        
        # Extract the text from the response
        reply = response.text
        
        print(f"Model reply: {reply}")
        return reply
    except Exception as e:
        # Handle potential errors during the API call, such as configuration issues
        print(f"An error occurred: {e}")
        return "Sorry, I'm having trouble connecting to the AI service right now. Please check the server logs."


# --- NO MODIFICATION NEEDED HERE ---
# This view function remains the same. It handles the web request and response.
def query_view(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        if not prompt:
            return JsonResponse({'error': 'Prompt cannot be empty.'}, status=400)
        
        response = get_completion(prompt)
        return JsonResponse({'response': response})
        
    return render(request, 'index.html')
