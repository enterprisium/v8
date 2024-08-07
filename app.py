LLM = "Gemini"
MODEL = "turbo"


import re
import json
import pprint
from g4f.client import Client
from hercai import Hercai
from g4f.client import Client
import google.generativeai as genai

gemini_apikey = "AIzaSyC6N1MVe9WmAFjWMNuXjlaLnYa8eO813tY"

def Genrate_Script_And_Prompts(prompt, LLM, model=None):
    if LLM == "G4F":
        client = Client()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        response_text = response.choices[0].message.content.strip()



    elif LLM == "Gemini":
        if not gemini_apikey:
            raise ValueError("Gemini API key is missing!")
        genai.configure(api_key=gemini_apikey)
        gemini_model = genai.GenerativeModel('gemini-pro')  # Specify Gemini model here
        response = gemini_model.generate_content(prompt)  # Use gemini_model
        response_text = response.text




    elif LLM == "Hercai":
        model = MODEL
        herc = Hercai("")  # Provide Hercai api key (optional)
        response = herc.question(model=model, content=prompt)
        response_text = response["reply"]

    else:
        raise ValueError("Invalid LLM selected")




    # Extract JSON from the response
    json_match = re.search(r'\[[\s\S]*\]', response_text)
    if json_match:
        json_str = json_match.group(0)
        if not json_str.endswith(']'):
            json_str += ']'
        output = json.loads(json_str)
    else:
        raise ValueError("Invalid JSON")

    pprint.pprint(output)
    image_prompts = [item['image_description'] for item in output]
    sentences = [item['sentence'] for item in output]

    return image_prompts, sentences




# Daily motivation, personal growth and positivity
topic = "Success and Achievement"
goal = "inspire people to overcome challenges, achieve success, and celebrate their victories"

prompt_prefix = f"""You are tasked with creating a script for a {topic} video that is about 30 seconds.
Your goal is to {goal}.
Please follow these instructions to create an engaging and impactful video:
1. Begin by setting the scene and capturing the viewer's attention with a captivating visual.
2. Each scene cut should occur every 5-10 seconds, ensuring a smooth flow and transition throughout the video.
3. For each scene cut, provide a detailed description of the stock image being shown.
4. Along with each image description, include a corresponding text that complements and enhances the visual. The text should be concise and powerful.
5. Ensure that the sequence of images and text builds excitement and encourages viewers to take action.
6. Strictly output your response in a JSON list format, adhering to the following sample structure:"""

sample_output = """
   [
       { "image_description": "Description of the first image here.", "sentence": "Text accompanying the first scene cut." },
       { "image_description": "Description of the second image here.", "sentence": "Text accompanying the second scene cut." }
   ]
"""

prompt_postinstruction = f"""By following these instructions, you will create an impactful {topic} short-form video.
Output:"""

prompt = prompt_prefix + sample_output + prompt_postinstruction


image_prompts, sentences = Genrate_Script_And_Prompts(prompt, LLM)
print("image_prompts:", image_prompts)
print("sentences:", sentences)
print("Number of sentences:", len(sentences))
