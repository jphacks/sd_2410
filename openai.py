import requests
import json

# Django?????API???????URL
url = "http://127.0.0.1:8000/api/openai-api/"  # ????????????????????

# ?????????????
headers = {
    "Content-Type": "application/json",
}
data = {
    "prompt": " say 0"
}

response = requests.post(url, headers=headers, data=json.dumps(data))

# ????????
if response.status_code == 200:
    print("Response:", response.json().get("answer"))
else:
    print("Error:", response.status_code, response.text)
