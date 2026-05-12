import requests
import time

while True:

    response = requests.get(
        "http://localhost:8088/system/webdev/samplequickstart/MESIntegration/mesapi"
    )

    data = response.json()

    print("MES RECEIVED:")
    print(data)

    time.sleep(1)
