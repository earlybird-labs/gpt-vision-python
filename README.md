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


Output is a json file with annotated images
