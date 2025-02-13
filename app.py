from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    image_url = None

    if request.method == "POST":
        prompt = request.form["prompt"]
        
        try:
            # Generate Jungian dream interpretation
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a Jungian psychoanalyst providing deep dream interpretations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            result = response.choices[0].message.content

            # Generate dream visualization image
            image_response = openai.images.generate(
                model="dall-e-3",
                prompt=f"An abstract dream representation based on: {prompt}",
                n=1,
                size="1024x1024"
            )
            image_url = image_response.data[0].url

        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template("index.html", result=result, image_url=image_url)

if __name__ == "__main__":
    app.run(debug=True)
