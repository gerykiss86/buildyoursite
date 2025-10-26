import os
import requests
import uuid
import re
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_image(prompt):
    """Generate an image using Google's Imagen API"""
    api_key = os.getenv('GOOGLE_API_KEY')

    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")

    # Always instruct photorealism in the prompt
    photorealistic_prompt = f"photorealistic, {prompt}"

    # Try using Imagen 3.0 with predict method
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key={api_key}"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "instances": [{
            "prompt": photorealistic_prompt
        }],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": "1:1",
            "safetyFilterLevel": "block_some",
            "personGeneration": "allow_adult"
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        # Try to extract and save the generated image
        if 'predictions' in result and len(result['predictions']) > 0:
            import base64
            prediction = result['predictions'][0]
            if 'bytesBase64Encoded' in prediction:
                image_data = base64.b64decode(prediction['bytesBase64Encoded'])
            elif 'image' in prediction:
                image_data = base64.b64decode(prediction['image'])
            else:
                print("Unexpected response format:", prediction)
                return None

            # Create filename based on prompt content and unique GUID
            # Sanitize prompt for filename (keep alphanumeric and spaces, replace spaces with underscores)
            sanitized_prompt = re.sub(r'[^\w\s-]', '', prompt)[:50]  # Limit to 50 chars
            sanitized_prompt = re.sub(r'\s+', '_', sanitized_prompt.strip())

            # Generate unique identifier
            unique_id = str(uuid.uuid4())[:8]

            # Create output directory if it doesn't exist
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)

            # Construct filename with output subfolder
            output_file = os.path.join(output_dir, f"{sanitized_prompt}_{unique_id}.png")

            with open(output_file, 'wb') as f:
                f.write(image_data)
            print(f"Image generated successfully: {output_file}")
            return output_file
        else:
            print("No predictions in response")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python generate_image_bulk.py \"prompt1\" \"prompt2\" \"prompt3\" ...")
        sys.exit(1)

    prompts = sys.argv[1:]
    print(f"Generating {len(prompts)} image(s)...\n")

    max_retries = 3
    retry_delay = 2  # seconds
    batch_delay = 1  # delay between different prompts

    for i, prompt in enumerate(prompts, 1):
        print(f"[{i}/{len(prompts)}] Generating image with prompt: {prompt}")

        for attempt in range(max_retries):
            result = generate_image(prompt)
            if result:
                break

            if attempt < max_retries - 1:
                print(f"  Retrying ({attempt + 2}/{max_retries}) in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print(f"  Failed after {max_retries} attempts")

        # Add delay between different prompts to avoid rate limiting
        if i < len(prompts):
            time.sleep(batch_delay)

        print()
