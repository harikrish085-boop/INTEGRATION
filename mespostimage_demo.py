import requests
import base64
import os
from datetime import datetime
imagename = "Dark-particle-and-fiber-defect-detection-results-under-oblique-texture-a1-a3-dark.webp"
image_dir =os.path.join(os.getcwd(),"images")
image_path = os.path.join(image_dir,imagename)


with open(image_path,"rb") as f:
    img = base64.b64encode(f.read()).decode()

payload = {
            "machinelocation":"UNIT0010",
			"status": "BAD",
			"pinholes": "6",
            "imageName": imagename,
            "imageType": "DFTC001",
            "createdAt": datetime.now().isoformat(),
            "imageData": img
}
####### Post image to MESIntegration API locally running on port 8088 ########
#r = requests.post(
#    "http://localhost:8088/system/webdev/samplequickstart/MESIntegration/api/images/postimagedemo",
#    json=payload
#)
###### Post image to MESIntegration API DEV server running on port 8088 ########
r = requests.post(
    "http://10.34.26.4:8088/system/webdev/samplequickstart/MES_INTEGRATION_REST_API/API/images/postimagedemo",
   json=payload
)

#print(r.json())
print(r.status_code)
print(r)
print("Image posted successfully")  
