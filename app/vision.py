import os

import json
import base64
import logging
import requests
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

api_key = os.getenv("OPENAI_KEY")

class Vision:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    model = "gpt-4-vision-preview"
    max_tokens = 300

    @staticmethod
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    @staticmethod
    def encode_image_from_url(image_url):
        response = requests.get(image_url)
        return base64.b64encode(response.content).decode('utf-8')

    @staticmethod
    def resize_image(image_path, size):
        original_image = Image.open(image_path)
        resized_image = original_image.resize(size)
        resized_image.save(image_path)

    @staticmethod
    def annotate_images(image_paths_or_urls):
        annotated_images = []
        for image_path_or_url in image_paths_or_urls:
            try:
                if image_path_or_url.startswith("http"):
                    base64_image = Vision.encode_image_from_url(image_path_or_url)
                else:
                    Vision.resize_image(image_path_or_url, (1920, 1080))  # Resize the image before encoding it
                    base64_image = Vision.encode_image(image_path_or_url)
                
                payload = {
                    "model": Vision.model,
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "What is in this image?"
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}"
                                    }
                                }
                            ]
                        }
                    ],
                    "max_tokens": Vision.max_tokens
                }
                response = requests.post("https://api.openai.com/v1/chat/completions", headers=Vision.headers, json=payload)
                if response.status_code == 200:
                    result = json.loads(response.content)
                    # Process the result as needed
                    description = result["choices"][0]["message"]["content"].strip()
                    annotated_image = {
                        "image_path_or_url": image_path_or_url,
                        "description": description,
                    }
                    annotated_images.append(annotated_image)
                else:
                    logging.error(f"Request failed with status code {response.status_code}, response: {response.content}")
            except Exception as e:
                # Log the error and continue to the next image
                logging.error(f"Failed to annotate image {image_path_or_url}. Error: {e}")

        return annotated_images



if __name__ == "__main__":
    image_paths_or_urls = [
        "/Users/BilalRaza/Downloads/imageforAI1.jpeg",
        "/Users/BilalRaza/Downloads/imageforAI2.jpeg"
        ]
    annotated_images = Vision.annotate_images(image_paths_or_urls)
    print(annotated_images)
    with open("annotated_images.json", "w") as f:
        json.dump(annotated_images, f)