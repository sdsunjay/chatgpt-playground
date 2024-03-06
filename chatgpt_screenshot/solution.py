import pyautogui
import requests
import base64

from constants import Constants

def take_screenshot_and_save():
    """Take a screenshot and save it to a file."""
    screenshot = pyautogui.screenshot()
    screenshot_path = 'screenshot.png'
    screenshot.save(screenshot_path)
    return screenshot_path

def encode_image(image_path):
    """Encode the image to base64."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def send_image_to_openai(base64_image):
    """Send the encoded image to OpenAI for analysis."""
    # REPLACE WITH YOUR API KEY
    api_key = Constants.API_KEY
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    text = Constants.PHOTO_PROMPT_TEXT
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": text
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_json = response.json()

    if response.status_code == 200 and 'choices' in response_json:
        # Extracting the message from the first choice in the response
        assistant_message = response_json['choices'][0]['message']['content']
        print("Description from the assistant:")
        print(assistant_message)
    else:
        print("Failed to get a valid response. Status Code:", response.status_code)
        print("Response:", response.text)

# Main code
screenshot_path = take_screenshot_and_save()
base64_image = encode_image(screenshot_path)
send_image_to_openai(base64_image)

