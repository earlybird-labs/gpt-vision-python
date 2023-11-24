# Image Captioning Tool

Input is a folder of images, business description

`sample_prompt = f"Categorize and describe the image in the format of json with the keys of ('description': str, 'keywords': list[str]) for {business_description}`

### Cleaning Output

```python
import json

print(response)

try:
    data = json.loads(response)

except json.decoder.JSONDecodeError:

    json_string = response.replace("```json\n", "").replace("\n```", "")

    data = json.loads(json_string)

print(data['keywords'][0:2])
```

### Uploading Local Images

```python
import base64
import requests

# OpenAI API Key
api_key = "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"

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "path_to_your_image.jpg"

# Getting the base64 string
base64_image = encode_image(image_path)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "What’s in this image?"
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
    "max_tokens": 300
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

print(response.json())
```

### Task

1. Create vision.py that has a class called Vision that has functions to read images from path or a url
2. Create a function that uses the above function by opening a file path and iterating through folders or taking in an array of urls. (When iterating use try and except to catch errors, saving the progress to a list)
3. 

Output is a json file with annotated images

{
    "image_path": "path_to_image.jpg",
    "description": "description of image",
    "keywords": ["keyword1", "keyword2"]
}
