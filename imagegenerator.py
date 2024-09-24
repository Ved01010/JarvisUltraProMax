import requests
from PIL import Image
from io import BytesIO

def createimage(prompt):
    url = 'https://api.airforce/v1/imagine2'
    params = {'prompt': prompt}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        image.save('created_image.png')
    else:
        print(f"failed to retrive image. status {response.status_code}")


createimage('robot')
