import requests,time
import urllib3
while True:
# Disable SSL warning
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    url = "https://localhost:8043/system/webdev/samplequickstart/MESIntegration/mesapi"

    response = requests.get(
        url,
        verify=False
    )

    print(response.status_code)
    print(response.json())
    time.sleep(1)