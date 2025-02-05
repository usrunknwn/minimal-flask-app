from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")  # Securely load API key

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    image_url = None
    if request.method == "POST":
        prompt = request.form["prompt"]
        try:
            # Generate text response using GPT-4o-mini
            response = openai.chat.completions.create(
                model="gpt-4o-mini",  
                messages=[
                    {"role": "developer", "content": "You are a thorough assistant. Your responses are short and smart. Avoid predictable phrasing."}, 
                    {"role": "user", "content": prompt}
                ],
                temperature=1.2,
                max_completion_tokens=50
            )
            result = response.choices[0].message.content

            # Combine the question and response for image prompt
            image_prompt = f"Create a hyperrealistic photography inspired by the question: '{prompt}' and the response: '{result}'."
            
            # Generate image using DALL·E (OpenAI Image API)
            image_response = openai.OpenAI().images.generate(
                model="dall-e-2",
                prompt=image_prompt,
                size="512x512",
                quality="standard",
                n=1,
            )
            image_url = image_response.data[0].url
            print (image_url)
        except Exception as e:
            result = f"Error: {str(e)}"
    return render_template("index.html", result=result, image_url=image_url)

if __name__ == "__main__":
    app.run(debug=True)  # Run locally for testing
