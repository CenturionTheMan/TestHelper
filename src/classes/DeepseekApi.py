from typing import Dict, List
import requests
import json

class DeepseekApi(object):
    def __init__(self, key):
        self.key = key
    
    def get_response(self, message: str|List[Dict]) -> str:
        if isinstance(message, list):
            data_str = json.dumps({
                "model": "deepseek/deepseek-r1:free",
                "messages": message,
            })
        else:
            data_str = json.dumps({
                "model": "deepseek/deepseek-r1:free",
                "messages": [
                    {
                        "role": "user",
                        "content": message
                    }
                ],
            })
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
                "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
            },
            data=data_str
        )
        
        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code} - {response.text}")
        response_data = response.json()
        if 'choices' not in response_data or len(response_data['choices']) == 0:
            raise Exception("No choices found in response")
        return response_data['choices'][0]['message']['content'].strip()
    