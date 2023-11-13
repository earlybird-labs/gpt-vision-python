import json
import base64
import logging
import requests

class Vision:
    api_key = "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"
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
    def annotate_images(image_paths_or_urls):
        annotated_images = []
        for image_path_or_url in image_paths_or_urls:
            try:
                if image_path_or_url.startswith("http"):
                    base64_image = Vision.encode_image_from_url(image_path_or_url)
                else:
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
                response = requests.post(
                    "https://api.openai.com/v1/engines/davinci-codex/completions",
                    headers=Vision.headers,
                    data=json.dumps(payload)
                )
                if response.status_code == 200:
                    result = json.loads(response.content)
                    # Process the result as needed
                    description = result["choices"][0]["message"]["content"].strip()
                    keywords = result["choices"][0]["message"]["keywords"]
                    annotated_image = {
                        "image_path_or_url": image_path_or_url,
                        "description": description,
                        "keywords": keywords
                    }
                    annotated_images.append(annotated_image)
                else:
                    logging.error(f"Request failed with status code {response.status_code}")
            except Exception as e:
                # Log the error and continue to the next image
                logging.error(f"Failed to annotate image {image_path_or_url}. Error: {e}")

        return annotated_images

if __name__ == "__main__":
    image_paths_or_urls = [
        "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.nature.com%2Farticles%2F528452a&psig=AOvVaw0RTB0Ql1AXbFOymp6f_D4g&ust=1699988340683000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCKiumZvUwYIDFQAAAAAdAAAAABAE",
        "https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2F9%2F9a%2FGull_portrait_ca_usa.jpg&tbnid=0DzWhtJoQ1KWgM&vet=12ahUKEwiHpM-a1MGCAxV5TTABHSY8A6oQMyhcegUIARDLAg..i&imgrefurl=https%3A%2F%2Fcommons.wikimedia.org%2Fwiki%2FCommons%3AQuality_images&docid=cIQ7wXCEtJiOWM&w=2272&h=1704&q=images&ved=2ahUKEwiHpM-a1MGCAxV5TTABHSY8A6oQMyhcegUIARDLAg",
        "https://www.google.com/imgres?imgurl=https%3A%2F%2Fcdn.pixabay.com%2Fphoto%2F2013%2F07%2F21%2F13%2F00%2Frose-165819_640.jpg&tbnid=t1X5lcWFswI5RM&vet=10CCIQMyh3ahcKEwiorpmb1MGCAxUAAAAAHQAAAAAQCA..i&imgrefurl=https%3A%2F%2Fpixabay.com%2Fimages%2Fsearch%2Fflowers%2F&docid=6QnaOLvEQovLfM&w=640&h=424&itg=1&q=images&ved=0CCIQMyh3ahcKEwiorpmb1MGCAxUAAAAAHQAAAAAQCA"
        ]
    annotated_images = Vision.annotate_images(image_paths_or_urls)
    with open("annotated_images.json", "w") as f:
        json.dump(annotated_images, f)