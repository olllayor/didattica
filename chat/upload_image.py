import requests

def upload_image_to_telegraph(image_file):
    files = {'file':
                 (
                     'image.jpg', image_file, 'image/jpeg'
                 )
    }
    response = requests.post('https://telegra.ph/upload', files=files)
    if response.status_code == 200:
        img_src = response.json()
        link = 'https://telegra.ph' + img_src[0]["src"]
        return link
    return None

