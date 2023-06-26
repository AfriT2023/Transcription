import requests
import json
import time

base_url = "https://api.assemblyai.com/v2"

headers = {
    "authorization": "12af36e210ce42a4920d26598adfc070"
}

with open("./my-audio.mp3", "rb") as f:
  response = requests.post(base_url + "/upload",
                          headers=headers,
                          data=f)

upload_url = response.json()["upload_url"]

data = {
    "audio_url": upload_url # You can also use a URL to an audio or video file on the web
}

url = base_url + "/transcript"
response = requests.post(url, json=data, headers=headers)
transcript_id = response.json()['id']
polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

while True:
  transcription_result = requests.get(polling_endpoint, headers=headers).json()

  if transcription_result['status'] == 'completed':
    break

  elif transcription_result['status'] == 'error':
    raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

  else:
    time.sleep(3)
